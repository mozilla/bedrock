# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.cms.utils import get_cms_environment


def cms_admin(request):
    return {"cms_environment": get_cms_environment()}
