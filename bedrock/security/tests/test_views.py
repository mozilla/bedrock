# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.test import RequestFactory

from mock import patch, Mock
from product_details.version_compare import Version

from bedrock.mozorg.tests import TestCase
from bedrock.security.management.commands.update_security_advisories import add_or_update_advisory
from bedrock.security.models import Product
from bedrock.security.views import ProductView, ProductVersionView, latest_queryset


class TestViews(TestCase):
    def setUp(self):
        pvnames = [
            'Firefox 3.6',
            'Firefox 4.0',
            'Firefox 4.0.1',
            'Firefox 4.2',
            'Firefox 4.2.3',
            'Firefox 24.0',
        ]
        self.pvs = [Product.objects.create(name=pv) for pv in pvnames]

    def test_product_view_min_version(self):
        """Should not include versions below minimum."""
        pview = ProductView()
        pview.kwargs = {'slug': 'firefox'}
        with patch.dict(pview.minimum_versions, {'firefox': Version('4.2')}):
            self.assertListEqual(pview.get_queryset(),
                                 [self.pvs[5], self.pvs[4], self.pvs[3]])

        with patch.dict(pview.minimum_versions, {'firefox': Version('22.0')}):
            self.assertListEqual(pview.get_queryset(), [self.pvs[5]])

    def test_product_version_view_filter_major(self):
        """Given a major version should return all minor versions."""
        pview = ProductVersionView()
        pview.kwargs = {'slug': 'firefox-4'}
        self.assertListEqual(pview.get_queryset(),
                             [self.pvs[4], self.pvs[3], self.pvs[2], self.pvs[1]])

    def test_product_version_view_filter_minor(self):
        """Given a minor version should return all point versions."""
        pview = ProductVersionView()
        pview.kwargs = {'slug': 'firefox-4.2'}
        self.assertListEqual(pview.get_queryset(), [self.pvs[4], self.pvs[3]])


class TestLastModified(TestCase):
    def setUp(self):
        self.next_id = 1
        self.rf = RequestFactory()

    def new_advisory(self, mfsa_id=None, title='WILMAAAA!', impact='Critical',
                     announced='August 18, 2014', fixed_in=None,
                     html='Wilma finally leaves Fred for a brontosaurus.'):
        if mfsa_id is None:
            mfsa_id = '2014-{0:0>2}'.format(self.next_id)
            self.next_id += 1

        if fixed_in is None:
            fixed_in = ['Firefox 29', 'Thunderbird 29']

        return add_or_update_advisory({
            'mfsa_id': mfsa_id,
            'title': title,
            'impact': impact,
            'announced': announced,
            'fixed_in': fixed_in,
        }, html)

    def test_latest_queryset_all(self):
        """Should return all advisories for the all page."""
        advisories = [self.new_advisory() for i in range(10)]
        req = self.rf.get('/')
        req.resolver_match = Mock()
        req.resolver_match.url_name = 'security.advisories'
        qs = latest_queryset(req, {})
        self.assertListEqual(advisories, list(qs.order_by('year', 'order')))

    def test_latest_queryset_single(self):
        """Should return a single advisory based on PK."""
        advisories = [self.new_advisory() for i in range(10)]
        req = self.rf.get('/')
        req.resolver_match = Mock()
        req.resolver_match.url_name = 'security.advisory'
        qs = latest_queryset(req, {'pk': '2014-05'})
        self.assertEqual(advisories[4], qs.get())

    def test_latest_queryset_product(self):
        """Should advisories for a single product."""
        advisories_fx = [self.new_advisory(fixed_in=['Firefox 30.0']) for i in range(5)]
        for i in range(5):
            self.new_advisory(fixed_in=['Thunderbird 30.0'])
        req = self.rf.get('/')
        req.resolver_match = Mock()
        req.resolver_match.url_name = 'security.product-advisories'
        qs = latest_queryset(req, {'slug': 'firefox'})
        self.assertListEqual(advisories_fx, list(qs.order_by('year', 'order')))

    def test_latest_queryset_product_version(self):
        """Should advisories for a single product version."""
        advisories_30 = [self.new_advisory(fixed_in=['Firefox 30.{0}'.format(i)])
                         for i in range(5)]
        advisories_29 = [self.new_advisory(fixed_in=['Firefox 29.0.{0}'.format(i)])
                         for i in range(1, 5)]
        # make sure the one with no point version is included
        advisories_29.append(self.new_advisory(fixed_in=['Firefox 29.0']))
        req = self.rf.get('/')
        req.resolver_match = Mock()
        req.resolver_match.url_name = 'security.product-version-advisories'
        qs = latest_queryset(req, {'slug': 'firefox-30'})
        self.assertListEqual(advisories_30, list(qs.order_by('year', 'order')))
        qs = latest_queryset(req, {'slug': 'firefox-30.1'})
        self.assertEqual(advisories_30[1], qs.get())
        qs = latest_queryset(req, {'slug': 'firefox-29.0'})
        self.assertListEqual(advisories_29, list(qs.order_by('year', 'order')))
