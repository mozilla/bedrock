from bedrock.firefox.forms import SMSSendToDeviceForm
from bedrock.mozorg.tests import TestCase


class TestSMSToDeviceForm(TestCase):
    def test_empty(self):
        form = SMSSendToDeviceForm({"phone_number": "", "platform": "ios"})
        assert not form.is_valid()
        assert form.errors["phone_number"] == ["Invalid phone number"]

    def test_invalid(self):
        form = SMSSendToDeviceForm({"phone_number": "1234", "platform": "ios"})
        assert not form.is_valid()
        assert form.errors["phone_number"] == ["Invalid phone number for region: US"]

    def test_number_formatting(self):
        form = SMSSendToDeviceForm({"phone_number": "4155551212", "platform": "ios"})
        assert form.is_valid(), form.errors
        assert form.cleaned_data["phone_number"] == "+14155551212"
