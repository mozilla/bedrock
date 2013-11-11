# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.test.client import RequestFactory
from funfactory.urlresolvers import reverse

from nose.tools import eq_

from bedrock.mozorg.context_processors import funnelcake_param
from bedrock.mozorg.tests import TestCase


class TestFunnelcakeParam(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def _funnelcake(self, url='/', **kwargs):
        return funnelcake_param(self.rf.get(url, kwargs))

    def test_funnelcake_param_noop(self):
        """Should return an empty dict normally."""
        eq_(self._funnelcake(), {})

    def test_funnelcake_param_f(self):
        """Should inject funnelcake into context."""
        eq_(self._funnelcake(f='5'), {'funnelcake_id': '5'})
        eq_(self._funnelcake(f='234'), {'funnelcake_id': '234'})

    def test_funnelcake_param_bad(self):
        """Should not inject bad funnelcake into context."""
        eq_(self._funnelcake(f='5dude'), {})
        eq_(self._funnelcake(f='123456'), {})

    def test_funnelcake_param_increment_installer_help(self):
        """FC param should be +1 on the firefox/installer-help/ page.

        Bug 933852.
        """
        url = reverse('firefox.installer-help')
        ctx = self._funnelcake(url, f='20')
        eq_(ctx['funnelcake_id'], '21')

        ctx = self._funnelcake(url, f='10')
        eq_(ctx['funnelcake_id'], '11')
