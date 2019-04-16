# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from builtins import range
import re
from datetime import date

from bedrock.grants.grants_db import GRANTS
from bedrock.mozorg.tests import TestCase


class TestGrants(TestCase):
    def test_grant_url_slug(self):
        """Grant url slug must be composed of a-z, 0-9, _, and -."""
        for grant in GRANTS:
            self.assertTrue(re.match(r'^[a-z0-9_\-]+$', grant.url), "'%s' is not a valid url slug" % grant.url)

    def test_grant_grantee(self):
        """Grant grantee must be a string."""
        for grant in GRANTS:
            self.assertTrue(len(grant.grantee) > 0, "'%s' is not a valid grantee" % grant.grantee)

    def test_grant_location(self):
        """Grant location must be a string."""
        for grant in GRANTS:
            self.assertTrue(len(grant.location) > 0, "'%s' is not a valid location" % grant.location)

    def test_grant_title(self):
        """Grant title must be a string."""
        for grant in GRANTS:
            self.assertTrue(len(grant.title) > 0, "'%s' is not a valid title" % grant.title)

    def test_grant_type(self):
        """Grant type must be one of 4 valid types."""
        valid_grant_types = [
            u'free-culture-community',
            u'learning-webmaking',
            u'open-source-technology',
            u'user-sovereignty',
        ]
        for grant in GRANTS:
            self.assertIn(grant.type, valid_grant_types)

    def test_grant_total_support(self):
        """Grant total_support must look like a monetary amount."""
        for grant in GRANTS:
            self.assertTrue(re.match(r'^\$\d{1,3},\d{3}(\.\d{2})?$', grant.total_support), "'%s' is not a valid total_support" % grant.total_support)

    def test_grant_year(self):
        """Grant year must be in the range 2006 to next year."""
        next_year = date.today().year + 1
        valid_grant_years = list(range(2006, next_year))
        for grant in GRANTS:
            self.assertIn(grant.year, valid_grant_years)

    def test_grant_description(self):
        """Grant description must be a string."""
        for grant in GRANTS:
            self.assertTrue(len(grant.description) > 0, "'%s' is not a valid description" % grant.description)

    def test_grant_break_down(self):
        """Grant break_down must be an empty string or a dict."""
        for grant in GRANTS:
            self.assertTrue(grant.break_down == u'' or isinstance(grant.break_down, dict), "'%s' is not a valid break_down" % grant.break_down)

    def test_grant_urls(self):
        """Grant urls must be an empty string or a list of urls."""
        for grant in GRANTS:
            self.assertTrue(grant.urls == u'' or isinstance(grant.urls, list), "'%s' is not a list of valid urls" % grant.urls)
