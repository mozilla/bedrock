# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from product_details import product_details


def get_latest_version(channel='release'):
    return product_details.thunderbird_versions.get('LATEST_THUNDERBIRD_VERSION')
