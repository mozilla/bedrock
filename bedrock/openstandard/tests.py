from datetime import datetime

from django.test import TestCase
from django.test.utils import override_settings

from dateutil.tz import tzutc
from mock import Mock, patch
from nose.tools import eq_

from . import utils


class UtilsTest(TestCase):
    @patch('bedrock.openstandard.utils.cache')
    def test_categorized_articles_cache_hit(self, cache_mock):
        """
        Should return cached result
        """
        eq_(utils.categorized_articles(), cache_mock.get.return_value)
        cache_mock.get.assert_called_with('openstandard_articles')

    @patch('bedrock.openstandard.utils.cache')
    @patch('bedrock.openstandard.utils.Article')
    def test_categorized_articles_cache_miss(self, article_mock, cache_mock):
        """
        Should construct dict from db, cache result, return dict
        """
        live1 = Mock(category='live')
        live2 = Mock(category='live')
        learn1 = Mock(category='learn')
        learn2 = Mock(category='learn')
        (article_mock.objects.exclude.return_value.select_related.return_value
         .order_by.return_value) = [live1, live2, learn1, learn2]
        cache_mock.get.return_value = None

        categorized = utils.categorized_articles()
        eq_(categorized['live'], [live1, live2])
        eq_(categorized['learn'], [learn1, learn2])
        cache_mock.get.assert_called_with('openstandard_articles')
        cache_mock.set.assert_called_with('openstandard_articles', categorized, None)

    @patch('bedrock.openstandard.utils.cache')
    @patch('bedrock.openstandard.utils.Article')
    def test_categorized_articles_force_cache_refresh(self, article_mock, cache_mock):
        """
        Should update cache from db and return without checking cache
        """
        live1 = Mock(category='live')
        live2 = Mock(category='live')
        learn1 = Mock(category='learn')
        learn2 = Mock(category='learn')
        (article_mock.objects.exclude.return_value.select_related.return_value
         .order_by.return_value) = [live1, live2, learn1, learn2]

        categorized = utils.categorized_articles(force_cache_refresh=True)
        eq_(cache_mock.get.call_count, 0)
        eq_(categorized['live'], [live1, live2])
        eq_(categorized['learn'], [learn1, learn2])
        cache_mock.set.assert_called_with('openstandard_articles', categorized, None)

    @override_settings(USE_TZ=False, TIME_ZONE='America/Los_Angeles')
    @patch('bedrock.openstandard.utils.categorized_feed_entries')
    def test_published_in_feeds(self, categorized_feed_entries_mock):
        categorized_feed_entries_mock.return_value = [
            ('category', {'published': 'Fri, 17 Oct 2014 20:09:34 +0000'}),
            ('category', {})]
        eq_(list(utils.published_in_feeds()),
            [datetime(2014, 10, 17, 20, 9, 34, tzinfo=tzutc())])

    @patch('bedrock.openstandard.utils.Article')
    @patch('bedrock.openstandard.utils.published_in_feeds')
    @patch('bedrock.openstandard.utils.categorized_articles')
    def test_delete_old_articles(self, categorized_articles_mock,
                                 published_in_feeds_mock, article_mock):
        """
        Should delete articles older than those on homepage and/or in feeds
        """
        oldest_homepage_published = datetime(2001, 1, 1)
        categorized_articles_mock.return_value.values.return_value = [
            [Mock(published=oldest_homepage_published)]]
        published_in_feeds_mock.return_value = [datetime(2001, 1, 2)]
        utils.delete_old_articles()
        article_mock.objects.filter.return_value.delete.assert_called_once_with()
        article_mock.objects.filter.assert_called_once_with(
            published__lt=oldest_homepage_published)

    def test_multi_cateorize(self):
        """
        Should create a sorted csv of deduped categories in the category key
        """
        eq_(utils.multi_categorize({'category': 'a'}, 'a'),
            {'category': 'a'})
        eq_(utils.multi_categorize({'category': 'b'}, 'a'),
            {'category': 'a,b'})

    def test_maybe_update_unchanged(self):
        """
        Should not call save method for unchanged data
        """
        model_instance_mock = Mock(key='value')
        data = {'key': 'value'}
        utils.maybe_update(model_instance_mock, data)
        eq_(model_instance_mock.save.called, 0)

    def test_maybe_update_changed(self):
        """
        Should call save method for changed data with specific update_fields
        """
        model_instance_mock = Mock(key='value')
        data = {'key': 'value', 'changed_field': 'changed'}
        utils.maybe_update(model_instance_mock, data)
        eq_(model_instance_mock.changed_field, 'changed')
        model_instance_mock.save.assert_called_once_with(
            update_fields=['changed_field'])

    @patch('bedrock.openstandard.utils.BeautifulSoup')
    @patch('bedrock.openstandard.utils.parse_datetime')
    @patch('bedrock.openstandard.utils.get_or_maybe_create_article_image')
    def test_get_validated_article_data(self, get_or_maybe_create_article_image,
                                        parse_datetime, beautifulsoup):
        eq_(utils.get_validated_article_data({}, 'category'), None)
        entry = {
            'author': 'Joel and Ethan Coen',
            'link': 'http://en.wikipedia.org/wiki/The_Big_Lebowski',
            'title': 'The Big Lebowski',
            'summary': 'The Dude abides.',
            'published': 'January 18, 1998'}
        validated_entry = {
            'author': 'Joel and Ethan Coen',
            'link': 'http://en.wikipedia.org/wiki/The_Big_Lebowski',
            'title': 'The Big Lebowski',
            'summary': beautifulsoup.return_value.get_text.return_value,
            'published': parse_datetime.return_value,
            'category': 'films',
            'image': get_or_maybe_create_article_image.return_value}
        eq_(utils.get_validated_article_data(entry, 'films'), validated_entry)
        parse_datetime.assert_called_with('January 18, 1998')
        get_or_maybe_create_article_image.assert_called_with(
            beautifulsoup.return_value)
        beautifulsoup.assert_called_with(entry['summary'])

        sponsored_entry = entry.copy()
        sponsored_entry['tags'] = [{'term': 'Sponsored'}]
        eq_(utils.get_validated_article_data(sponsored_entry, 'films'), None)
