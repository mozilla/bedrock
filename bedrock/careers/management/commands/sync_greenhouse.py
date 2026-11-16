# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import html
import re

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

import requests
from justhtml import JustHTML, SanitizationPolicy

from bedrock.base.sanitization import _URL_POLICY
from bedrock.careers.models import Position
from bedrock.utils.management.decorators import alert_sentry_on_exception

GREENHOUSE_URL = "https://boards-api.greenhouse.io/v1/boards/{}/jobs?content=true"
# to see the raw data for debugging use this command:
# curl 'https://boards-api.greenhouse.io/v1/boards/mozilla/jobs?content=true' | \
# jq -r .jobs[0].content | sed 's/&lt;/</g' | sed 's/&quot;/"/g' | sed 's/&gt;/>/g'


# Sanitization policy for job descriptions
_SANITIZE_POLICY = SanitizationPolicy(
    allowed_tags={
        "a",
        "abbr",
        "acronym",
        "b",
        "blockquote",
        "button",
        "code",
        "div",
        "em",
        "h4",
        "h5",
        "h6",
        "i",
        "img",
        "li",
        "ol",
        "p",
        "small",
        "span",
        "strike",
        "strong",
        "ul",
    },
    allowed_attributes={"*": ["alt", "class", "id", "rel", "title"], "a": ["href"], "img": ["src", "srcset"]},
    disallowed_tag_handling="unwrap",
    url_policy=_URL_POLICY,
)
# Regex to convert h1/h2/h3 to h4
_HEADER_RE = re.compile(r"<(/?)(h[123])(\s|>)", re.IGNORECASE)


def _sanitize_job_description(content: str) -> str:
    """Sanitize Greenhouse job description HTML."""
    # Convert h1/h2/h3 to h4 for consistent heading levels
    content = _HEADER_RE.sub(r"<\1h4\3", content)
    return JustHTML(content, sanitize=True, policy=_SANITIZE_POLICY, fragment=True).to_html(pretty=False)


@alert_sentry_on_exception
class Command(BaseCommand):
    help = "Sync jobs from Greenhouse"

    def add_arguments(self, parser):
        parser.add_argument(
            "--quiet",
            action="store_true",
            dest="quiet",
            default=False,
            help="Do not print output to stdout.",
        )

    @transaction.atomic
    def handle(self, quiet, *args, **options):
        jobs_added = 0
        jobs_updated = 0
        jobs_removed = 0
        jobs_skipped = 0
        job_ids = []
        board_by_job_id = {}
        jobs_list = []

        for board in settings.GREENHOUSE_BOARDS:
            response = requests.get(GREENHOUSE_URL.format(board))
            response.raise_for_status()
            # Remember which board each job came from: it decides the employer.
            jobs_list.extend((board, job) for job in response.json()["jobs"])

        for board, job in jobs_list:
            # Greenhouse ids are unique across all boards, so a repeat within one
            # board's JSON is just a duplicated row. The same id arriving from a
            # second board would be a clash bedrock cannot store (job_id is the
            # URL key), so keep the first one and say so.
            if job["id"] in board_by_job_id:
                if board_by_job_id[job["id"]] != board:
                    self.stderr.write(f"Job {job['id']} is on both the {board_by_job_id[job['id']]} and {board} boards; keeping the first")
                continue
            board_by_job_id[job["id"]] = board

            from_foundation_board = board == settings.FOUNDATION_GREENHOUSE_BOARD

            # Greenhouse sets this on every job post. It is the key that groups the
            # per-location postings of one job, so a post without it cannot be
            # placed correctly: skip it rather than guess, and say so.
            internal_job_id = job.get("internal_job_id")
            if not internal_job_id:
                jobs_skipped += 1
                self.stderr.write(f"Skipping job {job['id']}: no internal_job_id")
                continue

            job_ids.append(job["id"])

            position, created = Position.objects.get_or_create(job_id=job["id"], internal_job_id=internal_job_id, source="gh")

            departments = job.get("departments", "")
            if departments:
                department = departments[0]["name"] or ""
            else:
                department = ""

            # Everything on the Foundation board is a MoFo job. Jobs on the MoCo
            # board filed under a "Mozilla Foundation" department are too.
            is_mofo = from_foundation_board or department == "Mozilla Foundation"

            offices = job.get("offices", "")
            if offices:
                location = ",".join([office["name"] for office in offices])
            else:
                location = ""

            # Greenhouse can concatenate with commas or semicolons
            jobLocations = ",".join(job.get("location", {}).get("name", "").split(";"))

            description = html.unescape(job.get("content", ""))
            description = _sanitize_job_description(description)
            # Remove empty paragraphs and h4s and paragraphs with \xa0
            # (no-brake space). I ♥ regex
            description = re.sub(r"<(p|h4)>([ ]*|(\xa0)+)</(p|h4)>", "", description)

            for metadata in job.get("metadata", []) or []:
                if metadata.get("name", "") == "Employment Type":
                    position_type = metadata["value"] or ""
                    break
            else:
                position_type = ""

            object_data = {
                "title": job["title"],
                "department": department,
                "is_mofo": is_mofo,
                "location": location,
                "job_locations": jobLocations,
                "description": description,
                "position_type": position_type,
                "apply_url": job["absolute_url"],
                # Even making this an 'aware' `datetime` like below still results
                # in a `RuntimeWarning` about receiving a naive datetime.
                # "updated_at": datetime.datetime.strptime(job["updated_at"], "%Y-%m-%dT%H:%M:%S%z"),
                "updated_at": job["updated_at"],
                "internal_job_id": internal_job_id,
            }

            changed = False
            for key, value in object_data.items():
                if getattr(position, key, None) != value:
                    changed = True
                    setattr(position, key, value)

            if changed:
                if created:
                    jobs_added += 1
                else:
                    jobs_updated += 1
                position.save()

        # Only delete Greenhouse jobs. Other sources will be supported here later
        positions_to_be_removed = Position.objects.filter(source="gh").exclude(job_id__in=job_ids)
        jobs_removed = positions_to_be_removed.count()
        positions_to_be_removed.delete()

        if not quiet:
            self.stdout.write(f"Jobs added: {jobs_added} updated: {jobs_updated} removed: {jobs_removed} skipped: {jobs_skipped}")
