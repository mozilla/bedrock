# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.test import TestCase

from lib.l10n_utils.management.commands import _fluent


class TestTrans(TestCase):
    def test_trans(self):
        input = """
        {% trans %}
        Just some text
        {% endtrans %}

        {% trans one='value' , two=url('privacy.notices.firefox') %}
        There's {{one}} and
        {{ two  }} things to check here.
        {%  endtrans  %}
        """
        lang_strings = []
        for trans_match in _fluent.TRANS_BLOCK_RE.finditer(input):
            lang_strings.append(_fluent.trans_to_lang(trans_match["string"]))
        assert len(lang_strings) == 2
        assert lang_strings[0] == "Just some text"
        assert lang_strings[1] == "There's %(one)s and %(two)s things to check here."
