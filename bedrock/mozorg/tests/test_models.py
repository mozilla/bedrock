# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.cache import cache
from django.db.utils import DatabaseError
from django.db.models.signals import post_save

from mock import patch

from bedrock.mozorg.models import TwitterCache
from bedrock.mozorg.tests import TestCase


@patch.object(TwitterCache.objects, 'get')
class TestTwitterCacheManager(TestCase):
    def setUp(self):
        cache.clear()

    def test_results_cached(self, get_mock):
        """Results from get_tweets_for() should be cached."""
        get_mock.return_value.tweets = ['dude']

        tweets = TwitterCache.objects.get_tweets_for('dude')
        self.assertEqual(['dude'], tweets)

        tweets = TwitterCache.objects.get_tweets_for('dude')
        self.assertEqual(['dude'], tweets)

        get_mock.assert_called_once_with(account='dude')

        get_mock.return_value.tweets = ['donny']

        tweets = TwitterCache.objects.get_tweets_for('donny')
        self.assertEqual(['donny'], tweets)

        tweets = TwitterCache.objects.get_tweets_for('donny')
        self.assertEqual(['donny'], tweets)

        self.assertEqual(get_mock.call_count, 2)

    def test_errors_fail_silently(self, get_mock):
        """Errors should return an empty list"""
        get_mock.side_effect = TwitterCache.DoesNotExist
        self.assertEqual(TwitterCache.objects.get_tweets_for('dude'), [])
        self.assertEqual(TwitterCache.objects.get_tweets_for('dude'), [])

        # and even errors should be cached
        get_mock.assert_called_once_with(account='dude')

        get_mock.reset_mock()
        get_mock.side_effect = DatabaseError
        self.assertEqual(TwitterCache.objects.get_tweets_for('walter'), [])
        self.assertEqual(TwitterCache.objects.get_tweets_for('walter'), [])

        # and even errors should be cached
        get_mock.assert_called_once_with(account='walter')

    @patch('bedrock.mozorg.models.cache_tweets')
    def test_cache_post_save(self, mock_cache_tweets, get_mock):
        post_save.send(TwitterCache,
                       instance=TwitterCache(account='me', tweets=['I twote']))
        mock_cache_tweets.assert_called_once_with('me', ['I twote'])
