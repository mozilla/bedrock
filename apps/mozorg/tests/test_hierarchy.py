from mock import patch
from nose.tools import eq_

from django.conf import settings
from django.test.client import Client

from funfactory.urlresolvers import reverse
from mozorg.tests import TestCase
from urls_hierarchy import hierarchy, ref_urlpatterns, urlpatterns


@patch.object(settings, 'ROOT_URLCONF', 'mozorg.tests.urls_hierarchy')
class TestHierarchy(TestCase):
    def test_as_urlpattern(self):
        eq_(len(urlpatterns), len(ref_urlpatterns))

    def test_breadcrumbs(self):
        c = Client()
        with self.activate('en-US'):
            url = reverse('firefoxfamily.overview')
        response = c.get(url)
        response.context is None
        assert False
