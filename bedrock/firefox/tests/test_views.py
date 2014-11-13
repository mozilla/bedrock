# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from funfactory.urlresolvers import reverse
from nose.tools import ok_

from bedrock.mozorg.tests import TestCase


class TestFirefoxNew(TestCase):
    def test_frames_allow(self):
        """
        Bedrock pages get the 'x-frame-options: DENY' header by default.
        The firefox/new page needs to be framable for things like stumbleupon.
        Bug 1004598.
        """
        with self.activate('en-US'):
            resp = self.client.get(reverse('firefox.new'))

        ok_('x-frame-options' not in resp)
