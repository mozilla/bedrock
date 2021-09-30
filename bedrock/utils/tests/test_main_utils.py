from django.test import override_settings

from bedrock.utils import expand_locale_groups


@override_settings(LANG_GROUPS={"en": ["en-US", "en-GB"]})
def test_expand_locale_groups():
    assert expand_locale_groups(["de", "fr", "en-GB"]) == ["de", "fr", "en-GB"]
    assert expand_locale_groups(["de", "fr", "en"]) == ["de", "fr", "en-US", "en-GB"]
    assert expand_locale_groups(["en"]) == ["en-US", "en-GB"]
