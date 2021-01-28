from hashlib import sha1

from django.conf import settings

import qrcode as qr
from django_jinja import library
from jinja2 import Markup
from qrcode.image.svg import SvgPathImage


QR_CACHE_PATH = settings.DATA_PATH.joinpath('qrcode_cache')
QR_CACHE_PATH.mkdir(exist_ok=True)


@library.global_function
def qrcode(data, box_size=20):
    name = sha1(f'{data}-{box_size}'.encode('utf-8')).hexdigest()
    filename = f'{name}.svg'
    filepath = QR_CACHE_PATH.joinpath(filename)
    if not filepath.exists():
        img = qr.make(data,
                      image_factory=SvgPathImage,
                      box_size=box_size)
        img.save(str(filepath))

    with filepath.open() as fp:
        return Markup(fp.read())
