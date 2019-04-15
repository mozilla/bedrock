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

    # Redirects for SeaMonkey project website, now living at seamonkey-project.org
    url_test('/projects/seamonkey/', 'http://www.seamonkey-project.org/'),
    url_test('/projects/seamonkey/artwork.html',
             'http://www.seamonkey-project.org/dev/artwork'),
    url_test('/projects/seamonkey/community.html',
             'http://www.seamonkey-project.org/community'),
    url_test('/projects/seamonkey/get-involved.html',
             'http://www.seamonkey-project.org/dev/get-involved'),
    url_test('/projects/seamonkey/index.html', 'http://www.seamonkey-project.org/'),
    url_test('/projects/seamonkey/news.html', 'http://www.seamonkey-project.org/news'),
    url_test('/projects/seamonkey/project-areas.html',
             'http://www.seamonkey-project.org/dev/project-areas'),
    url_test('/projects/seamonkey/releases/', 'http://www.seamonkey-project.org/releases/'),
    url_test('/projects/seamonkey/releases/index.html',
             'http://www.seamonkey-project.org/releases/'),
    url_test('/projects/seamonkey/review-and-flags.html',
             'http://www.seamonkey-project.org/dev/review-and-flags'),
    url_test('/projects/seamonkey/releases/1.2.3.html',
             'http://www.seamonkey-project.org/releases/1.2.3'),
    url_test('/projects/seamonkey/releases/seamonkey-man/index.html',
             'http://www.seamonkey-project.org/releases/seamonkey-man/'),
    url_test('/projects/seamonkey/releases/seamonkey-dude/walter.html',
             'http://www.seamonkey-project.org/releases/seamonkey-dude/walter'),
    url_test('/projects/seamonkey/releases/updates/so-good',
             'http://www.seamonkey-project.org/releases/updates/so-good'),
    url_test('/projects/seamonkey/start/', 'http://www.seamonkey-project.org/start/'),

    # bug 1236910
    url_test('/support/anything', 'https://support.mozilla.org/'),

    # Bug 682619
    url_test('/support/thunderbird/problem', 'https://support.mozilla.org/products/thunderbird'),
    url_test('/support/firefox/bug', 'https://support.mozilla.org/products/firefox'),

    # Bug 638948 redirect beta privacy policy link
    url_test('/firefox/beta/feedbackprivacypolicy/', '/privacy/firefox/'),

    # Bug 424204
    url_test('/en-US/firefox/help/', 'https://support.mozilla.org/'),

    # Bug 1255882
    url_test('/some/url///', '/some/url/'),
    url_test('////', '/en-US/'),
    url_test('/en-US///', '/en-US/'),
    url_test('/de/firefox/about/', '/de/about/'),

    # bug 1300373
    url_test('/%2fgoogle.com//', '/google.com/'),

    # bug 453506, 1255882
    url_test('/editor/editor-embedding.html',
             'https://developer.mozilla.org/docs/Gecko/Embedding_Mozilla/Embedding_the_editor'),
    url_test('/editor/midasdemo/securityprefs.html',
             'https://developer.mozilla.org/docs/Mozilla/Projects/Midas/Security_preferences'),
    url_test('/editor/random/page.html', 'http://www-archive.mozilla.org/editor/random/page.html'),

    # bug 726217, 1255882
    url_test('/projects/bonecho/anti-phishing/',
             'https://support.mozilla.org/kb/how-does-phishing-and-malware-protection-work'),

    # Bug 453876, 840416
    url_test('/add-ons/kodakcd', 'https://addons.mozilla.org/en-US/firefox/addon/4441'),

    # Bug 1255882
    url_test('/firefox/personal.html', '/firefox/new/'),
    url_test('/firefox/upgrade.html', '/firefox/new/'),
    url_test('/firefox/ie.html', '/firefox/new/'),
))
