from django.test.utils import override_settings

from mock import Mock, patch

from bedrock.firefox.models import FirefoxOSFeedLink
from bedrock.mozorg.tests import TestCase

from scripts import update_firefox_os_feeds


class TestUpdateFirefoxOSFeeds(TestCase):
    @override_settings(FIREFOX_OS_FEEDS=[('xx', 'http://example.com/feed'),
                                         ('yy', 'http://example.com/feed2')])
    @patch('scripts.update_firefox_os_feeds.create_or_update_fxos_feed_links')
    @patch('scripts.update_firefox_os_feeds.parse')
    def test_run_exception_handling(self, parse, create_or_update_fxos_feed_links):
        parse.side_effect = [Exception('test'), 'parsed feed']
        update_firefox_os_feeds.run()
        create_or_update_fxos_feed_links.assert_called_with('yy', 'parsed feed')

    @patch('scripts.update_firefox_os_feeds.create_or_update_fxos_feed_link')
    def test_create_or_update_fxos_feed_links(
            self, create_or_update_fxos_feed_link):
        update_firefox_os_feeds.create_or_update_fxos_feed_links(
            'xx',
            {'entries': [{}, {'link': 'http://example.com', 'title': 'Title'}]})
        create_or_update_fxos_feed_link.assert_called_with(
            'xx', 'http://example.com', 'Title')

    @patch('scripts.update_firefox_os_feeds.FirefoxOSFeedLink.objects')
    def test_create_or_update_fxos_feed_link(self, objects):
        objects.get_or_create.return_value = ('feed_link', True)
        update_firefox_os_feeds.create_or_update_fxos_feed_link(
            'xx', 'http://example.com', 'Title')
        objects.get_or_create.assert_called_with(
            locale='xx', link='http://example.com', defaults={'title': 'Title'})

    @patch('scripts.update_firefox_os_feeds.FirefoxOSFeedLink.objects')
    def test_create_or_update_fxos_feed_link_update_title(self, objects):
        feed_link = Mock(title='Old Title')
        objects.get_or_create.return_value = (feed_link, False)
        update_firefox_os_feeds.create_or_update_fxos_feed_link(
            'xx', 'http://example.com', 'Title')
        objects.get_or_create.assert_called_with(
            locale='xx', link='http://example.com', defaults={'title': 'Title'})
        feed_link.save.assert_called_with(update_fields=['title'])
