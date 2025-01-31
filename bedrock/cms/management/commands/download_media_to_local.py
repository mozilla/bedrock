# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from google.cloud import storage

from bedrock.cms.models import BedrockImage
from bedrock.settings.base import path as build_path

BUCKETS = {
    "dev": "bedrock-nonprod-dev-cms-media",
    "stage": "bedrock-nonprod-stage-cms-media",
    "prod": "bedrock-prod-prod-cms-media",
}


class Command(BaseCommand):
    help = """Downloads public media files from the appropriate cloud bucket
    so that they match the sqlite database being currently used."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--environment",
            default="dev",
            help="Which Springfield environment are you downloading from? Values are dev | stage | prod (default is dev)",
        )
        parser.add_argument(
            "--redownload",
            action="store_true",
            dest="redownload",
            default=False,
            help="If passed, will force re-download of all the assets in the relevant bucket.",
        )

    def handle(self, *args, **options):
        # If we're not using sqlite, stop, because this tool isn't for that

        if settings.DATABASES["default"]["ENGINE"] != "django.db.backends.sqlite3":
            self.stderr.write(f"This command only works if you are using sqlite as your local DB. Got {settings.DATABASES['default']['ENGINE']}\n")
            sys.exit(1)

        try:
            bucket_name = BUCKETS[options["environment"]]
        except KeyError:
            self.stderr.write(f"Couldn't determine which bucket you wanted. Got {options['environment']}\n")
            sys.exit(1)

        storage_client = storage.Client.create_anonymous_client()
        bucket = storage_client.bucket(bucket_name)

        # Get the files, ideally in a way that checks whether we have them already
        # unless the --redownload param is passed
        redownload = options["redownload"]
        if redownload:
            self.stdout.write("Forcing redownload of all files.\n")

        for image in BedrockImage.objects.all():
            image_key = f"media/cms/{image.file.name}"
            local_dest = build_path(settings.MEDIA_ROOT, image.file.name)

            expected_output_dirs = [
                build_path(settings.MEDIA_ROOT, "original_images"),
                build_path(settings.MEDIA_ROOT, "images"),
            ]
            for dir_path in expected_output_dirs:
                if not os.path.exists(dir_path):
                    self.stdout.write(f"setting up: {dir_path}\n")
                    os.makedirs(dir_path)

            if os.path.exists(local_dest) and not redownload:
                self.stdout.write(f"Skipping: {local_dest} already exists locally.\n")
            else:
                blob = bucket.blob(image_key)
                blob.download_to_filename(local_dest)
                self.stdout.write(f"Downloaded {image_key} from {bucket_name} to {local_dest}\n")
                if redownload:
                    # The DB will still think it has renditions included, and we want to regenerate those
                    self.stdout.write(f"Deleting DB records of old renditions for {image_key}\n")
                    image.renditions.all().delete()
                image._pre_generate_expected_renditions()
                self.stdout.write("Triggered local generation of renditions\n")

        self.stdout.write("All done.\n")
