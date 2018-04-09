import mock

from bedrock.mozorg.tests import TestCase
from bedrock.newsletter import utils
from bedrock.newsletter.models import Newsletter
from bedrock.newsletter.tests import newsletters


newsletters_mock = mock.Mock()
newsletters_mock.return_value = newsletters


class TestGetNewsletters(TestCase):
    def test_simple_get(self):
        # get_newsletters returns whatever is in the DB.
        Newsletter.objects.create(
            slug='dude',
            data={
                'title': 'Abide',
                'languages': ['en']
            },
        )
        Newsletter.objects.create(
            slug='donnie',
            data={
                'title': 'Walrus',
                'languages': ['de']
            },
        )
        result = utils.get_newsletters()
        self.assertEqual(result, {
            'dude': {
                'title': 'Abide',
                'languages': ['en']
            },
            'donnie': {
                'title': 'Walrus',
                'languages': ['de']
            },
        })


@mock.patch('bedrock.newsletter.utils.get_newsletters', newsletters_mock)
class TestGetNewsletterLanguages(TestCase):
    def test_newsletter_langs(self):
        """Without args should return all langs."""
        result = utils.get_languages_for_newsletters()
        good_set = {'en', 'es', 'fr', 'de', 'pt', 'ru'}
        self.assertSetEqual(good_set, result)

    def test_single_newsletter_langs(self):
        """Should return languages for a single newsletter."""
        result = utils.get_languages_for_newsletters('join-mozilla')
        good_set = {'en', 'es'}
        self.assertSetEqual(good_set, result)

    def test_list_newsletter_langs(self):
        """Should return all languages for specified list of newsletters."""
        result = utils.get_languages_for_newsletters(['join-mozilla', 'beta'])
        good_set = {'en', 'es'}
        self.assertSetEqual(good_set, result)

        result = utils.get_languages_for_newsletters(['firefox-tips', 'beta'])
        good_set = {'en', 'fr', 'de', 'pt', 'ru'}
        self.assertSetEqual(good_set, result)

    def test_works_with_bad_newsletter(self):
        """If given a bad newsletter name, should still return a set."""
        result = utils.get_languages_for_newsletters(['join-mozilla', 'eldudarino'])
        good_set = {'en', 'es'}
        self.assertSetEqual(good_set, result)
