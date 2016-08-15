# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from datetime import date
import json

from django.conf import settings
from django.core.cache import cache
from django.db.utils import DatabaseError
from django.http.response import Http404
from django.test.client import RequestFactory
from django.test.utils import override_settings

from captcha.fields import ReCaptchaField
from bedrock.base.urlresolvers import reverse
from mock import ANY, Mock, patch
from nose.tools import eq_, ok_

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg import views
from scripts import update_tableau_data


_ALL = settings.STUB_INSTALLER_ALL


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
    @patch('bedrock.mozorg.forms.basket.subscribe')
    def test_subscribe(self, mock_subscribe):
        mock_subscribe.return_value = {'status': 'ok'}
        data = {
            'email': u'dude@example.com',
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
            'major': 'science',
            'major_free_text': '',
            'privacy': 'True'
        }
        with self.activate('en-US'):
            self.client.post(reverse('mozorg.contribute.studentambassadors.join'), data)
        mock_subscribe.assert_called_with(
            data['email'],
            ['ambassadors', 'about-mozilla'],
            format=u'H',
            country=u'gr',
            source_url=u'',
            first_name=data['first_name'],
            last_name=data['last_name'],
            fsa_current_status=data['status'],
            fsa_school=data['school'],
            fsa_grad_year=data['grad_year'],
            fsa_major=data['major'],
            fsa_city=data['city'],
            fsa_allow_share=u'N',
        )

    @patch.object(ReCaptchaField, 'clean', Mock())
    @patch('bedrock.mozorg.forms.basket.subscribe')
    def test_subscribe_major_free_text(self, mock_subscribe):
        """Should use the major_free_text field for major if provided"""
        mock_subscribe.return_value = {'status': 'ok'}
        data = {
            'email': u'dude@example.com',
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
            'major': 'other',
            'major_free_text': 'Physical Education',
            'privacy': 'True'
        }
        with self.activate('en-US'):
            self.client.post(reverse('mozorg.contribute.studentambassadors.join'), data)
        mock_subscribe.assert_called_with(
            data['email'],
            ['ambassadors', 'about-mozilla'],
            format=u'H',
            country=u'gr',
            source_url=u'',
            first_name=data['first_name'],
            last_name=data['last_name'],
            fsa_current_status=data['status'],
            fsa_school=data['school'],
            fsa_grad_year=data['grad_year'],
            fsa_major=data['major_free_text'],
            fsa_city=data['city'],
            fsa_allow_share=u'N',
        )


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

    @patch('bedrock.mozorg.views.render_to_string',
           return_value='rendered')
    @patch('bedrock.mozorg.views.EmailMessage')
    def test_post_ajax(self, mock_email_message, mock_render_to_string):
        """
        POSTing with AJAX should return success/error JSON.
        """

        with self.activate('en-US'):
            mock_send = mock_email_message.return_value.send

            # test AJAX POST with valid form data
            request = self.factory.post(self.url, self.post_data,
                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

            response = views.process_partnership_form(request, self.template,
                                                      self.view)

            # decode JSON response
            resp_data = json.loads(response.content)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response._headers['content-type'][1],
                             'application/json')

            # make sure email was sent
            mock_send.assert_called_once_with()

            # make sure email values are correct
            mock_email_message.assert_called_once_with(
                views.PARTNERSHIPS_EMAIL_SUBJECT,
                'rendered',
                views.PARTNERSHIPS_EMAIL_FROM,
                views.PARTNERSHIPS_EMAIL_TO)

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

    @patch('bedrock.mozorg.views.render_to_string',
           return_value='rendered')
    @patch('bedrock.mozorg.views.EmailMessage')
    def test_post_ajax_honeypot(self, mock_email_message, mock_render_to_string):
        """
        POSTing with AJAX and honeypot should return success JSON.
        """
        with self.activate('en-US'):
            mock_send = mock_email_message.return_value.send

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
            ok_(not mock_send.called)

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

    @patch('bedrock.mozorg.views.render_to_string',
           return_value='rendered')
    @patch('bedrock.mozorg.views.EmailMessage')
    def test_lead_source(self, mock_email_message, mock_render_to_string):
        """
        A POST request should include the 'lead_source' field in that call. The
        value will be defaulted to 'www.mozilla.org/about/partnerships/' if it's
        not specified.
        """

        def _req(form_kwargs):
            request = self.factory.post(self.url, self.post_data)
            views.process_partnership_form(request, self.template,
                                           self.view, {}, form_kwargs)

            return str(mock_render_to_string.call_args[0][1])

        self.assertTrue('www.mozilla.org/about/partnerships/' in _req(None))
        self.assertTrue('www.mozilla.org/firefox/partners/' in
                        _req({'lead_source': 'www.mozilla.org/firefox/partners/'}))


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
