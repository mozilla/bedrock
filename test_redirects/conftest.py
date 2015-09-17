import pytest
from pytest_django.fixtures import live_server


def pytest_addoption(parser):
    group = parser.getgroup('django')
    group._addoption('--mozorg-url',
                     action='store', type='string', dest='mozorg_url', default='local',
                     help='URL of the mozorg server to test (default: local)')


def pytest_configure(config):
    url = config.getvalue('mozorg_url')
    config.mozorg_url = url.rstrip('/')


@pytest.fixture(scope='session')
def live_or_remote_server(request):
    url = request.config.getvalue('mozorg_url').rstrip('/')
    if url == 'local':
        return live_server(request).url

    return url
