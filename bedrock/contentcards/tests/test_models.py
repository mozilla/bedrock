# coding=utf-8
from builtins import str
from builtins import range
from django.test import override_settings

from jinja2 import Markup
from pathlib2 import Path

from bedrock.contentcards import models
from bedrock.mozorg.tests import TestCase


DATA_PATH = Path(__file__).parent.joinpath('test_data')


class TestGetDataFromFilePath(TestCase):
    def test_the_func(self):
        self.assertDictEqual(
            models.get_data_from_file_path(Path('content/home/dude.en-US.json')),
            {
                'locale': 'en-US',
                'card_name': 'dude',
                'page_name': 'home',
                'page_id': 'home-en-US-dude',
            }
        )
        self.assertDictEqual(
            models.get_data_from_file_path(Path('content/the-dude/10th.de.json')),
            {
                'locale': 'de',
                'card_name': '10th',
                'page_name': 'the-dude',
                'page_id': 'the-dude-de-10th',
            }
        )


@override_settings(
    CONTENT_CARDS_PATH=str(DATA_PATH),
    CONTENT_CARDS_URL='/media/',
    STATIC_URL='/media/',
)
class TestContentCardModel(TestCase):
    def setUp(self):
        models.ContentCard.objects.refresh()

    def test_get_card_missing(self):
        with self.assertRaises(models.ContentCard.DoesNotExist):
            models.ContentCard.objects.get_card('home', 'card_10')

    def test_card_data(self):
        card1 = models.ContentCard.objects.get_card('home', 'card_1')
        self.assertEqual(card1.id, 'home-en-US-card_1')
        self.assertEqual(card1.page_name, 'home')
        self.assertEqual(card1.card_name, 'card_1')
        self.assertEqual(card1.locale, 'en-US')
        with self.activate('de'):
            card_data = card1.card_data

        self.assertDictEqual(
            card_data,
            {
                'title': 'We keep your data safe, never sold.',
                'ga_title': 'We keep your data safe, never sold.',
                'highres_image_url': '/media/contentcards/img/home/ffyr-high-res.191bff93b820.png',
                'media_icon': 'mzp-has-video',
                'class': 'mzp-c-card-large',
                'image_url': '/media/contentcards/img/home/ffyr.75c74c6ba409.png',
                'youtube_id': 'rZAQ6vgt8nE',
                'aspect_ratio': 'mzp-has-aspect-16-9',
                'desc': u'You have the right to your own life \u2014 and your own data. '
                        u'Everything we make and do fights for you.',
                'link_url': '/de/firefox/fights-for-you/',
                'tag_label': 'Video',
            }
        )

    def test_get_page_cards(self):
        cards = models.ContentCard.objects.get_page_cards('home')
        self.assertTrue(all(name in cards for name in
                            ['card_%d' % i for i in range(1, 6)]))
        self.assertDictEqual(
            cards['card_2'],
            {
                'aspect_ratio': 'mzp-has-aspect-1-1',
                'desc': 'Microsoft is giving up on an independent shared platform for the internet, '
                        'and in doing so, hands over control of more of online life to Google.',
                'highres_image_url': '/media/contentcards/img/home/edge-high-res.e3fd47cab8f0.png',
                'image_url': '/media/contentcards/img/home/edge.72822d0ff717.png',
                'link_url': 'https://blog.mozilla.org/blog/2018/12/06/goodbye-edge/?utm_source='
                            'www.mozilla.org&utm_medium=referral&utm_campaign=homepage&utm_content=card',
                'class': 'mzp-c-card-small',
                'tag_label': 'Internet Health',
                'title': 'Goodbye, EdgeHTML',
                'ga_title': 'Goodbye, EdgeHTML',
            }
        )

    def test_get_page_cards_empty(self):
        cards = models.ContentCard.objects.get_page_cards('home', 'fr')
        self.assertEqual(cards, {})

    def test_html_content(self):
        card2 = models.ContentCard.objects.get_card('home', 'card_2')
        self.assertFalse('html_content' in card2.data)
        self.assertEqual(card2.content, '<p>This is the converted <em>Markdown</em></p>')
        self.assertEqual(card2.html, Markup('<p>This is the converted <em>Markdown</em></p>'))
