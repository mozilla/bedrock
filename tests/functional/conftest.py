# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest


@pytest.fixture(scope='session')
def capabilities(capabilities):
    capabilities.setdefault('tags', []).append('bedrock')
    return capabilities


@pytest.fixture
def selenium(selenium):
    selenium.set_window_size(1280, 1024)
    return selenium
