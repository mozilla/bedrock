# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from datetime import date
import json
import basket

from django.conf import settings
from django.core import mail
from django.core.cache import cache
from django.db.utils import DatabaseError
from django.http.response import Http404
from django.test.client import RequestFactory
from django.test.utils import override_settings

from captcha.fields import ReCaptchaField
from bedrock.base.urlresolvers import reverse
from jinja2.exceptions import TemplateNotFound
from mock import ANY, Mock, patch
from nose.tools import assert_false, eq_, ok_

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg import views
from scripts import update_tableau_data


_ALL = settings.STUB_INSTALLER_ALL


class TestContributeTasks(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.view = views.ContributeTasks()

    def test_query_param(self):
        self.view.request = self.rf.get('/', {'variation': '3'})
        cxt = self.view.get_context_data()
        self.assertEqual(cxt['variation'], '3')

    def test_no_query_param(self):
        self.view.request = self.rf.get('/')
        cxt = self.view.get_context_data()
        self.assertEqual(cxt['variation'], '4')

    def test_invalid_query_param(self):
        self.view.request = self.rf.get('/', {'variation': 'dude'})
        cxt = self.view.get_context_data()
        self.assertNotIn('variation', cxt)


class TestContributeTasksSurvey(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.view = views.ContributeTasksSurvey()

    def test_query_param(self):
        self.view.request = self.rf.get('/', {'task': '3'})
        cxt = self.view.get_context_data()
        self.assertEqual(cxt['task'], '3')

    def test_no_query_param(self):
        self.view.request = self.rf.get('/')
        cxt = self.view.get_context_data()
        self.assertNotIn('task', cxt)

    def test_invalid_query_param(self):
        self.view.request = self.rf.get('/', {'task': 'dude'})
        cxt = self.view.get_context_data()
        self.assertNotIn('task', cxt)

    @patch('bedrock.mozorg.views.basket.request')
    def test_basket_data(self, basket_mock):
        req = self.rf.post('/', {
            'email': 'dude@example.com',
            'name': 'The Dude',
            'privacy': 'yes',
            'country': 'us',
        })
        resp = views.ContributeTasksSurvey.as_view()(req)
        self.assertEqual(resp.status_code, 302)
        basket_mock.assert_called_with('post', 'get-involved', {
            'email': 'dude@example.com',
            'name': 'The Dude',
            'country': 'us',
            'interest_id': 'dontknow',
            'lang': 'en-US',
            'source_url': 'http://testserver/',
        })

    @patch('bedrock.mozorg.views.basket.request')
    def test_privacy_required(self, basket_mock):
        req = self.rf.post('/', {
            'email': 'dude@example.com',
            'name': 'The Dude',
            'country': 'us',
        })
        resp = views.ContributeTasksSurvey.as_view()(req)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(basket_mock.called)

    @patch('bedrock.mozorg.views.basket.request')
    def test_basket_error(self, basket_mock):
        basket_mock.side_effect = basket.BasketException
        req = self.rf.post('/', {
            'email': 'dude@example.com',
            'name': 'The Dude',
            'privacy': 'yes',
            'country': 'us',
        })
        with self.activate('en-US'):
            resp = views.ContributeTasksSurvey.as_view()(req)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('We apologize, but an error occurred in our system.', resp.content)
        self.assertTrue(basket_mock.called)

    @patch('bedrock.mozorg.views.basket.request')
    def test_basket_email_error(self, basket_mock):
        basket_mock.side_effect = basket.BasketException(code=basket.errors.BASKET_INVALID_EMAIL)
        req = self.rf.post('/', {
            'email': 'dude@example.com',
            'name': 'The Dude',
            'privacy': 'yes',
            'country': 'us',
        })
        with self.activate('en-US'):
            resp = views.ContributeTasksSurvey.as_view()(req)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Whoops! Be sure to enter a valid email address.', resp.content)
        self.assertTrue(basket_mock.called)


class TestContributeSignup(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    @patch('lib.l10n_utils.render')
    def test_thankyou_get_proper_context(self, render_mock):
        """category added to context from querystring on thankyou."""
        view = views.ContributeSignupThankyou.as_view()

        req = self.rf.get('/thankyou/?c=thedude')
        view(req)
        render_mock.assert_called_with(req, [views.ContributeSignupThankyou.template_name],
                                       {'category': 'thedude', 'view': ANY})

        # too long
        req = self.rf.get('/thankyou/?c=thisismuchtoolongtogetintocontext')
        view(req)
        render_mock.assert_called_with(req, [views.ContributeSignupThankyou.template_name],
                                       {'view': ANY})

        # bad characters
        req = self.rf.get('/thankyou/?c=this-is-bad')
        view(req)
        render_mock.assert_called_with(req, [views.ContributeSignupThankyou.template_name],
                                       {'view': ANY})

    @patch.object(views, 'basket')
    def test_send_to_basket(self, basket_mock):
        req = self.rf.post('/', {
            'name': 'The Dude',
            'email': 'dude@example.com',
            'privacy': 'Yes',
            'category': 'dontknow',
            'country': 'us',
            'format': 'T',
        })
        req.locale = 'en-US'
        resp = views.ContributeSignup.as_view()(req)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp['location'].endswith('?c=dontknow'))
        basket_mock.request.assert_called_with('post', 'get-involved', {
            'name': 'The Dude',
            'email': 'dude@example.com',
            'interest_id': 'dontknow',
            'lang': 'en-US',
            'country': 'us',
            'message': '',
            'source_url': 'http://testserver/',
            'format': 'T',
        })

    @patch.object(views, 'basket')
    def test_invalid_form_no_basket(self, basket_mock):
        # 'coding' requires area_coding field.
        req = self.rf.post('/', {
            'name': 'The Dude',
            'email': 'dude@example.com',
            'privacy': 'Yes',
            'category': 'coding',
            'country': 'us',
        })
        resp = views.ContributeSignup.as_view()(req)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(basket_mock.called)

        # 'privacy' required
        req = self.rf.post('/', {
            'name': 'The Dude',
            'email': 'dude@example.com',
            'category': 'dontknow',
            'country': 'us',
        })
        resp = views.ContributeSignup.as_view()(req)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(basket_mock.called)

        # 'email' required
        req = self.rf.post('/', {
            'name': 'The Dude',
            'privacy': 'Yes',
            'category': 'dontknow',
            'country': 'us',
        })
        resp = views.ContributeSignup.as_view()(req)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(basket_mock.called)


@patch('bedrock.mozorg.views.l10n_utils.render')
class TestHome(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    @override_settings(MOBILIZER_LOCALE_LINK={'en-US': 'His Dudeness', 'de': 'Herr Dude'})
    def test_gets_right_mobilizer_url(self, resp_mock):
        """Home page should get correct mobilizer link for locale."""
        req = self.rf.get('/')
        req.locale = 'de'
        views.home(req)
        ctx = resp_mock.call_args[0][2]
        self.assertEqual(ctx['mobilizer_link'], 'Herr Dude')

    @override_settings(MOBILIZER_LOCALE_LINK={'en-US': 'His Dudeness', 'de': 'Herr Dude'})
    def test_gets_default_mobilizer_url(self, resp_mock):
        """Home page should get default mobilizer link for other locale."""
        req = self.rf.get('/')
        req.locale = 'xx'  # does not exist
        views.home(req)
        ctx = resp_mock.call_args[0][2]
        self.assertEqual(ctx['mobilizer_link'], 'His Dudeness')


class TestViews(TestCase):
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


class TestStudentAmbassadorsJoin(TestCase):
    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.forms.request')
    @patch('bedrock.mozorg.forms.basket.subscribe')
    def test_subscribe(self, mock_subscribe, mock_request):
        mock_subscribe.return_value = {'token': 'token-example',
                                       'status': 'ok',
                                       'created': 'True'}
        data = {'email': u'dude@example.com',
                'country': 'gr',
                'fmt': 'H',
                'first_name': 'foo',
                'last_name': 'bar',
                'status': 'teacher',
                'school': 'TuC',
                'city': 'Chania',
                'age_confirmation': 'on',
                'grad_year': '',
                'nl_about_mozilla': 'on',
                'major': '',
                'major_free_text': '',
                'privacy': 'True'}
        request_data = {'FIRST_NAME': data['first_name'],
                        'LAST_NAME': data['last_name'],
                        'STUDENTS_CURRENT_STATUS': data['status'],
                        'STUDENTS_SCHOOL': data['school'],
                        'STUDENTS_GRAD_YEAR': data['grad_year'],
                        'STUDENTS_MAJOR': data['major'],
                        'COUNTRY_': data['country'],
                        'STUDENTS_CITY': data['city'],
                        'STUDENTS_ALLOW_SHARE': 'N'}
        with self.activate('en-US'):
            self.client.post(reverse('mozorg.contribute.studentambassadors.join'), data)
        mock_subscribe.assert_called_with(
            data['email'], ['ambassadors', 'about-mozilla'], format=u'H',
            country=u'gr', source_url=u'', sync='Y',
            welcome_message='Student_Ambassadors_Welcome')
        mock_request.assert_called_with('post',
                                        'custom_update_student_ambassadors',
                                        token='token-example',
                                        data=request_data)


class TestContributeStudentAmbassadorsLanding(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.get_req = self.rf.get('/')
        self.no_exist = views.TwitterCache.DoesNotExist()
        cache.clear()

    @patch.object(views.l10n_utils, 'render')
    @patch.object(views.TwitterCache.objects, 'get')
    def test_db_exception_works(self, mock_manager, mock_render):
        """View should function properly without the DB."""
        mock_manager.side_effect = DatabaseError
        views.contribute_studentambassadors_landing(self.get_req)
        mock_render.assert_called_with(ANY, ANY, {'tweets': []})

    @patch.object(views.l10n_utils, 'render')
    @patch.object(views.TwitterCache.objects, 'get')
    def test_no_db_row_works(self, mock_manager, mock_render):
        """View should function properly without data in the DB."""
        mock_manager.side_effect = views.TwitterCache.DoesNotExist
        views.contribute_studentambassadors_landing(self.get_req)
        mock_render.assert_called_with(ANY, ANY, {'tweets': []})

    @patch.object(views.l10n_utils, 'render')
    @patch.object(views.TwitterCache.objects, 'get')
    def test_db_cache_works(self, mock_manager, mock_render):
        """View should use info returned by DB."""
        good_val = 'The Dude tweets, man.'
        mock_manager.return_value.tweets = good_val
        views.contribute_studentambassadors_landing(self.get_req)
        mock_render.assert_called_with(ANY, ANY, {'tweets': good_val})


@patch.object(views, 'lang_file_is_active', lambda *x: False)
class TestContributeOldPage(TestCase):
    def setUp(self):
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

    @patch.object(ReCaptchaField, 'clean', Mock())
    def test_with_autoresponse(self):
        """Test contacts for functional area with autoresponses"""
        self.data.update(interest='support')
        self.client.post(self.url_en, self.data)
        eq_(len(mail.outbox), 2)

        cc = ['mana@mozilla.com']
        m = mail.outbox[0]
        eq_(m.from_email, 'contribute@mozilla.org')
        eq_(m.to, ['contribute@mozilla.org'])
        eq_(m.cc, cc)
        eq_(m.extra_headers['Reply-To'], self.contact)

        m = mail.outbox[1]
        eq_(m.from_email, 'contribute@mozilla.org')
        eq_(m.to, [self.contact])
        eq_(m.cc, [])
        eq_(m.extra_headers['Reply-To'], ','.join(['contribute@mozilla.org'] +
                                                  cc))

    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.email_contribute.basket.subscribe')
    def test_webmaker_mentor_signup(self, mock_subscribe):
        """Test Webmaker Mentor signup form for education functional area"""
        self.data.update(interest='education', newsletter=True)
        self.client.post(self.url_en, self.data)

        mock_subscribe.assert_called_with(self.contact, 'mozilla-learning-network', source_url=ANY)

    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.email_contribute.basket.subscribe')
    def test_webmaker_mentor_signup_newsletter_fail(self, mock_subscribe):
        """Test Webmaker Mentor signup form when newsletter is not selected"""
        self.data.update(interest='education', newsletter=False)
        self.client.post(self.url_en, self.data)

        assert_false(mock_subscribe.called)

    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.email_contribute.basket.subscribe')
    def test_webmaker_mentor_signup_functional_area_fail(self, mock_subscribe):
        """Test Webmaker Mentor signup form when functional area is not education"""
        self.data.update(interest='coding', newsletter=True)
        self.client.post(self.url_en, self.data)

        mock_subscribe.assert_called_with(self.contact, 'about-mozilla', source_url=ANY)

    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.email_contribute.basket.subscribe')
    def test_webmaker_mentor_signup_timeout_fail(self, mock_subscribe):
        """Test Webmaker Mentor signup form when request times out"""
        mock_subscribe.side_effect = basket.BasketException
        self.data.update(interest='education', newsletter=True)
        res = self.client.post(self.url_en, self.data)

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
        eq_(m.from_email, 'contribute@mozilla.org')
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
        eq_(m.from_email, 'contribute@mozilla.org')
        eq_(m.to, ['contribute@mozilla.org'])
        eq_(m.cc, cc)
        eq_(m.extra_headers['Reply-To'], self.contact)

        m = mail.outbox[1]
        eq_(m.from_email, 'contribute@mozilla.org')
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
        STRING = u"<strong>J'adore Citröns</strong> & <Piñatas> so there"
        EXPECTED = u"J'adore Citröns &  so there"
        self.data.update(comments=STRING)
        self.client.post(self.url_en, self.data)
        eq_(len(mail.outbox), 2)
        m = mail.outbox[0]
        self.assertIn(EXPECTED, m.body)


class TestRobots(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.view = views.Robots()

    def test_production_disallow_all_is_false(self):
        self.view.request = self.rf.get('/', HTTP_HOST='www.mozilla.org')
        self.assertFalse(self.view.get_context_data()['disallow_all'])

    def test_non_production_disallow_all_is_true(self):
        self.view.request = self.rf.get('/', HTTP_HOST='www.allizom.org')
        self.assertTrue(self.view.get_context_data()['disallow_all'])

    def test_robots_no_redirect(self):
        response = self.client.get('/robots.txt', HTTP_HOST='www.mozilla.org')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context_data['disallow_all'])
        self.assertEqual(response.get('Content-Type'), 'text/plain')


class TestProcessPartnershipForm(TestCase):
    def setUp(self):
        patcher = patch('bedrock.mozorg.views.requests.post')
        self.addCleanup(patcher.stop)
        self.requests_mock = patcher.start()
        self.requests_mock.return_value.status_code = 200

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
            resp_data = json.loads(response.content)

            self.assertEqual(resp_data['msg'], 'ok')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response._headers['content-type'][1],
                             'application/json')
            ok_(self.requests_mock.called)

            # test AJAX POST with invalid form data
            request = self.factory.post(self.url, self.invalid_post_data,
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

            response = views.process_partnership_form(request, self.template,
                                                      self.view)

            # decode JSON response
            resp_data = json.loads(response.content)

            self.assertEqual(resp_data['msg'], 'Form invalid')
            self.assertEqual(response.status_code, 400)
            self.assertTrue('email' in resp_data['errors'])
            self.assertEqual(response._headers['content-type'][1],
                             'application/json')

    def test_post_ajax_honeypot(self):
        """
        POSTing with AJAX and honeypot should return success JSON.
        """
        with self.activate('en-US'):
            self.post_data['office_fax'] = 'what is this?'
            request = self.factory.post(self.url, self.post_data,
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

            response = views.process_partnership_form(request, self.template,
                                                      self.view)

            # decode JSON response
            resp_data = json.loads(response.content)

            self.assertEqual(resp_data['msg'], 'ok')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response._headers['content-type'][1],
                             'application/json')
            ok_(not self.requests_mock.called)

    def test_post_ajax_error_xss(self):
        """
        POSTing with AJAX should return sanitized error messages.
        Bug 945845.
        """
        with self.activate('en-US'):
            # test AJAX POST with valid form data
            post_data = self.post_data.copy()
            post_data['interest'] = '"><img src=x onerror=alert(1);>'
            escaped_data = '"&gt;&lt;img src=x onerror=alert(1);&gt;'
            request = self.factory.post(self.url, post_data,
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

            response = views.process_partnership_form(request, self.template,
                                                      self.view)

            # decode JSON response
            resp_data = json.loads(response.content)

            self.assertEqual(resp_data['msg'], 'Form invalid')
            self.assertEqual(response.status_code, 400)
            self.assertTrue(post_data['interest'] not in resp_data['errors']['interest'][0])
            self.assertTrue(escaped_data in resp_data['errors']['interest'][0])
            self.assertEqual(response._headers['content-type'][1],
                             'application/json')

    def test_lead_source(self):
        """
        A POST request should include the 'lead_source' field in that call. The
        value will be defaulted to 'www.mozilla.org/about/partnerships/' if it's
        not specified.
        """

        def _req(form_kwargs):
            request = self.factory.post(self.url, self.post_data)
            views.process_partnership_form(request, self.template,
                                           self.view, {}, form_kwargs)
            return self.requests_mock.call_args[0][1]['lead_source']

        eq_(_req(None), 'www.mozilla.org/about/partnerships/')
        eq_(_req({'lead_source': 'www.mozilla.org/firefox/partners/'}),
            'www.mozilla.org/firefox/partners/')


class TestMozIDDataView(TestCase):
    def setUp(self):
        with patch.object(update_tableau_data, 'get_external_data') as ged:
            ged.return_value = (
                (date(2015, 2, 2), 'Firefox', 'bugzilla', 100, 10),
                (date(2015, 2, 2), 'Firefox OS', 'bugzilla', 100, 10),
                (date(2015, 2, 9), 'Sumo', 'sumo', 100, 10),
                (date(2015, 2, 9), 'Firefox OS', 'sumo', 100, 10),
                (date(2015, 2, 9), 'QA', 'reps', 100, 10),
            )
            update_tableau_data.run()

    def _get_json(self, source):
        cache.clear()
        req = RequestFactory().get('/')
        resp = views.mozid_data_view(req, source)
        eq_(resp['content-type'], 'application/json')
        eq_(resp['access-control-allow-origin'], '*')
        return json.loads(resp.content)

    def test_all(self):
        eq_(self._get_json('all'), [
            {'wkcommencing': '2015-02-09', 'totalactive': 300, 'new': 30},
            {'wkcommencing': '2015-02-02', 'totalactive': 200, 'new': 20},
        ])

    def test_team(self):
        """When acting on a team, should just return sums for that team."""
        eq_(self._get_json('firefoxos'), [
            {'wkcommencing': '2015-02-09', 'totalactive': 100, 'new': 10},
            {'wkcommencing': '2015-02-02', 'totalactive': 100, 'new': 10},
        ])

    def test_source(self):
        """When acting on a source, should just return sums for that source."""
        eq_(self._get_json('sumo'), [
            {'wkcommencing': '2015-02-09', 'totalactive': 100, 'new': 10},
        ])

    @patch('bedrock.mozorg.models.CONTRIBUTOR_SOURCE_NAMES', {})
    def test_unknown(self):
        """An unknown source should raise a 404."""
        with self.assertRaises(Http404):
            self._get_json('does-not-exist')
