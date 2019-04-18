"""Tests for settings"""

from django.conf import settings
from django.test import override_settings


@override_settings(DEV=False, PROD_LANGUAGES=('de', 'fr', 'nb-NO', 'ja', 'ja-JP-mac',
                                              'en-US', 'en-GB'))
def test_lang_groups():
    # should not contain 'nb' and 'ja' group should contain 'ja'
    assert dict(settings.LANG_GROUPS) == {
        'ja': ['ja-JP-mac', 'ja'],
        'en': ['en-US', 'en-GB'],
    }
