# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mock import Mock, patch
from captcha.fields import ReCaptchaField

from django.core import mail
from django.test.client import Client

import l10n_utils
from mozorg.tests import TestCase
from funfactory.urlresolvers import reverse
from nose.tools import assert_false, eq_, ok_
from nose.plugins.skip import SkipTest
from pyquery import PyQuery as pq


@patch.object(l10n_utils, 'lang_file_is_active', lambda *x: True)
class TestContribute(TestCase):
    def setUp(self):
        self.client = Client()
        with self.activate('en-US'):
            self.url_en = reverse('mozorg.contribute')
        with self.activate('pt-BR'):
            self.url_pt_br = reverse('mozorg.contribute')
        self.contact = 'foo@bar.com'
        self.data = {
            'contribute-form': 'Y',
            'email': self.contact,
            'interest': 'coding',
            'privacy': True,
            'comments': 'Wesh!',
        }

    def tearDown(self):
        mail.outbox = []

    def test_newsletter_en_only(self):
        """Test that the newsletter features are only available in en-US"""
        response = self.client.get(self.url_en)
        doc = pq(response.content)
        ok_(doc('.field-newsletter'))
        ok_(doc('a[href="#newsletter"]'))
        ok_(doc('#newsletter'))

        with self.activate('fr'):
            url = reverse('mozorg.contribute')
        response = self.client.get(url)
        doc = pq(response.content)
        assert_false(doc('.field-NEWSLETTER'))
        assert_false(doc('a[href="#newsletter"]'))
        assert_false(doc('#newsletter'))

    @patch.object(ReCaptchaField, 'clean', Mock())
    def test_no_autoresponse(self):
        """Test contacts for functional area without autoresponses"""
        self.data.update(interest='coding')
        self.client.post(self.url_en, self.data)
        eq_(len(mail.outbox), 1)

        m = mail.outbox[0]
        eq_(m.from_email, 'contribute-form@mozilla.org')
        eq_(m.to, ['contribute@mozilla.org'])
        eq_(m.cc, ['josh@joshmatthews.net'])
        eq_(m.extra_headers['Reply-To'], self.contact)

    @patch.object(ReCaptchaField, 'clean', Mock())
    def test_with_autoresponse(self):
        """Test contacts for functional area with autoresponses"""
        self.data.update(interest='support')
        self.client.post(self.url_en, self.data)
        eq_(len(mail.outbox), 2)

        cc = ['jay@jaygarcia.com', 'rardila@mozilla.com', 'madasan@gmail.com']
        m = mail.outbox[0]
        eq_(m.from_email, 'contribute-form@mozilla.org')
        eq_(m.to, ['contribute@mozilla.org'])
        eq_(m.cc, cc)
        eq_(m.extra_headers['Reply-To'], self.contact)

        m = mail.outbox[1]
        eq_(m.from_email, 'contribute-form@mozilla.org')
        eq_(m.to, [self.contact])
        eq_(m.cc, [])
        eq_(m.extra_headers['Reply-To'], ','.join(cc))

    @patch.object(ReCaptchaField, 'clean', Mock())
    def test_no_autoresponse_locale(self):
        """
        L10N version to test contacts for functional area without autoresponses
        """
        self.data.update(interest='coding')
        self.client.post(self.url_pt_br, self.data)
        eq_(len(mail.outbox), 1)

        m = mail.outbox[0]
        eq_(m.from_email, 'contribute-form@mozilla.org')
        eq_(m.to, ['contribute@mozilla.org'])
        eq_(m.cc, ['marcelo.araldi@yahoo.com.br'])
        eq_(m.extra_headers['Reply-To'], self.contact)

    @patch.object(ReCaptchaField, 'clean', Mock())
    def test_with_autoresponse_locale(self):
        """
        L10N version to test contacts for functional area with autoresponses
        """
        # UnSkip once pt-BR translation of support.txt is done
        raise SkipTest
        self.data.update(interest='support')
        self.client.post(self.url_pt_br, self.data)
        eq_(len(mail.outbox), 2)

        cc = ['marcelo.araldi@yahoo.com.br']
        m = mail.outbox[0]
        eq_(m.from_email, 'contribute-form@mozilla.org')
        eq_(m.to, ['contribute@mozilla.org'])
        eq_(m.cc, cc)
        eq_(m.extra_headers['Reply-To'], self.contact)

        m = mail.outbox[1]
        eq_(m.from_email, 'contribute-form@mozilla.org')
        eq_(m.to, [self.contact])
        eq_(m.cc, [])
        eq_(m.extra_headers['Reply-To'], ','.join(cc))
