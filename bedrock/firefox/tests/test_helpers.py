from django.test.utils import override_settings

from mock import patch
from nose.tools import assert_false, eq_

from bedrock.mozorg.tests import TestCase
from bedrock.firefox import helpers


@override_settings(FIREFOX_OS_FEED_LOCALES=['xx'])
@patch('bedrock.firefox.helpers.cache')
@patch('bedrock.firefox.helpers.FirefoxOSFeedLink')
class FirefoxOSFeedLinksTest(TestCase):
    def test_no_feed_for_locale(self, FirefoxOSFeedLink, cache):
        """
        Should return None without checking cache or db.
        """
        eq_(helpers.firefox_os_feed_links('yy'), None)
        assert_false(cache.get.called)
        assert_false(FirefoxOSFeedLink.objects.filter.called)

    def test_force_cache_refresh(self, FirefoxOSFeedLink, cache):
        """
        Should force cache update of first 10 values without cache.get()
        """

        (FirefoxOSFeedLink.objects.filter.return_value.order_by.return_value
         .values_list.return_value) = range(20)
        eq_(helpers.firefox_os_feed_links('xx', force_cache_refresh=True),
            range(10))
        assert_false(cache.get.called)
        FirefoxOSFeedLink.objects.filter.assert_called_with(locale='xx')
        cache.set.assert_called_with('firefox-os-feed-links-xx', range(10))

    def test_cache_miss(self, FirefoxOSFeedLink, cache):
        """
        Should update cache with first 10 items from db query
        """
        cache.get.return_value = None
        (FirefoxOSFeedLink.objects.filter.return_value.order_by.return_value
         .values_list.return_value) = range(20)
        eq_(helpers.firefox_os_feed_links('xx'), range(10))
        cache.get.assert_called_with('firefox-os-feed-links-xx')
        FirefoxOSFeedLink.objects.filter.assert_called_with(locale='xx')
        cache.set.assert_called_with('firefox-os-feed-links-xx', range(10))

    def test_hyphenated_cached(self, FirefoxOSFeedLink, cache):
        """
        Should construct cache key with only first part of hyphenated locale.
        """
        eq_(helpers.firefox_os_feed_links('xx-xx'), cache.get.return_value)
        cache.get.assert_called_with('firefox-os-feed-links-xx')
        assert_false(FirefoxOSFeedLink.objects.filter.called)


class FirefoxOSBlogLinkTest(TestCase):
    def test_correct_link_returned_for_es(self):
        """
        Should return the corect link for the es-ES locale
        """
        blog_link_es = 'https://blog.mozilla.org/press-es/category/firefox-os/'

        eq_(helpers.firefox_os_blog_link('es-ES'), blog_link_es)

    def test_correct_link_returned_for_locale_prefix(self):
        """
        Should return the latam link for the es-mx and es-ar locale
        """
        blog_link_latam = 'https://blog.mozilla.org/press-latam/category/firefox-os/'

        eq_(helpers.firefox_os_blog_link('es-mx'), blog_link_latam)
        eq_(helpers.firefox_os_blog_link('es-ar'), blog_link_latam)

    def test_none_returned(self):
        """
        Should return None as the locale will not be found
        """
        eq_(helpers.firefox_os_blog_link('esmx'), None)
