# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.core.management.base import BaseCommand
from django.conf import settings

from bedrock.utils.git import GitRepo


class Command(BaseCommand):
    help = 'Clones or updates l10n info from github'

    def handle(self, *args, **options):
        repo = GitRepo(settings.LOCALES_PATH, settings.LOCALES_REPO)
        repo.update()
