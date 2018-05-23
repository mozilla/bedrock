# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import date

from bedrock.mozorg.tests import TestCase
from bedrock.security.models import MitreCVE, Product, HallOfFamer


class TestProduct(TestCase):
    def test_version_ordering(self):
        pv3 = Product.objects.create(name='Firefox 24.0.1')
        pv2 = Product.objects.create(name='Firefox 24.0')
        pv0 = Product.objects.create(name='Fennec 24.0')
        pv1 = Product.objects.create(name='Firefox 23.0')
        pv4 = Product.objects.create(name='Firefox 25')
        pv5 = Product.objects.create(name='Firefox 22')
        pvs = [pv2, pv0, pv3, pv1, pv4, pv5]
        self.assertListEqual([pv0, pv5, pv1, pv2, pv3, pv4], sorted(pvs))

    def test_product_version_slug(self):
        """Slug should include the version."""
        pv0 = Product.objects.create(name='Firefox 24.0.1')
        pv1 = Product.objects.create(name='Firefox ESR 24.2')
        self.assertEqual(pv0.slug, 'firefox-24.0.1')
        self.assertEqual(pv1.slug, 'firefox-esr-24.2')


class TestHallOfFamer(TestCase):
    def test_year_quarter(self):
        hf1 = HallOfFamer.objects.create(name='The Dude', program='web', date=date(2018, 3, 2))
        hf2 = HallOfFamer.objects.create(name='The Dude', program='web', date=date(2017, 4, 2))
        hf3 = HallOfFamer.objects.create(name='The Dude', program='web', date=date(2016, 7, 12))
        hf4 = HallOfFamer.objects.create(name='The Dude', program='web', date=date(2015, 11, 7))
        assert hf1.year_quarter == (2018, 1)
        assert hf1.quarter_string == '1st Quarter 2018'
        assert hf2.year_quarter == (2017, 2)
        assert hf2.quarter_string == '2nd Quarter 2017'
        assert hf3.year_quarter == (2016, 3)
        assert hf3.quarter_string == '3rd Quarter 2016'
        assert hf4.year_quarter == (2015, 4)
        assert hf4.quarter_string == '4th Quarter 2015'


class TestMitreCVE(TestCase):
    cve_id_order = 100

    def _create_cve(self, products=None):
        self.cve_id_order += 1
        products = products or ['Firefox 60', 'Firefox 60.0.1']
        return MitreCVE.objects.create(
            id='CVE-2018-%s' % self.cve_id_order,
            year=2018,
            order=self.cve_id_order,
            title='A Testing Problem',
            description='There was a problem.',
            products=products,
            mfsa_ids=['2018-11'],
            bugs=[{'url': 'https://bugzilla.mozilla.org/show_bug.cgi?id=1234567',
                   'desc': 'Bug 1234567'}],
        )

    def test_product_versions(self):
        cve = self._create_cve()
        assert cve.product_versions() == {'Firefox': ['60', '60.0.1']}
        cve = self._create_cve(['Firefox ESR 60.0.1', 'Firefox ESR 52.8.0', 'Firefox 60.0.1'])
        assert cve.product_versions() == {'Firefox': ['60.0.1'], 'Firefox ESR': ['60.0.1', '52.8.0']}

    def test_get_reference_data(self):
        cve = self._create_cve()
        assert cve.get_reference_data() == [
            {'url': 'https://www.mozilla.org/security/advisories/mfsa2018-11/'},
            {'url': 'https://bugzilla.mozilla.org/show_bug.cgi?id=1234567'},
        ]

    def test_get_description(self):
        cve = self._create_cve()
        assert cve.get_description() == 'There was a problem. This vulnerability affects Firefox < 60 and Firefox < 60.0.1.'
        cve = self._create_cve(['Firefox ESR 60.0.1', 'Firefox ESR 52.8.0', 'Firefox 60.0.1'])
        assert cve.get_description() == ('There was a problem. This vulnerability affects Firefox ESR < 60.0.1, '
                                         'Firefox ESR < 52.8.0, and Firefox < 60.0.1.')
        cve = self._create_cve(['Firefox ESR 60.0.1'])
        cve.description = 'No punctuation'
        assert cve.get_description() == 'No punctuation. This vulnerability affects Firefox ESR < 60.0.1.'
        cve.description = 'Punctuation but extra space. \n'
        assert cve.get_description() == 'Punctuation but extra space. This vulnerability affects Firefox ESR < 60.0.1.'
