from hashlib import sha1
from io import BytesIO

from django.core.cache import caches

import qrcode as qr
from django_jinja import library
from jinja2 import Markup
from qrcode.image.svg import SvgPathImage


cache = caches['qrcode']


@library.global_function
def qrcode(data, box_size=20):
    key = sha1(f'{data}-{box_size}'.encode('utf-8')).hexdigest()
    svg = cache.get(key)
    if not svg:
        img = qr.make(data,
                      image_factory=SvgPathImage,
                      box_size=box_size)
        svg = BytesIO()
        img.save(svg)
        svg = svg.getvalue().decode('utf-8')
        cache.set(key, svg)

    return Markup(svg)
