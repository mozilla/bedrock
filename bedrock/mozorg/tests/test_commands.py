# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.core.management import call_command
from django.db import IntegrityError
from django.test import override_settings

from mock import patch, DEFAULT
from pathlib2 import Path

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg.management.commands import update_product_details_files
from bedrock.mozorg.models import BlogArticle


PD_REPO_TEST_PATH = Path(__file__).parent.joinpath('test_pd_repo')
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

    @patch('bedrock.mozorg.management.commands.update_blog_feeds.BlogArticle.objects')
    def test_error_loading_feed(self, mock_manager):
        mock_manager.create.side_effect = [IntegrityError] + [None] * 4
        call_command('update_blog_feeds', articles=4)
        # 5 calls since first fails and we want 4 articles
        self.assertEqual(mock_manager.create.call_count, 5)


@override_settings(PROD_DETAILS_STORAGE='PDDatabaseStorage',
                   PROD_DETAILS_TEST_DIR=str(PD_REPO_TEST_PATH.joinpath('product-details')))
class TestUpdateProductDetailsFiles(TestCase):
    def setUp(self):
        self.command = update_product_details_files.Command()
        self.command.repo.path = PD_REPO_TEST_PATH
        self.command.repo.path_str = str(PD_REPO_TEST_PATH)

    def test_handle_diff_loads_all(self):
        with patch.multiple(self.command, update_file_data=DEFAULT, validate_data=DEFAULT,
                            file_storage=DEFAULT, load_changes=DEFAULT, repo=DEFAULT):
            options = dict(quiet=False, database='default')
            self.command.update_file_data.return_value = True
            self.command.handle(**options)
            assert self.command.file_storage.all_json_files.called
            self.command.load_changes. \
                assert_called_with(options, self.command.file_storage.all_json_files())
            assert self.command.repo.set_db_latest.called

    def test_handle_error_no_set_latest(self):
        with patch.multiple(self.command, update_file_data=DEFAULT, validate_data=DEFAULT,
                            file_storage=DEFAULT, load_changes=DEFAULT, repo=DEFAULT):
            options = dict(quiet=False, database='default')
            self.command.update_file_data.return_value = True
            self.command.load_changes.side_effect = Exception('broke yo')
            with self.assertRaises(Exception):
                self.command.handle(**options)
            assert self.command.file_storage.all_json_files.called
            self.command.load_changes.\
                assert_called_with(options, self.command.file_storage.all_json_files())
            assert not self.command.repo.set_db_latest.called

    def test_handle_no_diff_does_nothing(self):
        with patch.multiple(self.command, update_file_data=DEFAULT, validate_data=DEFAULT,
                            file_storage=DEFAULT, load_changes=DEFAULT, repo=DEFAULT):
            options = dict(quiet=False, database='default')
            self.command.update_file_data.return_value = False
            self.command.handle(**options)
            assert not self.command.file_storage.all_json_files.called
            assert not self.command.repo.set_db_latest.called
