from mock import patch

from qrcode.image.svg import SvgPathImage

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg.templatetags.qrcode import qrcode


@patch('bedrock.mozorg.templatetags.qrcode.QR_CACHE_PATH')
@patch('bedrock.mozorg.templatetags.qrcode.qr')
class TestQRCode(TestCase):
    def test_qrcode_cache_cold(self, qr_mock, qrcp_mock):
        qrcp_mock.joinpath().exists.return_value = False
        data = 'https://dude.abide'
        qrcode(data, 20)
        qr_mock.make.assert_called_with(data, image_factory=SvgPathImage, box_size=20)

    def test_qrcode_cache_warm(self, qr_mock, qrcp_mock):
        qrcp_mock.joinpath().exists.return_value = True
        data = 'https://dude.abide'
        qrcode(data, 20)
        qr_mock.make.assert_not_called()
