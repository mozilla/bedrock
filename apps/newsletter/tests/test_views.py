# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import uuid

from basket import BasketException
from mock import DEFAULT, Mock, patch

from django.http import HttpResponse
from django.test.client import Client

from funfactory.urlresolvers import reverse
from mozorg.tests import TestCase
from nose.tools import ok_

from ..views import existing


# Test data for newsletters
# In the format returned by utils.get_newsletters()
newsletters = {
    u'mozilla-and-you': {
        'title': "Firefox & You",
        'languages': ['en', 'fr', 'de', 'pt', 'ru'],
        'show': True,
        'description': 'Firefox and you'
    },
    u'firefox-tips': {
        'show': True,
        'title': 'Firefox Tips',
        'languages': ['en', 'fr', 'de', 'pt', 'ru'],
        'description': 'Firefox tips',
    },
    u'beta': {
        'show': False,
        'title': 'Beta News',
        'languages': ['en'],
        'description': 'Beta News',
    },
    u'join-mozilla': {
        'show': False,
        'title': 'Join Mozilla',
        'languages': ['en'],
        'description': 'Join Mozilla',
    },
}


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


# Always mock basket.request to be sure we never actually call basket
# during tests.
@patch('basket.base.request')
class TestExistingNewsletterView(TestCase):
    def setUp(self):
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
        self.request = Mock(method='GET', locale='en-US', REQUEST={})
        super(TestExistingNewsletterView, self).setUp()

    @patch('newsletter.utils.get_newsletters')
    def test_get_token(self, get_newsletters, mock_basket_request):
        # If user gets page with valid token in their URL, they
        # see their data, and no privacy checkbox is presented
        get_newsletters.return_value = newsletters
        self.request.method = 'GET'
        # noinspection PyUnresolvedReferences
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('l10n_utils.render') as render:
                basket_patches['user'].return_value = self.user
                render.return_value = HttpResponse()
                existing(self.request, token=self.token)
        request, template_name, context = render.call_args[0]
        form = context['form']
        self.assertNotIn('privacy', form.fields)
        self.assertEqual(self.user['lang'], form.initial['lang'])

    @patch('newsletter.utils.get_newsletters')
    def test_show(self, get_newsletters, mock_basket_request):
        # Newsletters are only listed if the user is subscribed to them,
        # or they are marked 'show' in the settings
        get_newsletters.return_value = newsletters
        self.request.method = 'GET'
        # Find a newsletter without 'show' and subscribe the user to it
        for newsletter, data in newsletters.iteritems():
            if not data.get('show', False):
                self.user['newsletters'] = [newsletter]
                break
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('l10n_utils.render') as render:
                basket_patches['user'].return_value = self.user
                render.return_value = HttpResponse()
                existing(self.request, token=self.token)
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

    @patch('newsletter.utils.get_newsletters')
    def test_english_only(self, get_newsletters, mock_basket_request):
        # English-only newsletters are flagged in the forms passed to
        # the template.
        get_newsletters.return_value = newsletters
        self.request.method = 'GET'
        # Subscribe to them all
        self.user['newsletters'] = newsletters.keys()
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('l10n_utils.render') as render:
                basket_patches['user'].return_value = self.user
                render.return_value = HttpResponse()
                existing(self.request, token=self.token)
        request, template_name, context = render.call_args[0]
        forms = context['formset'].initial_forms

        for form in forms:
            newsletter = newsletters[form.initial['newsletter']]
            if form.initial['english_only']:
                self.assertEqual(['en'], newsletter['languages'])
            else:
                self.assertNotEqual(['en'], newsletter['languages'])

    @patch('newsletter.utils.get_newsletters')
    def test_get_no_token(self, get_newsletters, mock_basket_request):
        # If user gets page with no valid token in their URL, they
        # see an error message and that's about it
        get_newsletters.return_value = newsletters
        self.request.method = 'GET'
        # noinspection PyUnresolvedReferences
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT):
            with patch('l10n_utils.render') as render:
                render.return_value = HttpResponse()
                existing(self.request)
        request, template_name, context = render.call_args[0]
        self.assertNotIn('form', context)

    def test_user_not_found(self, mock_basket_request):
        # User passed token, but no user was found
        self.request.method = 'POST'
        self.request.POST = self.data
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('l10n_utils.render') as render:
                with patch('django.contrib.messages.add_message') as add_msg:
                    basket_patches['user'].side_effect = BasketException
                    render.return_value = HttpResponse()
                    existing(self.request, token='no such user')
        # Shouldn't call basket except for the attempt to find the user
        self.assertEqual(0, basket_patches['update_user'].call_count)
        self.assertEqual(0, basket_patches['unsubscribe'].call_count)
        self.assertEqual(0, basket_patches['subscribe'].call_count)
        # Should have given a message
        self.assertEqual(1, add_msg.call_count,
                         msg=repr(add_msg.call_args_list))

    @patch('newsletter.utils.get_newsletters')
    def test_subscribing(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        self.request.method = 'POST'
        # They subscribe to firefox-tips
        self.data['form-2-subscribed'] = u'True'
        # in English - and that's their language too
        self.user['lang'] = u'en'
        self.data['lang'] = u'en'
        self.request.POST = self.data
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('django.contrib.messages.add_message') as add_msg:
                with patch('l10n_utils.render'):
                    basket_patches['user'].return_value = self.user
                    rsp = existing(self.request, token=self.token)
        # Should have given some messages
        self.assertEqual(1, add_msg.call_count,
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
        # Should redirect to the 'updated' view with no parms
        url = reverse('newsletter.updated')
        self.assertEqual(url, rsp['Location'])

    @patch('newsletter.utils.get_newsletters')
    def test_unsubscribing(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        self.request.method = 'POST'
        # They unsubscribe from the one newsletter they're subscribed to
        self.data['form-0-subscribed'] = u'False'
        self.request.POST = self.data
        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('l10n_utils.render'):
                basket_patches['user'].return_value = self.user
                rsp = existing(self.request, token=self.token)
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
        self.assertEqual(url, rsp['Location'])

    @patch('newsletter.utils.get_newsletters')
    def test_remove_all(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        self.request.method = 'POST'
        self.data['remove_all'] = 'on'   # any value should do
        self.request.POST = self.data

        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            unsubscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('l10n_utils.render'):
                basket_patches['user'].return_value = self.user
                rsp = existing(self.request, token=self.token)
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
        self.assertEqual(url, rsp['Location'])

    @patch('newsletter.utils.get_newsletters')
    def test_change_lang_country(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        self.request.method = 'POST'
        self.data['lang'] = 'en'
        self.data['country'] = 'us'
        self.request.POST = self.data

        with patch.multiple('basket',
                            update_user=DEFAULT,
                            subscribe=DEFAULT,
                            user=DEFAULT) as basket_patches:
            with patch('l10n_utils.render'):
                with patch('django.contrib.messages.add_message') as add_msg:
                    basket_patches['user'].return_value = self.user
                    rsp = existing(self.request, token=self.token)

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
        # One message should be emitted
        self.assertEqual(1, add_msg.call_count,
                         msg=repr(add_msg.call_args_list))
        # Should redirect to the 'updated' view
        url = reverse('newsletter.updated')
        self.assertEqual(url, rsp['Location'])
