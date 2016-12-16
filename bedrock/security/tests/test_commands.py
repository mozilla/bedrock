# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from mock import patch

from nose.tools import eq_

from bedrock.mozorg.tests import TestCase
from bedrock.security.management.commands import update_security_advisories
from bedrock.security.models import Product


def test_fix_product_name():
    """Should fix SeaMonkey and strip '.0' from names."""
    eq_(update_security_advisories.fix_product_name('Seamonkey 2.2'),
        'SeaMonkey 2.2')
    eq_(update_security_advisories.fix_product_name('Firefox 2.2'),
        'Firefox 2.2')
    eq_(update_security_advisories.fix_product_name('fredflintstone 2.2'),
        'fredflintstone 2.2')
    eq_(update_security_advisories.fix_product_name('Firefox 32.0'),
        'Firefox 32')
    eq_(update_security_advisories.fix_product_name('Firefox 32.0.1'),
        'Firefox 32.0.1')


def test_filter_advisory_names():
    filenames = [
        'README.md',
        'LICENSE.txt',
        'announce/2015/mfsa2015-01.md',
        'announce/2015/mfsa2016-42.yml',
        'stuff/whatnot.md',
        'mfsa2015-02.md',
    ]
    good_filenames = [
        settings.MOFO_SECURITY_ADVISORIES_PATH + '/announce/2015/mfsa2015-01.md',
        settings.MOFO_SECURITY_ADVISORIES_PATH + '/announce/2015/mfsa2016-42.yml',
        settings.MOFO_SECURITY_ADVISORIES_PATH + '/mfsa2015-02.md',
    ]
    eq_(update_security_advisories.filter_advisory_filenames(filenames), good_filenames)


def test_get_ids_from_files():
    filenames = [
        'README.md',
        'LICENSE.txt',
        'announce/2015/mfsa2015-01.md',
        'announce/2015/mfsa2016-42.yml',
        'stuff/whatnot.md',
        'mfsa2015-02.md',
    ]
    good_ids = ['2015-01', '2016-42', '2015-02']
    eq_(update_security_advisories.get_ids_from_files(filenames), good_ids)


def make_mfsa(mfsa_id):
    update_security_advisories.add_or_update_advisory({
        'mfsa_id': mfsa_id,
        'title': 'The Dude is insecure',
        'impact': 'High',
        'announced': 'December 25, 2015',
        'fixed_in': ['Firefox 43.0.1'],
    }, 'The Dude minds, man!')


class TestDBActions(TestCase):
    def test_get_files_to_delete_from_db(self):
        make_mfsa('2015-100')
        make_mfsa('2015-101')
        make_mfsa('2015-102')
        make_mfsa('2015-103')
        all_files = ['mfsa2015-100.md', 'mfsa2015-101.md']
        eq_(update_security_advisories.get_files_to_delete_from_db(all_files),
            ['mfsa2015-102.md', 'mfsa2015-103.md'])

    def test_delete_orphaned_products(self):
        make_mfsa('2015-100')
        Product.objects.create(name='Firefox 43.0.2')
        Product.objects.create(name='Firefox 43.0.3')
        eq_(update_security_advisories.delete_orphaned_products(), 2)
        eq_(Product.objects.get().name, 'Firefox 43.0.1')

    @patch.object(update_security_advisories, 'get_all_mfsa_files')
    @patch.object(update_security_advisories, 'delete_files')
    @patch.object(update_security_advisories, 'update_db_from_file')
    @patch.object(update_security_advisories, 'GitRepo')
    def test_file_name_extension_change(self, git_mock, udbff_mock, df_mock, gamf_mock):
        """
        An MFSA file can now be either .md or .yml. Make sure this is an update, not a delete.
        """
        make_mfsa('2016-42')
        make_mfsa('2016-43')
        all_files = ['mfsa2016-42.yml']
        gamf_mock.return_value = all_files
        git_mock().has_changes.return_value = True
        update_security_advisories.Command().handle_noargs(quiet=True, no_git=False,
                                                           clear_db=False)
        udbff_mock.assert_called_with(update_security_advisories.filter_advisory_filenames(
            all_files)[0])
        df_mock.assert_called_with(['mfsa2016-43.md'])
