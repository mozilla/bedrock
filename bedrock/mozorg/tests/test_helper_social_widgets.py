# coding: utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os.path

from django.test.client import RequestFactory

import tweepy

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg.templatetags.social_widgets import *  # noqa


TEST_FILES_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'test_files')


class TestFormatTweet(TestCase):
    rf = RequestFactory()

    with open(os.path.join(TEST_FILES_ROOT, 'data', 'tweets.json')) as file:
        tweets = json.load(file)

    # For test, select and parse a tweet containing a hashtag, mention and URL
    tweet = tweepy.models.Status.parse(tweepy.api, tweets[5])

    def test_format_tweet_body(self):
        """Should return a tweet in an HTML format"""
        # Note that … is a non-ASCII character. That's why the UTF-8 encoding is
        # specified at the top of the file.
        actual = format_tweet_body(self.tweet)
        expected = (
            u'Want more information about the <a href="https://twitter.com/'
            u'mozstudents" class="mention">@mozstudents</a> program? Sign-up '
            u'and get a monthly newsletter in your in-box <a href="http://t.co/'
            u'0thqsyksC3" title="http://www.mozilla.org/en-US/contribute/'
            u'universityambassadors/">mozilla.org/en-US/contribu…</a> <a href='
            u'"https://twitter.com/search?q=%23oto%C3%B1o&amp;src=hash" class='
            u'"hash">#otoño</a>')
        self.assertEqual(actual, expected)

    def test_format_tweet_timestamp(self):
        """Should return a timestamp in an HTML format"""
        expected = (
            u'<time datetime="2014-01-16T19:28:24" title="2014-01-16 19:28" '
            u'itemprop="dateCreated">16 Jan <span class="full">(2014-01-16 '
            u'19:28)</span></time>')
        self.assertEqual(format_tweet_timestamp(self.tweet), expected)
