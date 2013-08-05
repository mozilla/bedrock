# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import uuid
from bedrock.newsletter.views import unknown_address_text, recovery_text

from django.http import HttpResponse
from django.test.client import Client

from mock import DEFAULT, patch
from nose.tools import ok_

from basket import BasketException
from bedrock.mozorg.tests import TestCase
from bedrock.newsletter.utils import clear_caches
from funfactory.urlresolvers import reverse


# Test data for newsletters
# In the format returned by utils.get_newsletters()
newsletters = {
    u'mozilla-and-you': {
        'title': "Firefox & You",
        'languages': ['en', 'fr', 'de', 'pt', 'ru'],
        'show': True,
        'description': 'Firefox and you',
        'order': 4,
    },
    u'firefox-tips': {
        'show': True,
        'title': 'Firefox Tips',
        'languages': ['en', 'fr', 'de', 'pt', 'ru'],
        'description': 'Firefox tips',
        'order': 2,
    },
    u'beta': {
        'show': False,
        'title': 'Beta News',
        'languages': ['en'],
        'description': 'Beta News',
        'order': 3,
    },
    u'join-mozilla': {
        'show': False,
        'title': 'Join Mozilla',
        'languages': ['en'],
        'description': 'Join Mozilla',
        'order': 1,
    },
}


def assert_redirect(response, url):
    """
    Assert that the response indicates a redirect to the url.
    """
    # This is like Django TestCase's assertRedirect, only we're not
    # using Django TestCase due to our lack of a database, so we
    # need to fake our own.

    # Django seems to stick this into the Location header
    url = "http://testserver" + url
    assert url == response['Location'],\
        "Response did not redirect to %s; Location=%s" % \
        (url, response['Location'])


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        clear_caches()

    def test_hacks_newsletter_frames_allow(self):
        """
        Bedrock pages get the 'x-frame-options: DENY' header by default.
        The hacks newsletter page is framed, so needs to ALLOW.
        """
        with self.activate('en-US'):
            resp = self.client.get(reverse('mozorg.hacks_newsletter'))

        ok_('x-frame-options' not in resp)


# Always mock basket.request to be sure we never actually call basket
# during tests.
@patch('basket.base.request')
class TestExistingNewsletterView(TestCase):
    def setUp(self):
        self.client = Client()
        self.token = unicode(uuid.uuid4())
        self.user = {
            'newsletters': [u'mozilla-and-you'],
            'token': self.token,
            'email': u'user@example.com',
            'lang': u'pt',
            'country': u'br',
            'format': u'T',
        }
        # By default, data matches user's existing data; change it
        # in the test as desired. Also, user has accepted privacy
        # checkbox.
        self.data = {
            u'form-MAX_NUM_FORMS': 5,
            u'form-INITIAL_FORMS': 5,
            u'form-TOTAL_FORMS': 5,
            u'email': self.user['email'],
            u'lang': self.user['lang'],
            u'country': self.user['country'],
            u'format': self.user['format'],
            u'privacy': u'on',
            u'form-0-subscribed': u'True',
            u'form-0-newsletter': u'mozilla-and-you',
            u'form-1-subscribed': u'False',
            u'form-1-newsletter': u'mobile',
            u'form-2-newsletter': u'firefox-tips',
            u'form-2-subscribed': u'False',
            u'form-3-subscribed': u'False',
            u'form-3-newsletter': u'beta',
            u'form-4-newsletter': u'join-mozilla',
            u'form-4-subscribed': u'False',
            u'submit': u'Save Preferences',
        }
        clear_caches()
        super(TestExistingNewsletterView, self).setUp()

    @patch('bedrock.newsletter.utils.get_newsletters')
    def test_get_token(self, get_newsletters, mock_basket_request):
        # If user gets page with valid token in their URL, they
        # see their data, and no privacy checkbox is presented
        get_newsletters.return_value = newsletters
        url = reverse('newsletter.existing.token', args=(self.token,))
        # noinspection PyUnresolvedReferences
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('lib.l10n_utils.render') as render:
                basket_patches['user'].return_value = self.user
                render.return_value = HttpResponse('')
                self.client.get(url)
        request, template_name, context = render.call_args[0]
        form = context['form']
        self.assertNotIn('privacy', form.fields)
        self.assertEqual(self.user['lang'], form.initial['lang'])

    @patch('bedrock.newsletter.utils.get_newsletters')
    def test_show(self, get_newsletters, mock_basket_request):
        # Newsletters are only listed if the user is subscribed to them,
        # or they are marked 'show' in the settings
        get_newsletters.return_value = newsletters
        # Find a newsletter without 'show' and subscribe the user to it
        for newsletter, data in newsletters.iteritems():
            if not data.get('show', False):
                self.user['newsletters'] = [newsletter]
                break
        url = reverse('newsletter.existing.token', args=(self.token,))
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('lib.l10n_utils.render') as render:
                basket_patches['user'].return_value = self.user
                render.return_value = HttpResponse('')
                self.client.get(url)
        request, template_name, context = render.call_args[0]
        forms = context['formset'].initial_forms

        shown = set([form.initial['newsletter'] for form in forms])
        to_show = set([newsletter for newsletter, data
                       in newsletters.iteritems()
                       if data.get('show', False)])
        subscribed = set(self.user['newsletters'])

        # All subscribed newsletters are shown
        self.assertEqual(set(), subscribed - shown)
        # All 'show' newsletters are shown
        self.assertEqual(set(), to_show - shown)
        # No other newsletters are shown
        self.assertEqual(set(), shown - subscribed - to_show)

    def test_get_no_token(self, mock_basket_request):
        # No token in URL - should redirect to recovery
        url = reverse('newsletter.existing.token', args=('',))
        rsp = self.client.get(url)
        self.assertEqual(302, rsp.status_code)
        self.assertTrue(rsp['Location'].endswith(reverse('newsletter.recovery')))

    def test_get_user_not_found(self, mock_basket_request):
        # Token in URL but not a valid token - should redirect to recovery
        rand_token = unicode(uuid.uuid4())
        url = reverse('newsletter.existing.token', args=(rand_token,))
        with patch.multiple('basket',
                            user=DEFAULT) as basket_patches:
            with patch('lib.l10n_utils.render') as render:
                render.return_value = HttpResponse('')
                with patch('django.contrib.messages.add_message') as add_msg:
                    basket_patches['user'].side_effect = BasketException
                    rsp = self.client.get(url)
        # Should have given a message
        self.assertEqual(1, add_msg.call_count,
                         msg=repr(add_msg.call_args_list))
        # Should have been redirected to recovery page
        self.assertEqual(302, rsp.status_code)
        self.assertTrue(rsp['Location'].endswith(reverse('newsletter.recovery')))

    def test_invalid_token(self, mock_basket_request):
        # "Token" in URL is not syntactically a UUID - should redirect to
        # recovery *without* calling Exact Target
        token = "not a token"
        url = reverse('newsletter.existing.token', args=(token,))
        with patch.multiple('basket', user=DEFAULT) as basket_patches:
            with patch('django.contrib.messages.add_message') as add_msg:
                rsp = self.client.get(url, follow=False)
        self.assertEqual(0, basket_patches['user'].call_count)
        self.assertEqual(1, add_msg.call_count)
        self.assertEqual(302, rsp.status_code)
        self.assertTrue(rsp['Location'].endswith(reverse('newsletter.recovery')))

    def test_post_user_not_found(self, mock_basket_request):
        # User submits form and passed token, but no user was found
        # Should issue message and redirect to recovery
        rand_token = unicode(uuid.uuid4())
        url = reverse('newsletter.existing.token', args=(rand_token,))
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('lib.l10n_utils.render') as render:
                render.return_value = HttpResponse('')
                with patch('django.contrib.messages.add_message') as add_msg:
                    basket_patches['user'].side_effect = BasketException
                    rsp = self.client.post(url, self.data)
        # Shouldn't call basket except for the attempt to find the user
        self.assertEqual(0, basket_patches['update_user'].call_count)
        self.assertEqual(0, basket_patches['unsubscribe'].call_count)
        self.assertEqual(0, basket_patches['subscribe'].call_count)
        # Should have given a message
        self.assertEqual(1, add_msg.call_count,
                         msg=repr(add_msg.call_args_list))
        # Should have been redirected to recovery page
        self.assertEqual(302, rsp.status_code)
        self.assertTrue(rsp['Location'].endswith(reverse('newsletter.recovery')))

    @patch('bedrock.newsletter.utils.get_newsletters')
    def test_subscribing(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        # They subscribe to firefox-tips
        self.data['form-2-subscribed'] = u'True'
        # in English - and that's their language too
        self.user['lang'] = u'en'
        self.data['lang'] = u'en'
        url = reverse('newsletter.existing.token', args=(self.token,))
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('django.contrib.messages.add_message') as add_msg:
                with patch('lib.l10n_utils.render'):
                    basket_patches['user'].return_value = self.user
                    rsp = self.client.post(url, self.data)
        # Should have given no messages
        self.assertEqual(0, add_msg.call_count,
                         msg=repr(add_msg.call_args_list))
        # Should have called update_user with subscription list
        self.assertEqual(1, basket_patches['update_user'].call_count)
        kwargs = basket_patches['update_user'].call_args[1]
        self.assertEqual(
            {'newsletters': u'mozilla-and-you,firefox-tips'},
            kwargs
        )
        # Should not have called unsubscribe
        self.assertEqual(0, basket_patches['unsubscribe'].call_count)
        # Should not have called subscribe
        self.assertEqual(0, basket_patches['subscribe'].call_count)
        # Should redirect to the 'updated' view
        url = reverse('newsletter.updated')
        assert_redirect(rsp, url)

    @patch('bedrock.newsletter.utils.get_newsletters')
    def test_unsubscribing(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        # They unsubscribe from the one newsletter they're subscribed to
        self.data['form-0-subscribed'] = u'False'
        url = reverse('newsletter.existing.token', args=(self.token,))
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('lib.l10n_utils.render'):
                basket_patches['user'].return_value = self.user
                rsp = self.client.post(url, self.data)
        # Should have called update_user with list of newsletters
        self.assertEqual(1, basket_patches['update_user'].call_count)
        kwargs = basket_patches['update_user'].call_args[1]
        self.assertEqual(
            {'newsletters': u''},
            kwargs
        )
        # Should not have called subscribe
        self.assertEqual(0, basket_patches['subscribe'].call_count)
        # Should not have called unsubscribe
        self.assertEqual(0, basket_patches['unsubscribe'].call_count)
        # Should redirect to the 'updated' view
        url = reverse('newsletter.updated')
        assert_redirect(rsp, url)

    @patch('bedrock.newsletter.utils.get_newsletters')
    def test_remove_all(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        self.data['remove_all'] = 'on'   # any value should do

        url = reverse('newsletter.existing.token', args=(self.token,))
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('lib.l10n_utils.render'):
                basket_patches['user'].return_value = self.user
                rsp = self.client.post(url, self.data)
        # Should not have updated user details at all
        self.assertEqual(0, basket_patches['update_user'].call_count)
        # Should have called unsubscribe
        self.assertEqual(1, basket_patches['unsubscribe'].call_count)
        # and said user opts out
        args, kwargs = basket_patches['unsubscribe'].call_args
        self.assertEqual((self.token, self.user['email']), args)
        self.assertTrue(kwargs['optout'])
        # Should redirect to the 'updated' view with unsub=1 and token
        url = reverse('newsletter.updated') + "?unsub=1"
        url += "&token=%s" % self.token
        assert_redirect(rsp, url)

    @patch('bedrock.newsletter.utils.get_newsletters')
    def test_change_lang_country(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        self.data['lang'] = 'en'
        self.data['country'] = 'us'

        url = reverse('newsletter.existing.token', args=(self.token,))
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('lib.l10n_utils.render'):
                with patch('django.contrib.messages.add_message') as add_msg:
                    basket_patches['user'].return_value = self.user
                    rsp = self.client.post(url, self.data)

        # We have an existing user with a change to their email data,
        # but none to their subscriptions.
        # 'subscribe' should not be called
        self.assertEqual(0, basket_patches['subscribe'].call_count)
        # update_user should be called once
        self.assertEqual(1, basket_patches['update_user'].call_count)
        # with the new lang and country and the newsletter list
        kwargs = basket_patches['update_user'].call_args[1]
        self.assertEqual(
            {'lang': u'en',
             'country': u'us',
             'newsletters': u'mozilla-and-you'},
            kwargs
        )
        # No messages should be emitted
        self.assertEqual(0, add_msg.call_count,
                         msg=repr(add_msg.call_args_list))
        # Should redirect to the 'updated' view
        url = reverse('newsletter.updated')
        assert_redirect(rsp, url)

    @patch('bedrock.newsletter.utils.get_newsletters')
    def test_newsletter_ordering(self, get_newsletters, mock_basket_request):
        # Newsletters are listed in 'order' order, if they have an 'order'
        # field
        get_newsletters.return_value = newsletters
        url = reverse('newsletter.existing.token', args=(self.token,))
        self.user['newsletters'] = [u'mozilla-and-you', u'firefox-tips',
                                    u'beta']
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('lib.l10n_utils.render') as render:
                basket_patches['user'].return_value = self.user
                render.return_value = HttpResponse('')
                self.client.get(url)
        request, template_name, context = render.call_args[0]
        forms = context['formset'].initial_forms

        newsletters_in_order = [form.initial['newsletter'] for form in forms]
        self.assertEqual([u'firefox-tips', u'beta', u'mozilla-and-you'],
                         newsletters_in_order)

    @patch('bedrock.newsletter.utils.get_newsletters')
    def test_newsletter_no_order(self, get_newsletters, mock_basket_request):
        """Newsletter views should work if we get no order from basket."""
        orderless_newsletters = {}
        for key, val in newsletters.items():
            nl_copy = val.copy()
            del nl_copy['order']
            orderless_newsletters[key] = nl_copy

        get_newsletters.return_value = orderless_newsletters
        url = reverse('newsletter.existing.token', args=(self.token,))
        self.user['newsletters'] = [u'mozilla-and-you', u'firefox-tips',
                                    u'beta']
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('lib.l10n_utils.render') as render:
                basket_patches['user'].return_value = self.user
                render.return_value = HttpResponse('')
                self.client.get(url)
        request, template_name, context = render.call_args[0]
        forms = context['formset'].initial_forms

        newsletters_in_order = [form.initial['newsletter'] for form in forms]
        self.assertEqual([u'beta', u'mozilla-and-you', u'firefox-tips'],
                         newsletters_in_order)


class TestConfirmView(TestCase):
    def setUp(self):
        self.token = unicode(uuid.uuid4())
        self.url = reverse('newsletter.confirm', kwargs={'token': self.token})
        self.client = Client()
        clear_caches()

    def test_normal(self):
        """Confirm works with a valid token"""
        with patch('basket.confirm') as confirm:
            confirm.return_value = {'status': 'ok'}
            with patch('lib.l10n_utils.render') as mock_render:
                mock_render.return_value = HttpResponse('')
                rsp = self.client.get(self.url, follow=True)
            self.assertEqual(200, rsp.status_code)
            confirm.assert_called_with(self.token)
            context = mock_render.call_args[0][2]
            self.assertTrue(context['success'])
            self.assertFalse(context['generic_error'])
            self.assertFalse(context['token_error'])

    def test_basket_down(self):
        """If basket is down, we report the appropriate error"""
        with patch('basket.confirm') as confirm:
            confirm.side_effect = BasketException()
            with patch('lib.l10n_utils.render') as mock_render:
                mock_render.return_value = HttpResponse('')
                rsp = self.client.get(self.url, follow=True)
            self.assertEqual(200, rsp.status_code)
            confirm.assert_called_with(self.token)
            context = mock_render.call_args[0][2]
            self.assertFalse(context['success'])
            self.assertTrue(context['generic_error'])
            self.assertFalse(context['token_error'])

    def test_bad_token(self):
        """If the token is bad, we report the appropriate error"""
        with patch('basket.confirm') as confirm:
            confirm.side_effect = BasketException(status_code=403)
            with patch('lib.l10n_utils.render') as mock_render:
                mock_render.return_value = HttpResponse('')
                rsp = self.client.get(self.url, follow=True)
            self.assertEqual(200, rsp.status_code)
            confirm.assert_called_with(self.token)
            context = mock_render.call_args[0][2]
            self.assertFalse(context['success'])
            self.assertFalse(context['generic_error'])
            self.assertTrue(context['token_error'])


class TestRecoveryView(TestCase):
    def setUp(self):
        self.url = reverse('newsletter.recovery')
        self.client = Client()

    def test_bad_email(self):
        """Email syntax errors are caught"""
        data = {'email': 'not_an_email'}
        rsp = self.client.post(self.url, data)
        self.assertEqual(200, rsp.status_code)
        self.assertIn('email', rsp.context['form'].errors)

    @patch('basket.send_recovery_message', autospec=True)
    def test_unknown_email(self, mock_basket):
        """Unknown email addresses give helpful error message"""
        data = {'email': 'unknown@example.com'}
        mock_basket.side_effect = BasketException(status_code=404)
        rsp = self.client.post(self.url, data)
        self.assertTrue(mock_basket.called)
        self.assertEqual(200, rsp.status_code)
        form = rsp.context['form']
        expected_error = unknown_address_text % \
            reverse('newsletter.mozilla-and-you')
        self.assertIn(expected_error, form.errors['email'])

    @patch('django.contrib.messages.add_message', autospec=True)
    @patch('basket.send_recovery_message', autospec=True)
    def test_good_email(self, mock_basket, add_msg):
        """If basket returns success, don't report errors"""
        data = {'email': 'known@example.com'}
        mock_basket.return_value = {'status': 'ok'}
        rsp = self.client.post(self.url, data)
        self.assertTrue(mock_basket.called)
        # On successful submit, we redirect
        self.assertEqual(302, rsp.status_code)
        rsp = self.client.get(rsp['Location'])
        self.assertEqual(200, rsp.status_code)
        self.assertFalse(rsp.context['form'])
        # We also give them a success message
        self.assertEqual(1, add_msg.call_count,
                         msg=repr(add_msg.call_args_list))
        self.assertIn(recovery_text, add_msg.call_args[0])
