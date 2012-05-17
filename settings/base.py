# Django settings file for bedrock.

import os

from django.utils.functional import lazy

from funfactory.settings_base import *

# Make file paths relative to settings.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = lambda *a: os.path.join(ROOT, *a)

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

SESSION_COOKIE_SECURE = True

# Accepted locales
PROD_LANGUAGES = ('ab-CD', 'ach', 'af', 'ak', 'ar', 'as', 'ast', 'be', 'bg',
                  'bin', 'bn-BD', 'bn-IN', 'br', 'bs', 'ca', 'cs', 'csb', 'cy',
                  'da', 'de', 'el', 'en-GB', 'en-US', 'en-ZA', 'eo', 'es-AR',
                  'es-CL', 'es-ES', 'es-MX', 'et', 'eu', 'fa', 'ff', 'fi', 'fr',
                  'fy-NL', 'ga-IE', 'gd', 'gl', 'gu-IN', 'he', 'hi-IN', 'hr',
                  'hu', 'hy-AM', 'id', 'is', 'it', 'ja', 'ja-JP-mac', 'js',
                  'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'lg', 'lij', 'lt', 'lv',
                  'mai', 'mk', 'ml', 'mn', 'mr', 'ms', 'my', 'nb-NO', 'nl',
                  'nn-NO', 'nso', 'oc', 'or', 'pa-IN', 'pl', 'pt-BR', 'pt-PT',
                  'rm', 'ro', 'ru', 'si', 'sk', 'sl', 'son', 'sq', 'sr',
                  'sv-SE', 'sw', 'ta', 'ta-LK', 'te', 'th', 'tr', 'uk',
                  'vi', 'wo', 'zh-CN', 'zh-TW', 'zu')
DEV_LANGUAGES = list(DEV_LANGUAGES) + ['en-US']

FEED_CACHE = 60
DOTLANG_CACHE = 60

DOTLANG_FILES = ['main', 'base', 'newsletter']

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1iz#v0m55@h26^m6hxk3a7at*h$qj_2a$juu1#nv50548j(x1v'

TEMPLATE_DIRS = (
    path('templates'),
    path('locale')
)

def JINJA_CONFIG():
    import jinja2
    from django.conf import settings
    config = {'extensions': ['tower.template.i18n', 'jinja2.ext.do',
                             'jinja2.ext.with_', 'jinja2.ext.loopcontrols',
                             'l10n_utils.template.l10n_blocks',
                             'l10n_utils.template.lang_blocks'],
              'finalize': lambda x: x if x is not None else ''}
    return config

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'about': (
            'css/about.less',
        ),
        'b2g': (
            'css/b2g.less',
        ),
        'webmaker': (
            'css/webmaker.less',
        ),
        'collusion': (
            'css/collusion.less',
        ),
        'common': (
            'css/sandstone/sandstone.less',
        ),
        'contribute': (
            'css/contribute.less',
        ),
        'contribute-page': (
            'css/contribute-page.less',
        ),
        'channel': (
            'css/covehead/template.css',
            'css/covehead/content.css',
            'css/covehead/channel.css',
        ),
        'firefox': (
            'css/firefox/template.less',
        ),
        'firefox_channel': (
            'css/firefox/channel.less',
        ),
        'firefox_central': (
            'css/sandstone/video.less',
            'css/firefox/central.less',
        ),
        'firefox_customize': (
            'css/sandstone/video.less',
            'css/firefox/customize.less',
        ),
        'firefox_features': (
            'css/sandstone/video.less',
            'css/firefox/features.less',
        ),
        'firefox_fx': (
            'css/firefox/fx.less',
        ),
        'firefox_geolocation': (
            'css/mozilla-expanders.less',
            'css/firefox/geolocation.less',
            'css/jquery/nyroModal.css'
        ),
        'firefox_happy': (
            'css/firefox/happy.less',
        ),
        'firefox_new': (
            'css/firefox/new.less',
        ),
        'firefox_organizations': (
            'css/firefox/organizations.less',
        ),
        'firefox_security': (
            'css/firefox/security.less',
        ),
        'firefox_speed': (
            'css/firefox/speed.less',
        ),
        'firefox_technology': (
            'css/firefox/technology.less',
            'css/firefox/technology-demos.css',
        ),
        'firefox_updates': (
            'css/mozilla-expanders.less',
            'css/firefox/update.less',
        ),
        'home': (
            'css/home.less',
        ),
        'marketplace': (
            'css/marketplace.less',
        ),
        'mission': (
            'css/sandstone/video.less',
            'css/mission.less',
        ),
        'mozilla_expanders': (
            'css/mozilla-expanders.less',
        ),
        'partnerships': (
            'css/partnerships.less',
        ),
        'persona': (
            'css/persona.less',
        ),
        'privacy': (
            'css/privacy.less',
        ),
        'projects': (
            'css/projects.less',
        ),
        'research': (
            'css/research/research.less',
        ),
        'sandstone_guide': (
            'css/sandstone-guide.less',
        ),
        'video': (
            'css/sandstone/video.less',
        ),
        'landing_devices': (
            'css/landing/devices.less',
            'css/firefox/template.less'
        ),
        'page_not_found': (
            'css/page-not-found.less',
        ),
    },
    'js': {
        'site': (
            'js/site.js',  # this is automatically included on every page
        ),
        'webmaker': (
            'js/webmaker/feeds.js',
        ),
        'collusion': (
            'js/collusion/d3.layout.js',
            'js/collusion/d3.geom.js',
            'js/collusion/collusion-addon.js',
            'js/collusion/demo.js',
            'js/collusion/graphrunner.js',
        ),
        'common': (
            'js/libs/jquery-1.7.1.min.js',
            'js/global.js',
            'js/footer-email-form.js',
            'js/mozilla-input-placeholder.js',
        ),
        'contribute': (
            'js/contribute-page.js',
            'js/mozilla-pager.js',
            'js/mozilla-video-tools.js',
        ),
        'contribute-form': (
            'js/contribute-form.js',
            'js/mozilla-input-placeholder.js',
        ),
        'expanders': (
            'js/mozilla-expanders.js',
        ),
        'firefox': (
            'js/libs/jquery-1.7.1.min.js',
            'js/global.js',
            'js/nav-main.js',
            'js/footer-email-form.js',
        ),
        'firefox_central': (
            'js/mozilla-video-tools.js',
            'js/firefox/central.js',
            'js/mozilla-pager.js',
        ),
        'firefox_channel': (
            'js/mozilla-pager.js',
            'js/firefox/channel.js',
        ),
        'firefox_customize': (
            'js/mozilla-video-tools.js',
            'js/firefox/customize.js',
        ),
        'firefox_features': (
            'js/mozilla-video-tools.js',
            'js/firefox/features.js',
        ),
        'firefox_happy': (
            'js/libs/jquery-1.4.4.min.js',
            'js/libs/jquery-css-transform.js',
            'js/libs/jquery-animate-css-rotate-scale.js',
        ),
        'firefox_speed': (
            'js/libs/jquery-1.4.4.min.js',
            'js/libs/jquery-css-transform.js',
            'js/libs/jquery-animate-css-rotate-scale.js',
        ),
        'geolocation': (
            'js/libs/jquery-1.4.4.min.js',
            'js/libs/jquery.nyroModal.pack.js',
            'js/mozilla-expanders.js',
            'js/geolocation-demo.js',
            'js/footer-email-form.js',
        ),
        'marketplace': (
            'js/mozilla-video-tools.js',
        ),
        'marketplace-partners': (
            'js/mozilla-pager.js',
            'js/mozilla-video-tools.js',
            'js/marketplace/partners.js',
        ),
        'pager': (
            'js/mozilla-pager.js',
        ),
        'partnerships': (
            'js/libs/jquery.validate.js',
            'js/partnerships.js',
        ),
        'video': (
            'js/mozilla-video-tools.js',
        ),
        'landing_devices': (
            'js/libs/jquery-1.4.4.min.js',
            'js/libs/jquery-css-transform.js',
            'js/libs/jquery-animate-css-rotate-scale.js',
            'js/global.js',
            'js/nav-main.js',
            'js/libs/jquery.cycle.all.js',
            'js/libs/jquery.ba-hashchange.min.js',
            'js/landing/devices.js'
        ),
    }
}

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS = {
    'messages': [
        ('apps/**.py',
            'tower.management.commands.extract.extract_tower_python'),
        ('apps/**/templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
        ('templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
    ],
}

# Dynamically process LESS server-side? (usually true to local
# development)
LESS_PREPROCESS = False
LESS_BIN = 'lessc'

# Override this because we've moved settings into a directory
PROD_DETAILS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'lib/product_details_json')

MIDDLEWARE_CLASSES = (
    'funfactory.middleware.LocaleURLMiddleware',
    #'multidb.middleware.PinningRouterMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'mozorg.middleware.NoVarySessionMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'session_csrf.CsrfMiddleware',  # Must be after auth middleware.
    #'django.contrib.messages.middleware.MessageMiddleware',
    'commonware.middleware.FrameOptionsHeader',
    #'mobility.middleware.DetectMobileMiddleware',
    #'mobility.middleware.XMobileMiddleware',
    'mozorg.middleware.CacheMiddleware'
)

INSTALLED_APPS = (
    # Local apps
    'funfactory',  # Content common to most playdoh-based apps.
    'jingo_minify',
    'tower',  # for ./manage.py extract (L10n)

    # Django contrib apps
    'django.contrib.auth',
    'django_sha2',  # Load after auth to monkey-patch it.
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    # 'django.contrib.sites',
    # 'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # Third-party apps, patches, fixes
    'commonware.response.cookies',
    'djcelery',
    'django_nose',
    'cronjobs',
    #'session_csrf',

    # L10n
    'product_details',

    # Local apps
    'b2g',
    'webmaker',
    'collusion',
    'firefox',
    'marketplace',
    'mozorg',
    'persona',
    'landing',
    'research',
    'privacy',

    # libs
    'l10n_utils',
    'captcha'
)

## Auth
PWD_ALGORITHM = 'bcrypt'
HMAC_KEYS = {
    #'2011-01-01': 'cheesecake',
}

FEEDS = {
    'mozilla': 'http://blog.mozilla.org/feed/'
}

GMAP_API_KEY = ''

BASKET_URL = 'http://basket.mozilla.com'

# This prefixes /b/ on all URLs generated by `reverse` so that links
# work on the dev site while we have a mix of Python/PHP
FORCE_SLASH_B = False

# Locals with transitional download pages
LOCALES_WITH_TRANSITION = ['en-US', 'af', 'ar', 'ast', 'be', 'bg',
                           'bn-BD', 'bn-IN', 'ca', 'cs', 'cy', 'da',
                           'de', 'el', 'eo', 'es-AR', 'es-CL', 'es-ES',
                           'es-MX', 'et', 'eu', 'fa', 'fi', 'fr',
                           'fy-NL', 'ga-IE', 'gd', 'gl', 'gu-IN',
                           'he', 'hi-IN', 'hr', 'hu', 'hy-AM', 'id',
                           'is', 'it', 'ja', 'kk', 'kn', 'ko', 'ku',
                           'lt', 'lv', 'mk', 'ml', 'mr', 'nb-NO',
                           'nl', 'or', 'pa-IN', 'pl', 'pt-BR', 'pt-PT',
                           'rm', 'ro', 'ru', 'si', 'sk', 'sl', 'sq',
                           'sr', 'sv-SE', 'ta', 'ta-LK', 'te', 'th',
                           'tr', 'uk', 'vi', 'zh-CN', 'zh-TW'];

# reCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
