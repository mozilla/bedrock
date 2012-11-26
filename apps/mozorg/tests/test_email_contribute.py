# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from mozorg.tests import TestCase
from nose.tools import assert_false, eq_, ok_

from mozorg.email_contribute import FUNCTIONAL_AREAS, LOCALE_CONTACTS

class TestEmailContribute(TestCase):
    def test_valid_locale_contacts(self):
        for locale, contacts in LOCALE_CONTACTS.items():
            ok_(locale in settings.PROD_LANGUAGES)
            ok_(type(contacts) is list)

    def test_valid_functional_areas(self):
        for area in FUNCTIONAL_AREAS:
            ok_(type(area.contacts) is list)
