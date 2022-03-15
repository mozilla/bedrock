# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import html
import re

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

import bleach
import requests
from bleach.css_sanitizer import CSSSanitizer
from html5lib.filters.base import Filter

from bedrock.careers.models import Position
from bedrock.utils.management.decorators import alert_sentry_on_exception

GREENHOUSE_URL = "https://api.greenhouse.io/v1/boards/{}/jobs/?content=true"
# to see the raw data for debugging use this command:
# curl 'https://api.greenhouse.io/v1/boards/mozilla/jobs/?content=true' | \
# jq -r .jobs[0].content | sed 's/&lt;/</g' | sed 's/&quot;/"/g' | sed 's/&gt;/>/g'

# based on bleach.sanitizer.ALLOWED_TAGS
ALLOWED_TAGS = [
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "button",
    "code",
    "div",
    "em",
    "h1",
    "h2",
    "h3",
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
]
ALLOWED_ATTRS = [
    "alt",
    "class",
    "href",
    "id",
    "src",
    "srcset",
    "style",
    "rel",
    "title",
]
ALLOWED_STYLES = [
    "font-weight",
]


class HeaderConverterFilter(Filter):
    def __iter__(self):
        for token in Filter.__iter__(self):
            if token["type"] in ["StartTag", "EndTag"]:
                if token["name"] in ["h1", "h2", "h3"]:
                    token["name"] = "h4"
            yield token


cleaner = bleach.sanitizer.Cleaner(
    tags=ALLOWED_TAGS,
    attributes=ALLOWED_ATTRS,
    css_sanitizer=CSSSanitizer(allowed_css_properties=ALLOWED_STYLES),
    strip=True,
    filters=[HeaderConverterFilter],
)


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
        job_ids = []

        response = requests.get(GREENHOUSE_URL.format(settings.GREENHOUSE_BOARD))
        response.raise_for_status()

        data = response.json()
        for job in data["jobs"]:
            # In case GH includes jobs with the same ID multiple times in the json.
            if job["id"] in job_ids:
                continue

            job_ids.append(job["id"])

            position, created = Position.objects.get_or_create(job_id=job["id"], internal_job_id=job["internal_job_id"], source="gh")

            departments = job.get("departments", "")
            if departments:
                department = departments[0]["name"] or ""
            else:
                department = ""

            is_mofo = False
            if department == "Mozilla Foundation":
                is_mofo = True

            offices = job.get("offices", "")
            if offices:
                location = ",".join([office["name"] for office in offices])
            else:
                location = ""

            jobLocations = job.get("location", {}).get("name", "")

            description = html.unescape(job.get("content", ""))
            description = cleaner.clean(description)
            # Remove empty paragraphs and h4s and paragraphs with \xa0
            # (no-brake space). I ♥ regex
            description = re.sub(r"<(p|h4)>([ ]*|(\xa0)+)</(p|h4)>", "", description)

            for metadata in job.get("metadata", []):
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
                "internal_job_id": job["internal_job_id"],
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

        positions_to_be_removed = Position.objects.exclude(job_id__in=job_ids, source="gh")
        jobs_removed = positions_to_be_removed.count()
        positions_to_be_removed.delete()

        if not quiet:
            self.stdout.write(f"Jobs added: {jobs_added} updated: {jobs_updated} removed: {jobs_removed}")
