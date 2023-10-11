# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from tempfile import TemporaryFile

from django.conf import settings
from django.db import models
from django.utils.dateparse import parse_date, parse_datetime

import requests
from google.cloud import storage


class BreachManager(models.Manager):
    def sync_db(self):
        # Fetch new breach data and update the database.
        BREACH_URL = "https://haveibeenpwned.com/api/v3/breaches"

        response = requests.get(BREACH_URL, headers={"User-Agent": "mozilla-org"})
        response.raise_for_status()

        breaches_added = 0
        breaches_updated = 0

        for data in response.json():
            breach, created = self.get_or_create(name=data["Name"])
            obj_data = {
                "title": data["Title"],
                "domain": data["Domain"],
                "breach_date": data["BreachDate"],
                "added_date": data["AddedDate"],
                "modified_date": data["ModifiedDate"],
                "pwn_count": data["PwnCount"],
                "logo_path": "",  # We aren't using the hibp logos because they are too large and inconsistent.
                "data_classes": data["DataClasses"],
                "is_verified": data["IsVerified"],
                "is_fabricated": data["IsFabricated"],
                "is_sensitive": data["IsSensitive"],
                "is_retired": data["IsRetired"],
                "is_spam_list": data["IsSpamList"],
                "is_malware": data["IsMalware"],
            }

            changed = False
            for key, value in obj_data.items():
                # Convert date strings to date objects.
                if key == "breach_date":
                    value = parse_date(value)
                elif key in ("added_date", "modified_date"):
                    value = parse_datetime(value)

                if getattr(breach, key, None) != value:
                    changed = True
                    setattr(breach, key, value)

            if changed:
                if created:
                    breaches_added += 1
                else:
                    breaches_updated += 1
                breach.save()

        return breaches_added, breaches_updated

    def sync_logos(self, verbose=True):
        # Iterate over db breaches and download logos.
        verbose and print("Syncing breach logos...")

        GCS_DIR = "media/"
        GCS_PATH = "img/products/monitor/breach_logos/"

        def _urlize(path):
            # Convert a GCS path to the full static URL to the logo.
            return path.replace(GCS_DIR, settings.STATIC_URL, 1)

        # Get list of all breach logos from GCS.
        try:
            client = storage.Client()
            bucket = client.get_bucket(settings.GCS_MEDIA_BUCKET_NAME)
            blob_list = bucket.list_blobs(prefix=GCS_DIR + GCS_PATH)
            gcs_logos = [_urlize(blob.name) for blob in blob_list]
        except Exception as e:
            verbose and print(f"Failed to get list of GCS logos: {e}. Aborting.")
            return

        for breach in self.all():
            if not breach.domain:
                verbose and print(f"Skipping {breach.name} because it has no domain.")
                continue

            # Check if the breach has a logo_path value and if it exists in GCS.
            if breach.logo_path and breach.logo_path in gcs_logos:
                verbose and print(f"Skipping {breach.name} because it already has an existing logo.")
                continue

            # NOTE: We are storing the full logo URL in the logo_path field since the db is per deployment environment.
            # This allows us to reference the logo images locally without needing to download them.
            logo_path = f"{GCS_DIR}{GCS_PATH}{breach.domain.lower()}.ico"
            logo_url = _urlize(logo_path)

            # Check if the logo exists in GCS. If so, no reason to re-fetch fron DDG.
            if logo_url in gcs_logos:
                breach.logo_path = logo_url
                breach.save()
                print(f"Found existing logo for {breach.name} in GCS. Updating db.")
                continue

            # Fetch the logo from the ddg api.
            resp = requests.get(f"https://icons.duckduckgo.com/ip3/{breach.domain}.ico", headers={"User-Agent": "mozilla-org"})
            if resp.status_code != 200:
                verbose and print(f"Failed to fetch logo for {breach.name} from ddg api. Status code: {resp.status_code}.")
                continue

            # Save the logo to a temp file then upload to GCS.
            with TemporaryFile() as tf:
                tf.write(resp.content)
                tf.seek(0)
                try:
                    blob = bucket.blob(logo_path)
                    blob.upload_from_file(tf)
                    print(f"Uploaded logo for {breach.name} to GCS: {logo_path}")
                except Exception as e:
                    verbose and print(f"Failed to upload logo for {breach.name} to GCS: {e}")
                    continue

            # Update the logo_path value in the db.
            breach.logo_path = logo_url
            breach.save()
            verbose and print(f"Saved logo for {breach.name} to {breach.logo_path}")

            # Add the logo_path to the list of gcs logos.
            gcs_logos.append(logo_path)


class Breach(models.Model):
    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    breach_date = models.DateField(null=True)
    added_date = models.DateTimeField(null=True)
    modified_date = models.DateTimeField(null=True)
    pwn_count = models.PositiveIntegerField(default=0)
    # Note: The description is unused on the site and not included to reduce the size of the database.
    # description = models.TextField()
    logo_path = models.CharField(max_length=255)
    data_classes = models.JSONField(default=list)
    is_verified = models.BooleanField(default=False)
    is_fabricated = models.BooleanField(default=False)
    is_sensitive = models.BooleanField(default=False)
    is_retired = models.BooleanField(default=False)
    is_spam_list = models.BooleanField(default=False)
    is_malware = models.BooleanField(default=False)

    objects = BreachManager()

    class Meta:
        verbose_name_plural = "Breaches"

    def __str__(self):
        return self.name

    @property
    def category(self):
        if self.name in ("Exactis", "Apollo", "YouveBeenScraped", "ElasticsearchSalesLeads", "Estonia", "MasterDeeds", "PDL"):
            return "data-aggregator-breach"
        if self.is_sensitive:
            return "sensitive-breach"
        if self.domain != "":
            return "website-breach"
        return "data-aggregator-breach"

    @property
    def is_delayed(self):
        # Boolean whether the difference between the `breach_date` and `added_date` is greater than 90 days.
        return abs((self.added_date.date() - self.breach_date).days) > 90
