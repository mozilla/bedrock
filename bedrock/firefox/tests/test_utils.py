# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.conf import settings
from django.test import RequestFactory
from django.test.utils import override_settings

from mock import ANY, patch
from nose.tools import ok_, eq_

from bedrock.mozorg.tests import TestCase
from bedrock.firefox.tests.test_base import firefox_details
from bedrock.firefox.utils import (firefox_version, is_current_or_newer,
    is_firefox, product_details)

@patch.dict(firefox_details.firefox_versions,
            FIREFOX_ESR='24.8.1',
            FIREFOX_ESR_NEXT='31.1.1',
            LATEST_FIREFOX_VERSION='33.0')
class TestIsCurrentOrNewer(TestCase):
    def test_current(self):
        """
        Should return True for all Firefox user agents at version 33.0 or greater.
        """
        eq_(is_current_or_newer(firefox_version('Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0')), True)
        eq_(is_current_or_newer(firefox_version('Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0')), True)
        eq_(is_current_or_newer(firefox_version('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:34.0) Gecko/20100101 Firefox/34.0')), True)

    def test_old(self):
        """
        Should return False for all Firefox user agents lower than version 31.
        """
        eq_(is_current_or_newer(firefox_version('Mozilla/5.0 (X11; Linux x86_64; rv:32.0.2) Gecko/20100101 Firefox/32.0.2')), False)
        eq_(is_current_or_newer(firefox_version('Mozilla/5.0 (Windows NT 5.1; rv:28.0) Gecko/20100101 Firefox/28.0')), False)
        eq_(is_current_or_newer(firefox_version('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0.1) Gecko/20100101 Firefox/21.0.1')), False)

    def test_esr(self):
        """
        Should return True for all Firefox user agents matching major ESR versions.
        """
        eq_(is_current_or_newer(firefox_version('Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0')), True)
        eq_(is_current_or_newer(firefox_version('Mozilla/5.0 (X11; Linux x86_64; rv:24.8.1) Gecko/20100101 Firefox/24.8.1')), True)
        eq_(is_current_or_newer(firefox_version('Mozilla/5.0 (Windows NT 5.1; rv:31.1.1) Gecko/20100101 Firefox/31.1.1')), True)


class TestIsFirefox(TestCase):
    def test_non_firefox(self):
        """
        Should return False for all non-Firefox user agents.
        """
        eq_(is_firefox('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'), False)
        eq_(is_firefox('Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; en; rv:1.9.2.24) Gecko/20111114 Camino/2.1 (like Firefox/3.6.24)'), False)
        eq_(is_firefox('Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1'), False)
        eq_(is_firefox('Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36'), False)
        eq_(is_firefox('Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1'), False)

    def test_firefox(self):
        """
        Should return True for all Firefox user agents
        """
        eq_(is_firefox('Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'), True)
        eq_(is_firefox('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0'), True)
        eq_(is_firefox('Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0'), True)
        eq_(is_firefox('Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'), True)
        eq_(is_firefox('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0'), True)


class TestFirefoxVersion(TestCase):
    def test_non_firefox(self):
        """
        Should return 0 for non-Firefox user agents.
        """
        eq_(firefox_version('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'), '0')
        eq_(firefox_version('Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1'), '0')
        eq_(firefox_version('Mozilla/5.0 (X11; Linux i686; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1'), '0')

    def test_firefox(self):
        """
        Should return the full version number for all Firefox user agents.
        """
        eq_(firefox_version('Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'), '31.0')
        eq_(firefox_version('Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20100101 Firefox/22.0'), '22.0')
        eq_(firefox_version('Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'), '16.0.1')
