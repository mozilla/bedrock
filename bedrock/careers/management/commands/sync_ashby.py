# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import html
import re

from django.core.management.base import BaseCommand
from django.db import transaction

import requests
from justhtml import JustHTML, SanitizationPolicy

from bedrock.base.sanitization import _URL_POLICY
from bedrock.careers.models import Position
from bedrock.utils.management.decorators import alert_sentry_on_exception

ASHBY_URL = "https://api.ashbyhq.com/jobPosting.list"
# to see the raw data for debugging use this command:
# curl 'https://api.ashbyhq.com/jobPosting.list' | \
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
    """Sanitize Ashby job description HTML."""
    # Convert h1/h2/h3 to h4 for consistent heading levels
    content = _HEADER_RE.sub(r"<\1h4\3", content)
    return JustHTML(content, safe=True, policy=_SANITIZE_POLICY, fragment=True).to_html(pretty=False)


@alert_sentry_on_exception
class Command(BaseCommand):
    help = "Sync jobs from Ashby"

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
        job_ids = []
        sources = ["https://api.ashbyhq.com/jobPosting.list"]
        jobs_list = []

        for source in sources:
            response = requests.get(source)
            response.raise_for_status()
            data = response.json()
            jobs_list.extend(data["jobs"])

        response = requests.get("https://api.ashbyhq.com/location.list")
        response.raise_for_status()
        data = response.json()
        locations = data["results"]

        for job in jobs_list:
            # In case Ashby includes jobs with the same ID multiple times in the json.
            if job["id"] in job_ids:
                continue

            job_ids.append(job["id"])

            position, created = Position.objects.get_or_create(job_id=job["id"], internal_job_id=job.get("internal_job_id", None), source="ashby")
            departmentName = job.get("departmentName", "")
            location = job.get("locationName", "")
            position_type = job.get("workplaceType", "")
            primary_location = job["locationIds"]["primaryLocationId"]

            # TODO remove this as there are more than just MoFo
            is_mofo = departmentName == "Mozilla Foundation"

            description = html.unescape(job.get("content", ""))
            description = _sanitize_job_description(description)
            # Remove empty paragraphs and h4s and paragraphs with \xa0
            # (no-brake space). I ♥ regex
            description = re.sub(r"<(p|h4)>([ ]*|(\xa0)+)</(p|h4)>", "", description)

            object_data = {
                "title": job["title"],
                "department": departmentName,
                "is_mofo": is_mofo,
                "location": location,
                "job_locations": locations[primary_location],
                "description": description,  # ???
                "position_type": position_type,
                "apply_url": job["applyLink"],
                # Even making this an 'aware' `datetime` like below still results
                # in a `RuntimeWarning` about receiving a naive datetime.
                # "updated_at": datetime.datetime.strptime(job["updated_at"], "%Y-%m-%dT%H:%M:%S%z"),
                "updated_at": job["updatedAt"],
                "internal_job_id": job.get("internal_job_id", None),
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

        positions_to_be_removed = Position.objects.exclude(job_id__in=job_ids, source="ashby")
        jobs_removed = positions_to_be_removed.count()
        positions_to_be_removed.delete()

        if not quiet:
            self.stdout.write(f"Jobs added: {jobs_added} updated: {jobs_updated} removed: {jobs_removed}")
