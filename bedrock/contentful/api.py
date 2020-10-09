import re

from django.conf import settings

import contentful as api


def get_client():
    client = None
    if settings.CONTENTFUL_SPACE_ID:
        client = api.Client(
            settings.CONTENTFUL_SPACE_ID,
            settings.CONTENTFUL_SPACE_KEY,
            api_url=settings.CONTENTFUL_SPACE_API,
        )

    return client


def _get_height(width, aspect):
    height = 0
    if aspect == '1-1':
        height = width

    if aspect == '3-2':
        height = width * 0.6666

    if aspect == '16-9':
        height = width * 0.5625

    return round(height)


def _get_image_url(image, width, aspect):
    return 'https:' + image.url(
        w=width,
        h=_get_height(width, aspect),
        fit='fill',
        f='faces',
    )


class Contentful:
    client = None
    card_field_re = re.compile(r'card\d$')
    card_fields = [
        'title',
        'desc',
        'cta',
        'meta',
        'image_url',
        'link_url',
        'tag_label',
        'youtube_id',
    ]
    # size, aspect
    card_layouts = {
        'fiveCardLayout': [
            ('large', '16-9'),
            ('small', '1-1'),
            ('small', '3-2'),
            ('small', '3-2'),
            ('small', '3-2'),
        ],
    }
    # normal, high-res
    card_image_widths = {
        'extra-small': (450, 900),
        'small': (450, 900),
        'medium': (600, 1200),
        'large': (930, 1860),
    }
    card_layout_classes = {
        'sixCardLayout': 'third',
        'fiveCardLayout': 'hero',
        'fourCardLayout': 'quarter',
        'threeCardLayout': 'third',
        'twoCardLayout': 'half',
    }

    def __init__(self):
        self.client = get_client()

    def get_all_page_data(self):
        pages = self.client.entries({'content_type': 'homepageEn'})
        return [self.get_home_page_data(p.id) for p in pages]

    def get_home_page_data(self, page_id):
        layouts = []
        page = self.client.entry(page_id, {'include': 5})
        page_data = {
            'lang': page.language.lower(),
            'id': page.id,
            'content_type': page.content_type.id,
        }
        layouts_data = self.get_home_page_layouts(page)
        for layout in layouts_data:
            layout_data = {
                'type': layout.content_type.id,
                'class': self.card_layout_classes[layout.content_type.id],
                'lang': page.language,
            }
            cards = self.get_layout_cards(layout)
            layout_data['cards'] = self.get_card_dicts(cards, layout_data['type'])
            layouts.append(layout_data)

        page_data['layouts'] = layouts
        return page_data

    def get_home_page_layouts(self, page_obj):
        return [v for k, v in page_obj.fields().items() if k.startswith('card_group')]

    def get_layout_cards(self, layout):
        return [v for k, v in layout.fields().items() if self.card_field_re.match(k)]

    def get_card_dicts(self, cards, layout_type):
        config = self.card_layouts[layout_type]
        card_list = []
        for i, card in enumerate(cards):
            size, aspect = config[i]
            card_list.append(self.get_card(card, size, aspect))

        return card_list

    def get_card(self, card, size, aspect):
        if hasattr(card, 'card'):
            card = card.card

        card_data = {
            'class': f'mzp-c-card-{size}',
            'aspect_ratio': f'mzp-has-aspect-{aspect}',
        }
        for name, value in card.fields().items():
            if name in self.card_fields:
                if name == 'image_url':
                    width, width_highres = self.card_image_widths[size]
                    max_width = value.file['details']['image']['width']
                    if max_width >= width_highres:
                        card_data['highres_image_url'] = _get_image_url(value, width_highres, aspect)

                    card_data[name] = _get_image_url(value, width, aspect)
                    continue

                card_data[name] = value

                if name == 'title':
                    card_data['ga_title'] = value

                if name == 'youtube_id':
                    card_data['media_icon'] = 'mzp-has-video'

        return card_data


contentful = Contentful()
