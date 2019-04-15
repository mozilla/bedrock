from builtins import str
from django.conf import settings

from mock import patch

from bedrock.base import waffle


@patch('bedrock.base.waffle.config')
def test_switch_helper(config_mock):
    waffle.switch('dude-and-walter')
    config_mock.assert_called_with('DUDE_AND_WALTER', namespace='SWITCH', default=str(settings.DEV), parser=bool)
