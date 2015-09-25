from django.test import TestCase

from mock import Mock, patch
from whitenoise.base import StaticFile

from bedrock.base.static import BedrockWhiteNoise


class TestBedrockWhiteNoise(TestCase):
    wn = BedrockWhiteNoise(Mock())

    def test_immutable_files(self):
        with patch.object(self.wn, 'is_immutable_file', return_value=True):
            static_file = Mock(headers={})
            self.wn.add_cache_headers(static_file, 'dude.txt')
            self.assertTrue(static_file.headers['Cache-Control'].endswith(
                'max-age={}'.format(self.wn.FOREVER)))

    def test_font_files(self):
        with patch.object(self.wn, 'is_immutable_file', return_value=False):
            static_file = Mock(headers={})
            self.wn.add_cache_headers(static_file, 'media/fonts/dude.txt')
            self.assertTrue(static_file.headers['Cache-Control'].endswith(
                'max-age={}'.format(self.wn.ONE_MONTH)))

    def test_caldata_files(self):
        with patch.object(self.wn, 'is_immutable_file', return_value=False):
            static_file = Mock(headers={})
            self.wn.add_cache_headers(static_file, 'media/caldata/ThaiHolidays.ics')
            self.assertTrue(static_file.headers['Cache-Control'].endswith(
                'max-age={}'.format(self.wn.ONE_MONTH)))

            # also at alternate path
            self.wn.add_cache_headers(static_file, 'project/calendar/caldata/ThaiHolidays.ics')
            self.assertTrue(static_file.headers['Cache-Control'].endswith(
                'max-age={}'.format(self.wn.ONE_MONTH)))

    def test_immutable_font_files(self):
        with patch.object(self.wn, 'is_immutable_file', return_value=True):
            static_file = Mock(headers={})
            self.wn.add_cache_headers(static_file, 'media/fonts/dude.txt')
            self.assertTrue(static_file.headers['Cache-Control'].endswith(
                'max-age={}'.format(self.wn.FOREVER)))

    def test_other_files(self):
        with patch.object(self.wn, 'is_immutable_file', return_value=False):
            static_file = Mock(headers={})
            self.wn.add_cache_headers(static_file, 'media/dude.txt')
            self.assertTrue(static_file.headers['Cache-Control'].endswith(
                'max-age={}'.format(self.wn.max_age)))

    def test_forbidden_flash(self):
        # Bug 1005674
        flash_file = StaticFile('/path/to/playerWithControls.swf')
        environ = {'QUERY_STRING': 'flv=http://example.com/logjammin.flv'}
        start_response = Mock()
        self.wn.serve(flash_file, environ, start_response)
        start_response.assert_called_with('403 Forbidden', [])

    def test_forbidden_flash_no_qs(self):
        # Bug 1005674
        flash_file = StaticFile('/path/to/playerWithControls.swf')
        environ = {'QUERY_STRING': ''}
        start_response = Mock()
        self.wn.serve(flash_file, environ, start_response)
        start_response.assert_called_with('403 Forbidden', [])

    @patch('bedrock.base.static.DjangoWhiteNoise.serve')
    def test_forbidden_flash_okay_relative(self, mock_serve):
        # Bug 1005674
        flash_file = StaticFile('/path/to/playerWithControls.swf')
        environ = {'QUERY_STRING': 'flv=/relative/url/awesome.flv'}
        start_response = Mock()
        self.wn.serve(flash_file, environ, start_response)
        mock_serve.assert_called_with(flash_file, environ, start_response)

    @patch('bedrock.base.static.DjangoWhiteNoise.serve')
    def test_forbidden_flash_okay_remote(self, mock_serve):
        # Bug 1005674
        flash_file = StaticFile('/path/to/playerWithControls.swf')
        environ = {'QUERY_STRING': 'flv=https://videos.mozilla.org/awesome.flv'}
        start_response = Mock()
        self.wn.serve(flash_file, environ, start_response)
        mock_serve.assert_called_with(flash_file, environ, start_response)
