# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.management.base import BaseCommand
from lib.sitemaps import update_sitemaps


class Command(BaseCommand):
    args = ''
    help = 'Update XML sitemaps based on the list of localized pages.'

    def handle(self, *args, **options):
        update_sitemaps()
