# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from mock import Mock

from ordereddict import OrderedDict

from bedrock.mozorg import credits
from bedrock.mozorg.tests import TestCase


class TestCredits(TestCase):
    def setUp(self):
        self.credits_file = credits.CreditsFile()

    def test_credits_list(self):
        self.credits_file.readlines = Mock(return_value=[
            'The Dude,Dude',
            'Walter Sobchak,Sobchak',
            'Theodore Donald Kerabatsos,Kerabatsos',
        ])
        self.assertListEqual(self.credits_file.rows, [
            ['The Dude', 'DUDE'],
            ['Theodore Donald Kerabatsos', 'KERABATSOS'],
            ['Walter Sobchak', 'SOBCHAK'],
        ])

    def test_credits_ordered_no_sortkey(self):
        """Should give an ordered dict or ordered lists keyed on first letter of name."""
        self.credits_file.readlines = Mock(return_value=[
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
        self.assertEqual(self.credits_file.ordered, good_names)

    def test_credits_ordered(self):
        """Should give an ordered dict or ordered lists keyed on first letter of sortkey."""
        self.credits_file.readlines = Mock(return_value=[
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
        self.assertEqual(self.credits_file.ordered, good_names)

    def test_credits_ordered_skips(self):
        """Should skip lines with more than 2 items."""
        self.credits_file.readlines = Mock(return_value=[
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
        self.assertEqual(self.credits_file.ordered, good_names)
