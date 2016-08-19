# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

VIEWPORT = {
    'desktop': {'width': 1280, 'height': 1024},
    'mobile': {'width': 320, 'height': 480}}


@pytest.fixture
def capabilities(request, capabilities):
    driver = request.config.getoption('driver')
    if capabilities.get('browserName', driver).lower() == 'firefox':
        capabilities['marionette'] = True
    return capabilities


@pytest.fixture
def driver_log():
    return 'tests/functional/driver.log'


@pytest.fixture(scope='session')
def session_capabilities(pytestconfig, session_capabilities):
    if pytestconfig.getoption('driver') == 'SauceLabs':
        session_capabilities.setdefault('tags', []).append('bedrock')

        # Avoid default SauceLabs proxy for IE8.
        session_capabilities['avoidProxy'] = True

    return session_capabilities


@pytest.fixture
def firefox(selenium):
    return selenium.capabilities.get('browserName').lower() == 'firefox'


@pytest.fixture
def internet_explorer(selenium):
    return selenium.capabilities.get('browserName').lower() == 'internet explorer'


@pytest.fixture(autouse=True)
def filter_capabilities(request):
    marker = None
    if request.node.get_marker('skip_if_firefox') and request.getfuncargvalue('firefox'):
        marker = request.node.get_marker('skip_if_firefox')
    if request.node.get_marker('skip_if_not_firefox') and not request.getfuncargvalue('firefox'):
        marker = request.node.get_marker('skip_if_not_firefox')
    if request.node.get_marker('skip_if_internet_explorer') and request.getfuncargvalue('internet_explorer'):
        marker = request.node.get_marker('skip_if_internet_explorer')

    if marker:
        reason = marker.kwargs.get('reason') or marker.name
        pytest.skip(reason)


@pytest.fixture
def selenium(request, selenium):
    viewport = VIEWPORT['desktop']
    if request.keywords.get('viewport') is not None:
        viewport = VIEWPORT[request.keywords.get('viewport').args[0]]
    selenium.set_window_size(viewport['width'], viewport['height'])
    return selenium
