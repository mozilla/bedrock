import json
from hashlib import sha256

from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import RequestFactory

from bedrock.contentful.api import ContentfulPage
from bedrock.contentful.models import ContentfulEntry


def data_hash(data):
    str_data = json.dumps(data, sort_keys=True)
    return sha256(str_data.encode("utf8")).hexdigest()


class Command(BaseCommand):
    rf = RequestFactory()

    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output."),
        parser.add_argument(
            "-f", "--force", action="store_true", dest="force", default=False, help="Load the data even if nothing new from Contentful."
        ),

    def log(self, msg):
        if not self.quiet:
            print(msg)

    def handle(self, *args, **options):
        self.quiet = options["quiet"]
        self.force = options["force"]
        if settings.CONTENTFUL_SPACE_ID and settings.CONTENTFUL_SPACE_KEY:
            self.log("Updating Contentful Data")
            added, updated = self.refresh()
            self.log(f"Done. Added: {added}. Updated: {updated}")
        else:
            print("Contentful credentials not configured")
            return

    def refresh(self):
        updated_count = 0
        added_count = 0
        content_ids = []
        for ctype in settings.CONTENTFUL_CONTENT_TYPES:
            for entry in ContentfulPage.client.entries({"content_type": ctype, "include": 0}).items:
                content_ids.append((ctype, entry.sys["id"]))

        for ctype, page_id in content_ids:
            request = self.rf.get("/")
            request.locale = "en-US"
            page = ContentfulPage(request, page_id)
            page_data = page.get_content()
            language = page_data["info"]["lang"]
            hash = data_hash(page_data)

            try:
                obj = ContentfulEntry.objects.get(contentful_id=page_id)
            except ContentfulEntry.DoesNotExist:
                ContentfulEntry.objects.create(
                    contentful_id=page_id,
                    content_type=ctype,
                    language=language,
                    data_hash=hash,
                    data=page_data,
                )
                added_count += 1
            else:
                if self.force or hash != obj.data_hash:
                    obj.language = language
                    obj.data_hash = hash
                    obj.data = page_data
                    obj.save()
                    updated_count += 1

        return added_count, updated_count
