from logging import getLogger

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import requests


log = getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        db_url = settings.MAXMIND_DB_URL
        if not db_url:
            log.debug('Skipped downloading GeoIP file')
            return

        try:
            resp = requests.get(db_url, timeout=2, stream=True)
        except requests.Timeout:
            raise CommandError('Request timed out: ' + db_url)
        except requests.RequestException as e:
            raise CommandError(str(e))

        if resp.status_code == 200:
            with open(settings.MAXMIND_DB_PATH, 'wb') as geoip_file:
                for chunk in resp:
                    geoip_file.write(chunk)

        log.info('GeoIP file downloaded successfully.')
