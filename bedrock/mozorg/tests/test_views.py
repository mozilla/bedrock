# -*- coding: utf8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core import mail
from django.test.client import Client
from django.test.utils import override_settings

from captcha.fields import ReCaptchaField
from funfactory.urlresolvers import reverse
from jinja2.exceptions import TemplateNotFound
from requests.exceptions import Timeout
from mock import Mock, patch
from nose.tools import assert_false, eq_, ok_
from pyquery import PyQuery as pq

from bedrock.mozorg.tests import TestCase
from lib import l10n_utils


_ALL = settings.STUB_INSTALLER_ALL


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_hacks_newsletter_frames_allow(self):
        """
        Bedrock pages get the 'x-frame-options: DENY' header by default.
        The hacks newsletter page is framed, so needs to ALLOW.
        """
        with self.activate('en-US'):
            resp = self.client.get(reverse('mozorg.hacks_newsletter'))

        ok_('x-frame-options' not in resp)

    @override_settings(STUB_INSTALLER_LOCALES={'win': _ALL})
    def test_download_button_funnelcake(self):
        """The download button should have the funnelcake ID."""
        with self.activate('en-US'):
            resp = self.client.get(reverse('mozorg.home'), {'f': '5'})
            ok_('product=firefox-stub-f5&' in resp.content)

    @override_settings(STUB_INSTALLER_LOCALES={'win': _ALL})
    def test_download_button_bad_funnelcake(self):
        """The download button should not have a bad funnelcake ID."""
        with self.activate('en-US'):
            resp = self.client.get(reverse('mozorg.home'), {'f': '5dude'})
            ok_('product=firefox-stub&' in resp.content)
            ok_('product=firefox-stub-f5dude&' not in resp.content)

            resp = self.client.get(reverse('mozorg.home'), {'f': '999999999'})
            ok_('product=firefox-stub&' in resp.content)
            ok_('product=firefox-stub-f999999999&' not in resp.content)


class TestUniversityAmbassadors(TestCase):
    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.forms.request')
    @patch('bedrock.mozorg.forms.basket.subscribe')
    def test_subscribe(self, mock_subscribe, mock_request):
        mock_subscribe.return_value = {'token': 'token-example',
                                       'status': 'ok',
                                       'created': 'True'}
        c = Client()
        data = {'email': u'dude@example.com',
                'country': 'gr',
                'fmt': 'H',
                'first_name': 'foo',
                'last_name': 'bar',
                'current_status': 'teacher',
                'school': 'TuC',
                'city': 'Chania',
                'age_confirmation': 'on',
                'expected_graduation_year': '',
                'nl_about_mozilla': 'on',
                'area': '',
                'area_free_text': '',
                'privacy': 'True'}
        request_data = {'FIRST_NAME': data['first_name'],
                        'LAST_NAME': data['last_name'],
                        'STUDENTS_CURRENT_STATUS': data['current_status'],
                        'STUDENTS_SCHOOL': data['school'],
                        'STUDENTS_GRAD_YEAR': data['expected_graduation_year'],
                        'STUDENTS_MAJOR': data['area'],
                        'COUNTRY_': data['country'],
                        'STUDENTS_CITY': data['city'],
                        'STUDENTS_ALLOW_SHARE': 'N'}
        with self.activate('en-US'):
            c.post(reverse('mozorg.contribute_university_ambassadors'), data)
        mock_subscribe.assert_called_with(
            data['email'], ['ambassadors', 'about-mozilla'], format=u'H',
            country=u'gr', source_url=u'',
            welcome_message='Student_Ambassadors_Welcome')
        mock_request.assert_called_with('post',
                                        'custom_update_student_ambassadors',
                                        token='token-example',
                                        data=request_data)


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
        eq_(m.extra_headers['Reply-To'], ','.join(['contribute@mozilla.org'] +
                                                  cc))

    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.email_contribute.basket.subscribe')
    @patch('bedrock.mozorg.email_contribute.requests.post')
    def test_webmaker_mentor_signup(self, mock_post, mock_subscribe):
        """Test Webmaker Mentor signup form for education functional area"""
        self.data.update(interest='education', newsletter=True)
        self.client.post(self.url_en, self.data)

        assert_false(mock_subscribe.called);
        payload = {'email': self.contact, 'custom-1788': '1'}
        mock_post.assert_called_with('https://sendto.mozilla.org/page/s/mentor-signup',
                                     data=payload, timeout=2)

    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.email_contribute.basket.subscribe')
    @patch('bedrock.mozorg.email_contribute.requests.post')
    def test_webmaker_mentor_signup_newsletter_fail(self, mock_post, mock_subscribe):
        """Test Webmaker Mentor signup form when newsletter is not selected"""
        self.data.update(interest='education', newsletter=False)
        self.client.post(self.url_en, self.data)

        assert_false(mock_subscribe.called);
        assert_false(mock_post.called)

    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.email_contribute.basket.subscribe')
    @patch('bedrock.mozorg.email_contribute.requests.post')
    def test_webmaker_mentor_signup_functional_area_fail(self, mock_post, mock_subscribe):
        """Test Webmaker Mentor signup form when functional area is not education"""
        self.data.update(interest='coding', newsletter=True)
        self.client.post(self.url_en, self.data)

        mock_subscribe.assert_called_with(self.contact, 'about-mozilla')
        assert_false(mock_post.called)

    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.email_contribute.basket.subscribe')
    @patch('bedrock.mozorg.email_contribute.requests.post')
    def test_webmaker_mentor_signup_timeout_fail(self, mock_post, mock_subscribe):
        """Test Webmaker Mentor signup form when request times out"""
        mock_post.side_effect = Timeout('Timeout')
        self.data.update(interest='education', newsletter=True)
        res = self.client.post(self.url_en, self.data)

        assert_false(mock_subscribe.called);
        eq_(res.status_code, 200);

    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.email_contribute.jingo.render_to_string')
    def test_no_autoresponse_locale(self, render_mock):
        """
        L10N version to test contacts for functional area without autoresponses
        """
        # first value is for send() and 2nd is for autorespond()
        render_mock.side_effect = ['The Dude minds, man!',
                                   TemplateNotFound('coding.txt')]
        self.data.update(interest='coding')
        self.client.post(self.url_pt_br, self.data)
        eq_(len(mail.outbox), 1)

        m = mail.outbox[0]
        eq_(m.from_email, 'contribute-form@mozilla.org')
        eq_(m.to, ['contribute@mozilla.org'])
        eq_(m.cc, ['envolva-se-mozilla-brasil@googlegroups.com'])
        eq_(m.extra_headers['Reply-To'], self.contact)

    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.email_contribute.jingo.render_to_string')
    def test_with_autoresponse_locale(self, render_mock):
        """
        L10N version to test contacts for functional area with autoresponses
        """
        render_mock.side_effect = 'The Dude abides.'
        self.data.update(interest='support')
        self.client.post(self.url_pt_br, self.data)
        eq_(len(mail.outbox), 2)

        cc = ['envolva-se-mozilla-brasil@googlegroups.com']
        m = mail.outbox[0]
        eq_(m.from_email, 'contribute-form@mozilla.org')
        eq_(m.to, ['contribute@mozilla.org'])
        eq_(m.cc, cc)
        eq_(m.extra_headers['Reply-To'], self.contact)

        m = mail.outbox[1]
        eq_(m.from_email, 'contribute-form@mozilla.org')
        eq_(m.to, [self.contact])
        eq_(m.cc, [])
        eq_(m.extra_headers['Reply-To'], ','.join(['contribute@mozilla.org'] +
                                                  cc))

    @patch.object(ReCaptchaField, 'clean', Mock())
    def test_emails_not_escaped(self):
        """
        Strings in the contribute form should not be HTML escaped
        when inserted into the email, which is just text.

        E.g. if they entered

            J'adore le ''Renard de feu''

        the email should not contain

            J&#39;adore le &#39;&#39;Renard de feu&#39;&#39;

        Tags are still stripped, though.
        """
        STRING = u"J'adore Citröns & <Piñatas> so there"
        EXPECTED = u"J'adore Citröns &  so there"
        self.data.update(comments=STRING)
        self.client.post(self.url_en, self.data)
        eq_(len(mail.outbox), 1)
        m = mail.outbox[0]
        self.assertIn(EXPECTED, m.body)
