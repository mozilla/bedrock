# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from datetime import datetime

from mock import Mock, patch
from ordereddict import OrderedDict

from bedrock.mozorg import credits
from bedrock.mozorg.tests import TestCase


class TestCredits(TestCase):
    def setUp(self):
        credits._clear_cache()

    def test_credits_list(self):
        names = credits.get_credits_list([
            'The Dude,Dude',
            'Walter Sobchak,Sobchak',
            'Theodore Donald Kerabatsos,Kerabatsos',
        ])
        self.assertListEqual(names, [
            ['The Dude', 'DUDE'],
            ['Theodore Donald Kerabatsos', 'KERABATSOS'],
            ['Walter Sobchak', 'SOBCHAK'],
        ])

    def test_credits_ordered_no_sortkey(self):
        """Should give an ordered dict or ordered lists keyed on first letter of name."""
        names = credits.get_credits_ordered([
            'Bunny Lebowski',
            'Maude Lebowski',
            'Jeffrey Lebowski',
            'Uli Kunkel',
            'The Dude',
            'Walter Sobchak',
            'Theodore Donald Kerabatsos',
        ])
        good_names = OrderedDict()
        good_names['B'] = ['Bunny Lebowski']
        good_names['J'] = ['Jeffrey Lebowski']
        good_names['M'] = ['Maude Lebowski']
        good_names['T'] = ['The Dude', 'Theodore Donald Kerabatsos']
        good_names['U'] = ['Uli Kunkel']
        good_names['W'] = ['Walter Sobchak']
        self.assertEqual(names, good_names)

    def test_credits_ordered(self):
        """Should give an ordered dict or ordered lists keyed on first letter of sortkey."""
        names = credits.get_credits_ordered([
            'Bunny Lebowski,Lebowski Bunny',
            'Maude Lebowski,Lebowski Maude',
            'Jeffrey Lebowski,Lebowski Jeffrey',
            'Uli Kunkel,Kunkel',
            'The Dude,Dude',
            'Walter Sobchak,Sobchak',
            'Theodore Donald Kerabatsos,Kerabatsos',
        ])
        good_names = OrderedDict()
        good_names['D'] = ['The Dude']
        good_names['K'] = ['Theodore Donald Kerabatsos', 'Uli Kunkel']
        good_names['L'] = ['Bunny Lebowski', 'Jeffrey Lebowski', 'Maude Lebowski']
        good_names['S'] = ['Walter Sobchak']
        self.assertEqual(names, good_names)

    def test_credits_ordered_skips(self):
        """Should skip lines with more than 2 items."""
        names = credits.get_credits_ordered([
            'Bunny Lebowski,Lebowski Bunny',
            'Maude Lebowski,Lebowski Maude',
            'Jeffrey Lebowski,Lebowski Jeffrey',
            'Karl Hungus,Karl,Inappropriate',
            'Uli Kunkel,Kunkel',
            'The Dude,Dude',
            'Walter Sobchak,Sobchak',
            'Theodore Donald Kerabatsos,Kerabatsos',
        ])
        good_names = OrderedDict()
        good_names['D'] = ['The Dude']
        good_names['K'] = ['Theodore Donald Kerabatsos', 'Uli Kunkel']
        good_names['L'] = ['Bunny Lebowski', 'Jeffrey Lebowski', 'Maude Lebowski']
        good_names['S'] = ['Walter Sobchak']
        self.assertEqual(names, good_names)

    @patch.object(credits, 'open', create=True)
    def test_credits_modified(self, open_mock):
        """Should return the modified timestamp."""
        open_mock.return_value.__enter__.return_value.read.return_value = 'The Dude abides.'
        self.assertEqual(credits.get_credits_last_modified(), 'The Dude abides.')

    @patch.object(credits, 'open', create=True)
    def test_credits_modified_read_error(self, open_mock):
        """Should return None on file read error."""
        open_mock.return_value.__enter__.return_value.read.side_effect = IOError
        self.assertIsNone(credits.get_credits_last_modified())

    @patch.object(credits, 'open', create=True)
    def test_credits_modified_datetime(self, open_mock):
        """should properly convert stored date stamp to datetime."""
        read_mock = open_mock.return_value.__enter__.return_value.read
        read_mock.return_value = 'Tue, 08 Jul 2014 12:00:00 GMT'
        good_datetime = datetime(year=2014, month=7, day=8, hour=12)
        self.assertEqual(credits.get_credits_last_modified_datetime(),
                         good_datetime)

    @patch.object(credits, 'open', create=True)
    def test_credits_modified_datetime_error(self, open_mock):
        """Should return None on error."""
        open_mock.return_value.__enter__.return_value.read.side_effect = IOError
        self.assertIsNone(credits.get_credits_last_modified_datetime())

    @patch.object(credits, 'open', create=True)
    def test_credits_modified_datetime_bad_str(self, open_mock):
        """Should return None with bad date string."""
        open_mock.return_value.__enter__.return_value.read.return_value = 'The Dude abides.'
        self.assertIsNone(credits.get_credits_last_modified_datetime())

    def test_memoize(self):
        mock = Mock()

        @credits.memoize
        def dumb_test():
            return mock('called')

        dumb_test()
        dumb_test()

        mock.assert_called_once_with('called')
        self.assertDictEqual(credits._memoize_cache,
                             {'dumb_test': mock.return_value})
