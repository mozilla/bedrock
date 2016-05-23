# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This is here so that we can mix storages as we need.

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

from pipeline.storage import PipelineMixin


class ManifestPipelineStorage(PipelineMixin, ManifestStaticFilesStorage):
    # turn off bundling in debug mode
    packing = not settings.DEBUG
