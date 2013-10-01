# -*- coding: utf8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core import mail
from django.test.client import Client, RequestFactory
from django.test.utils import override_settings
from django.utils import simplejson

from captcha.fields import ReCaptchaField
from funfactory.urlresolvers import reverse
from jinja2.exceptions import TemplateNotFound
from requests.exceptions import Timeout
from mock import ANY, Mock, patch
from nose.tools import assert_false, eq_, ok_
from pyquery import PyQuery as pq

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg import views
from lib import l10n_utils


_ALL = settings.STUB_INSTALLER_ALL


@patch('bedrock.mozorg.views.l10n_utils.render')
class TestHome(TestCase):
    def setUp(self):
        self.view = views.HomeTestView.as_view()
        self.rf = RequestFactory()

    def _test_view_template(self, resp_mock, template, qs=None, locale='en-US'):
        args = ['/en-US/']
        if qs is not None:
            args.append(qs)
        req = self.rf.get(*args)
        req.locale = locale
        self.view(req)
        resp_mock.assert_called_once_with(req, template, ANY)
        resp_mock.reset_mock()

    def test_uses_default_template(self, resp_mock):
        """Home page should render the default template with no QS."""
        self._test_view_template(resp_mock, 'mozorg/home.html')

    def test_uses_default_template_other_qs(self, resp_mock):
        """Home page should render the default template with wrong QS."""
        self._test_view_template(resp_mock, 'mozorg/home.html', {'a': 1})
        self._test_view_template(resp_mock, 'mozorg/home.html', {'v': 42})
        self._test_view_template(resp_mock, 'mozorg/home.html', {'v': 'Abide'})
        self._test_view_template(resp_mock, 'mozorg/home.html', {'v': '1234'})

    def test_uses_test_template(self, resp_mock):
        """Home page should render the test template with the right QS."""
        self._test_view_template(resp_mock, 'mozorg/home-b1.html', {'v': 1})
        self._test_view_template(resp_mock, 'mozorg/home-b2.html', {'v': 2})

    def test_uses_new_template_for_other_locales(self, resp_mock):
        """Should render the new template for locales not in test."""
        self._test_view_template(resp_mock, 'mozorg/home-b2.html', locale='xx')
        self._test_view_template(resp_mock, 'mozorg/home-b2.html', {'v': 2}, locale='xx')

    @override_settings(MOBILIZER_LOCALE_LINK={'es-ES': 'El Dudarino', 'de': 'Herr Dude'})
    def test_gets_right_mobilizer_url(self, resp_mock):
        """Home page should get correct mobilizer link for locale."""
        req = self.rf.get('/')
        req.locale = 'de'
        self.view(req)
        ctx = resp_mock.call_args[0][2]
        self.assertEqual(ctx['mobilizer_link'], 'Herr Dude')

    @override_settings(MOBILIZER_LOCALE_LINK={'en-US': 'His Dudeness', 'de': 'Herr Dude'})
    def test_gets_default_mobilizer_url(self, resp_mock):
        """Home page should get default mobilizer link for other locale."""
        req = self.rf.get('/')
        req.locale = 'xx'  # does not exist
        self.view(req)
        ctx = resp_mock.call_args[0][2]
        self.assertEqual(ctx['mobilizer_link'], 'His Dudeness')


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


@patch.object(l10n_utils.dotlang, 'lang_file_is_active', lambda *x: True)
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

        assert_false(mock_subscribe.called)
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

        assert_false(mock_subscribe.called)
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

        assert_false(mock_subscribe.called)
        eq_(res.status_code, 200)

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


class TestRobots(TestCase):
    @override_settings(SITE_URL='https://www.mozilla.org')
    def test_production_disallow_all_is_false(self):
        self.assertFalse(views.Robots().get_context_data()['disallow_all'])

    @override_settings(SITE_URL='http://mozilla.local')
    def test_non_production_disallow_all_is_true(self):
        self.assertTrue(views.Robots().get_context_data()['disallow_all'])

    @override_settings(SITE_URL='https://www.mozilla.org')
    def test_robots_no_redirect(self):
        response = Client().get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context_data['disallow_all'])
        self.assertEqual(response.get('Content-Type'), 'text/plain')


class TestProcessPartnershipForm(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.template = 'mozorg/partnerships.html'
        self.view = 'mozorg.partnerships'
        self.post_data = {
            'first_name': 'The',
            'last_name': 'Dude',
            'title': 'Abider of things',
            'company': 'Urban Achievers',
            'email': 'thedude@example.com',
        }
        self.invalid_post_data = {
            'first_name': 'The',
            'last_name': 'Dude',
            'title': 'Abider of things',
            'company': 'Urban Achievers',
            'email': 'thedude',
        }

        with self.activate('en-US'):
            self.url = reverse(self.view)

    def test_get(self):
        """
        A GET request should simply return a 200.
        """

        request = self.factory.get(self.url)
        request.locale = 'en-US'
        response = views.process_partnership_form(request, self.template,
                                                  self.view)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """
        POSTing without AJAX should redirect to self.url on success and
        render self.template on error.
        """

        with self.activate('en-US'):
            # test non-AJAX POST with valid form data
            request = self.factory.post(self.url, self.post_data)

            response = views.process_partnership_form(request, self.template,
                                                      self.view)

            # should redirect to success URL
            self.assertEqual(response.status_code, 302)
            self.assertIn(self.url, response._headers['location'][1])
            self.assertIn('text/html', response._headers['content-type'][1])

            # test non-AJAX POST with invalid form data
            request = self.factory.post(self.url, self.invalid_post_data)

            # locale is not getting set via self.activate above...?
            request.locale = 'en-US'

            response = views.process_partnership_form(request, self.template,
                                                      self.view)

            self.assertEqual(response.status_code, 200)
            self.assertIn('text/html', response._headers['content-type'][1])

    def test_post_ajax(self):
        """
        POSTing with AJAX should return success/error JSON.
        """

        with self.activate('en-US'):
            # test AJAX POST with valid form data
            request = self.factory.post(self.url, self.post_data,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')

            response = views.process_partnership_form(request, self.template,
                                                      self.view)

            # decode JSON response
            resp_data = simplejson.loads(response.content)

            self.assertEqual(resp_data['msg'], 'ok')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response._headers['content-type'][1],
                             'application/json')

            # test AJAX POST with invalid form data
            request = self.factory.post(self.url, self.invalid_post_data,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest')

            response = views.process_partnership_form(request, self.template,
                                                      self.view)

            # decode JSON response
            resp_data = simplejson.loads(response.content)

            self.assertEqual(resp_data['msg'], 'Form invalid')
            self.assertEqual(response.status_code, 400)
            self.assertTrue('email' in resp_data['errors'])
            self.assertEqual(response._headers['content-type'][1],
                             'application/json')
