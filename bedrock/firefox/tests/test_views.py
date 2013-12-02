# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.test.client import RequestFactory

from mock import patch
from nose.tools import eq_
from rna.models import Release

from bedrock.firefox import views
from bedrock.firefox.tests import NoteFactory, ProductFactory, ReleaseFactory
from bedrock.mozorg.tests import TestCase


class TestReleaseNotesView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        self.render_patch = patch('bedrock.firefox.views.l10n_utils.render')
        self.mock_render = self.render_patch.start()

    def tearDown(self):
        self.render_patch.stop()

    @property
    def last_ctx(self):
        """
        Convenient way to access the context of the last rendered
        response.
        """
        return self.mock_render.call_args[0][2]

    def test_missing_minor_version(self):
        """
        If the minor version is missing in the URL, it should default to
        0.
        """
        ReleaseFactory.create(version=18, sub_version=0, channel__name='Release',
                              product__name='Firefox')

        views.release_notes(self.request, '18.0')
        eq_(self.last_ctx['minor_version'], 0)

    def test_no_release_404(self):
        """
        Fetch the release using get_object_or_404, so that an Http404 is
        raised when the release isn't found.
        """
        with patch('bedrock.firefox.views.get_object_or_404') as get_object_or_404:
            views.release_notes(self.request, '18.0')
            eq_(self.last_ctx['release'], get_object_or_404.return_value)
            get_object_or_404.assert_called_with(Release, version=18, sub_version=0,
                                                 channel__name='Release', product__name='Firefox')

    def test_note_first_version_not_fixed(self):
        """
        If a note started on or before the current version, and has yet
        to be fixed, include it in known issues.
        """
        product = ProductFactory.create(name='Firefox')
        ReleaseFactory.create(version=19, sub_version=0, channel__name='Release', product=product)
        note1 = NoteFactory.create(first_version=18, fixed_in_version=None, product=product)
        note2 = NoteFactory.create(first_version=19, fixed_in_version=None, product=product)

        views.release_notes(self.request, '19.0')
        eq_(set([note1, note2]), set(self.last_ctx['known_issues']))

    def test_note_first_version_fixed(self):
        """
        If a note started on or before the current version, and was
        fixed on this version, include it in new features. If it was
        fixed after this version, include it in known issues.
        """
        product = ProductFactory.create(name='Firefox')
        ReleaseFactory.create(version=19, sub_version=0, channel__name='Release', product=product)
        note1 = NoteFactory.create(first_version=18, fixed_in_version=19, product=product)
        note2 = NoteFactory.create(first_version=19, fixed_in_version=19, product=product)
        note3 = NoteFactory.create(first_version=18, fixed_in_version=20, product=product)
        note4 = NoteFactory.create(first_version=19, fixed_in_version=20, product=product)

        views.release_notes(self.request, '19.0')
        eq_(set([note1, note2]), set(self.last_ctx['new_features']))
        eq_(set([note3, note4]), set(self.last_ctx['known_issues']))

    def test_note_fixed_no_first_version(self):
        """
        If a note started has no first version but was fixed in the
        current version, include it in new features.
        """
        product = ProductFactory.create(name='Firefox')
        ReleaseFactory.create(version=19, sub_version=0, channel__name='Release', product=product)
        note1 = NoteFactory.create(first_version=None, fixed_in_version=19, product=product)

        views.release_notes(self.request, '19.0')
        eq_(set([note1]), set(self.last_ctx['new_features']))

    def test_note_fixed_product_name(self):
        """
        If a note does has no product or "Firefox" as the product,
        include it.
        """
        product = ProductFactory.create(name='Firefox')
        ReleaseFactory.create(version=19, sub_version=0, channel__name='Release', product=product)
        note1 = NoteFactory.create(first_version=None, fixed_in_version=19, product=product)
        note2 = NoteFactory.create(first_version=None, fixed_in_version=19, product=None)

        # Notes that shouldn't appear.
        NoteFactory.create(first_version=None, fixed_in_version=19, product__name='Fennec')
        NoteFactory.create(first_version=None, fixed_in_version=19, product__name='FirefoxOS')

        views.release_notes(self.request, '19.0')
        eq_(set([note1, note2]), set(self.last_ctx['new_features']))
