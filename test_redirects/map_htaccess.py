from __future__ import absolute_import

from .base import flatten, url_test


URLS = flatten((
    # Bug 774331 - European press pages
    # en-GB
    url_test('/en-GB/press/', 'https://blog.mozilla.org/press-uk/'),
    url_test('/en-GB/press/media/', 'https://blog.mozilla.org/press-uk/media-library/'),
    url_test('/en-GB/press/media/logos/', 'https://blog.mozilla.org/press-uk/media-library/'),
    url_test('/en-GB/press/media/screenshots/',
             'https://blog.mozilla.org/press-uk/media-library/product-screenshots/'),
    url_test('/en-GB/press/media/images/', 'https://blog.mozilla.org/press-uk/media-library/'),
    url_test('/en-GB/press/media/videos/',
             'https://blog.mozilla.org/press-uk/media-library/videos/'),

    # de
    url_test('/de/press/', 'https://blog.mozilla.org/press-de/'),
    url_test('/de/press/media/', 'https://blog.mozilla.org/press-de/medienbibliothek/'),
    url_test('/de/press/media/logos/', 'https://blog.mozilla.org/press-de/medienbibliothek/'),
    url_test('/de/press/media/screenshots/',
             'https://blog.mozilla.org/press-de/medienbibliothek/produkt-screenshots/'),
    url_test('/de/press/media/images/', 'https://blog.mozilla.org/press-de/medienbibliothek/'),
    url_test('/de/press/media/videos/',
             'https://blog.mozilla.org/press-de/medienbibliothek/videos/'),
    url_test('/de/press/media/bios/', 'https://blog.mozilla.org/press/media-library/bios/'),

    # fr
    url_test('/fr/press/', 'https://blog.mozilla.org/press-fr/'),
    url_test('/fr/press/media/', 'https://blog.mozilla.org/press-fr/bibliotheque-mozilla/'),
    url_test('/fr/press/media/logos/', 'https://blog.mozilla.org/press-fr/bibliotheque-mozilla/'),
    url_test('/fr/press/media/screenshots/',
             'https://blog.mozilla.org/press-fr/bibliotheque-mozilla/captures-decran-produits/'),
    url_test('/fr/press/media/images/',
             'https://blog.mozilla.org/press-fr/bibliotheque-mozilla/'),
    url_test('/fr/press/media/videos/',
             'https://blog.mozilla.org/press-fr/bibliotheque-mozilla/videos/'),
    url_test('/fr/press/media/bios/', 'https://blog.mozilla.org/press/media-library/bios/'),

    # it
    url_test('/it/press/', 'https://blog.mozilla.org/press-it/'),
    url_test('/it/press/media/', 'https://blog.mozilla.org/press-it/galleria-multimediale/'),
    url_test('/it/press/media/logos/',
             'https://blog.mozilla.org/press-it/galleria-multimediale/'),
    url_test('/it/press/media/screenshots/',
             'https://blog.mozilla.org/press-it/galleria-multimediale/immagini-del-prodotto/'),
    url_test('/it/press/media/images/',
             'https://blog.mozilla.org/press-it/galleria-multimediale/'),
    url_test('/it/press/media/videos/',
             'https://blog.mozilla.org/press-it/galleria-multimediale/videos/'),
    url_test('/it/press/media/bios/', 'https://blog.mozilla.org/press/media-library/bios/'),

    # es
    url_test('/es{,-ES,-AR,-MX}/press/', 'https://blog.mozilla.org/press-es/'),
    url_test('/es{,-ES,-AR,-MX}/press/media/',
             'https://blog.mozilla.org/press-es/galeria-multimedia-de-mozilla/'),
    url_test('/es{,-ES,-AR,-MX}/press/media/logos/',
             'https://blog.mozilla.org/press-es/galeria-multimedia-de-mozilla/'),
    url_test('/es{,-ES,-AR,-MX}/press/media/screenshots/',
             'https://blog.mozilla.org/press-es/galeria-multimedia-de-mozilla/imagenes-del-producto/'),
    url_test('/es{,-ES,-AR,-MX}/press/media/images/',
             'https://blog.mozilla.org/press-es/galeria-multimedia-de-mozilla/'),
    url_test('/es{,-ES,-AR,-MX}/press/media/videos/',
             'https://blog.mozilla.org/press-es/galeria-multimedia-de-mozilla/videos/'),
    url_test('/es{,-ES,-AR,-MX}/press/media/bios/', 'https://blog.mozilla.org/press/media-library/bios/'),

    # pl
    url_test('/pl/press/', 'https://blog.mozilla.org/press-pl/'),
    url_test('/pl/press/media/', 'https://blog.mozilla.org/press-pl/galeria-multimediow/'),
    url_test('/pl/press/media/logos/', 'https://blog.mozilla.org/press-pl/galeria-multimediow/'),
    url_test('/pl/press/media/screenshots/',
             'https://blog.mozilla.org/press-pl/galeria-multimediow/screenshoty-produktow/'),
    url_test('/pl/press/media/images/', 'https://blog.mozilla.org/press-pl/galeria-multimediow/'),
    url_test('/pl/press/media/videos/',
             'https://blog.mozilla.org/press-pl/galeria-multimediow/videos/'),
    url_test('/pl/press/media/bios/', 'https://blog.mozilla.org/press/media-library/bios/'),

    # rest
    # Bug 747565
    url_test('/press/', 'https://blog.mozilla.org/press/'),
    url_test('/press/ataglance/', 'https://blog.mozilla.org/press/ataglance/'),
    url_test('/press/bios/', 'https://blog.mozilla.org/press/bios/'),
    url_test('/press/kits/', 'https://blog.mozilla.org/press/kits/'),
    url_test('/press/media/', 'https://blog.mozilla.org/press/media-library/'),
    url_test('/press/media/logos/', 'https://blog.mozilla.org/press/media-library/'),
    url_test('/press/media/bios/', 'https://blog.mozilla.org/press/media-library/bios/'),
    url_test('/press/media/screenshots/',
             'https://blog.mozilla.org/press/media-library/screenshots/'),
    url_test('/press/media/videos/', 'https://blog.mozilla.org/press/media-library/videos/'),

))
