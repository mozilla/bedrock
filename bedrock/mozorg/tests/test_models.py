# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.cache import cache
from django.db.utils import DatabaseError
from django.db.models.signals import post_save
from django.test import override_settings

from mock import patch
from pathlib2 import Path

from bedrock.mozorg.models import BlogArticle, TwitterCache
from bedrock.mozorg.tests import TestCase


HACKS_FILE = Path(__file__).parent.joinpath('test_files', 'data', 'hacks-blog.xml')
TEST_BLOG_FEEDS = {
    'hacks': {
        'name': 'Hacks',
        'url': 'https://hacks.mozilla.org',
        'feed_url': str(HACKS_FILE),
    }
}


@override_settings(BLOG_FEEDS=TEST_BLOG_FEEDS)
class TestBlogArticle(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestBlogArticle, cls).setUpClass()
        BlogArticle.update_feeds(num_articles=4)

    def test_htmlify(self):
        a = BlogArticle.objects.first()
        self.assertNotIn('Continue reading', a.htmlify())

    def test_ordering(self):
        a = BlogArticle.objects.first()
        self.assertEqual(a.link, 'https://hacks.mozilla.org/2016/09/firefox-49-fixes-'
                                 'sites-designed-with-webkit-in-mind-and-more/')

    def test_blog_link(self):
        a = BlogArticle.objects.first()
        self.assertEqual(a.blog_link, TEST_BLOG_FEEDS['hacks']['url'])

    def test_parse_feed(self):
        feed = BlogArticle.parse_feed('dude', {
            'feed_url': str(HACKS_FILE),
            'name': 'The Dude Feeds',
        })
        self.assertEqual(feed.mozorg_feed_id, 'dude')
        self.assertEqual(feed.mozorg_feed_name, 'The Dude Feeds')

    @patch('bedrock.mozorg.models.parse')
    def test_parse_feed_no_feed_url(self, parse_mock):
        BlogArticle.parse_feed('dude', {
            'url': 'https://example.com',
            'name': 'The Dude Feeds',
        })
        parse_mock.assert_called_with('https://example.com/feed/atom/')


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
