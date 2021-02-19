from mock import patch

from qrcode.image.svg import SvgPathImage

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg.templatetags.qrcode import qrcode


@patch('bedrock.mozorg.templatetags.qrcode.cache')
@patch('bedrock.mozorg.templatetags.qrcode.qr')
class TestQRCode(TestCase):
    def test_qrcode_cache_cold(self, qr_mock, cache_mock):
        cache_mock.get.return_value = None
        data = 'https://dude.abide'
        qrcode(data, 20)
        qr_mock.make.assert_called_with(data, image_factory=SvgPathImage, box_size=20)

    def test_qrcode_cache_warm(self, qr_mock, cache_mock):
        cache_mock.get.return_value = '<svg>stuff</svg>'
        data = 'https://dude.abide'
        qrcode(data, 20)
        qr_mock.make.assert_not_called()
