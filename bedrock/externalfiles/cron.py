# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings

import cronjobs

from bedrock.externalfiles import ExternalFile


@cronjobs.register
def update_externalfiles(file_id=None):
    file_ids = [file_id] if file_id else settings.EXTERNAL_FILES.keys()
    for fid in file_ids:
        ExternalFile(fid).update()
