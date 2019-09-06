# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pathlib import Path

from django.test import TestCase

from fluent.runtime import FluentResourceLoader

from lib.l10n_utils import fluent


L10N_PATH = Path(__file__).with_name('test_files').joinpath('l10n')
TEST_LOADER = FluentResourceLoader(f'{L10N_PATH}/{{locale}}/')


def get_l10n(locales=None, ftl_files=None):
    locales = locales or ['de', 'en']
    ftl_files = ftl_files or ['mozorg/fluent.ftl']
    return fluent.FluentL10n(locales, ftl_files, TEST_LOADER)


class TestFluentL10n(TestCase):
    def test_localized_bundles(self):
        l10n = get_l10n()
        bundles = list(l10n._bundles())
        localized_bundles = list(l10n._localized_bundles())
        assert len(bundles) == 2
        assert len(localized_bundles) == 1
        assert localized_bundles[0].locales[0] == 'de'

    def test_localized_messages(self):
        l10n = get_l10n()
        assert len(l10n._localized_message_ids) == 3
        assert 'brand-new-string' not in l10n._localized_message_ids

    def test_has_message(self):
        l10n = get_l10n()
        assert l10n.has_message('fluent-title')
        assert not l10n.has_message('brand-new-string')

    def test_required_messages(self):
        l10n = get_l10n()
        req_messages = l10n.required_message_ids
        assert 'fluent-title' in req_messages
        assert 'fluent-page-desc' in req_messages
        assert 'fluent-header-title' not in req_messages
        assert 'brand-new-string' not in req_messages

    def test_percent_translated(self):
        l10n = get_l10n()
        assert l10n.percent_translated == 75.0

    def test_has_required_messages(self):
        l10n = get_l10n()
        assert l10n.has_required_messages
        l10n = get_l10n(['fr', 'en'])
        assert not l10n.has_required_messages


class TestFluentTranslationUtils(TestCase):
    def setUp(self):
        fluent.cache.clear()

    def test_translate(self):
        l10n = get_l10n()
        assert fluent.translate(l10n, 'fluent-title') == 'Title in German'
        # does variable substition via kwargs
        assert fluent.translate(l10n, 'fluent-page-desc', lang='Dudeish') == \
            'Description in Dudeish'
        # fall back to 'en' string
        assert fluent.translate(l10n, 'brand-new-string') == \
            'New string not yet available in all languages'
        # will use fallback string
        assert fluent.translate(l10n, 'brand-new-string', fallback='fluent-title') == 'Title in German'

    def test_has_all_messages(self):
        l10n = get_l10n()
        assert fluent.ftl_has_messages(l10n, 'fluent-title', 'fluent-page-desc')
        assert not fluent.ftl_has_messages(l10n, 'fluent-title', 'fluent-page-desc', 'brand-new-string')

    def test_has_any_messages(self):
        l10n = get_l10n()
        assert fluent.ftl_has_messages(l10n, 'fluent-title', 'brand-new-string', require_all=False)
        assert not fluent.ftl_has_messages(l10n, 'brand-new-string', require_all=False)
