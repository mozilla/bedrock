# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.core.management import call_command
from django.db import IntegrityError
from django.test import override_settings

from mock import patch
from pathlib import Path

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg.models import BlogArticle


HACKS_FILE = Path(__file__).parent.joinpath('test_files', 'data', 'hacks-blog.xml')
TEST_BLOG_FEEDS = {
    'hacks': {
        'name': 'Hacks',
        'url': 'https://hacks.mozilla.org',
        'feed_url': str(HACKS_FILE),
    }
}


@override_settings(BLOG_FEEDS=TEST_BLOG_FEEDS)
class TestUpdateBlogFeeds(TestCase):
    def test_load_feed(self):
        call_command('update_blog_feeds', articles=4)
        self.assertEqual(BlogArticle.objects.count(), 4)

    @patch('bedrock.mozorg.management.commands.update_blog_feeds.BlogArticle')
    def test_error_loading_feed(self, mock_model):
        mock_model.objects.create.side_effect = [IntegrityError] + [None] * 4
        call_command('update_blog_feeds', articles=4)
        # 5 calls since first fails and we want 4 articles
        self.assertEqual(mock_model.objects.create.call_count, 5)
