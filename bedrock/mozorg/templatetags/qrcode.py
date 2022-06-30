# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hashlib import sha1
from io import BytesIO

from django.core.cache import caches

import qrcode as qr
from django_jinja import library
from markupsafe import Markup
from qrcode.image.svg import SvgPathImage

cache = caches["qrcode"]


@library.global_function
def qrcode(data, box_size=20):
    key = sha1(f"{data}-{box_size}".encode()).hexdigest()
    svg = cache.get(key)
    if not svg:
        img = qr.make(data, image_factory=SvgPathImage, box_size=box_size)
        svg = BytesIO()
        img.save(svg)
        svg = svg.getvalue().decode("utf-8")
        cache.set(key, svg)

    return Markup(svg)
