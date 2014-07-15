# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings

import cronjobs

from bedrock.svnfiles import SVNFile


@cronjobs.register
def update_svnfiles(file_id=None):
    file_ids = [file_id] if file_id else settings.SVN_FILES.keys()
    for fid in file_ids:
        SVNFile(fid).update()
