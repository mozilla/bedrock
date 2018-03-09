# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import date

from bedrock.mozorg.tests import TestCase
from bedrock.security.models import Product, HallOfFamer


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
