from django.test import TestCase

from mock import Mock, patch

from bedrock.base.static import BedrockWhiteNoise


class TestBedrockWhiteNoise(TestCase):
    def setUp(self):
        self.wn = BedrockWhiteNoise(Mock())

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
