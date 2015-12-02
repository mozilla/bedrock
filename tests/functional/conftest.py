# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

VIEWPORT = {
    'desktop': {'width': 1280, 'height': 1024},
    'mobile': {'width': 320, 'height': 480}}


@pytest.fixture(scope='session')
def capabilities(capabilities):
    capabilities.setdefault('tags', []).append('bedrock')
    return capabilities


@pytest.fixture(autouse=True)
def filter_capabilities(request, selenium):
    capabilities = selenium.capabilities
    firefox = capabilities.get('browserName').lower() == 'firefox'
    if firefox and 'skip_if_firefox' in request.keywords:
        pytest.skip('Test must not be run on Firefox')


@pytest.fixture
def selenium(request, selenium):
    viewport = VIEWPORT['desktop']
    if request.keywords.get('viewport') is not None:
        viewport = VIEWPORT[request.keywords.get('viewport').args[0]]
    selenium.set_window_size(viewport['width'], viewport['height'])
    return selenium
