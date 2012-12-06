# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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
NEWSLETTER_LANGUAGES = ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru']

FEED_CACHE = 3900
DOTLANG_CACHE = 60

DOTLANG_FILES = ['main', 'base', 'newsletter']

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1iz#v0m55@h26^m6hxk3a7at*h$qj_2a$juu1#nv50548j(x1v'

TEMPLATE_DIRS = (
    path('templates'),
    path('locale')
)


# has to stay a callable because tower expects that.
def JINJA_CONFIG():
    return {
        'extensions': [
            'l10n_utils.template.i18n', 'jinja2.ext.do', 'jinja2.ext.with_',
            'jinja2.ext.loopcontrols', 'l10n_utils.template.l10n_blocks',
            'l10n_utils.template.lang_blocks'
        ],
        # Make None in templates render as ''
        'finalize': lambda x: x if x is not None else '',
        'auto_reload': True,
    }


# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'about': (
            'css/about.less',
        ),
        'mobile_overview': (
            'css/mobile.less',
        ),
        'firefoxos': (
            'css/firefoxos.less',
        ),
        'gameon': (
            'css/gameon.less',
        ),
        'grants': (
            'css/grants.less',
        ),
        'collusion': (
            'css/collusion.less',
        ),
        'itu': (
            'css/itu.less',
        ),
        'common': (
            'css/sandstone/sandstone.less',
        ),
        'responsive': (
            'css/sandstone/sandstone-resp.less',
        ),
        'contribute': (
            'css/contribute.less',
            'css/sandstone/video-resp.less',
        ),
        'contribute-page': (
            'css/contribute-page.less',
        ),
        'channel': (
            'css/covehead/template.css',
            'css/covehead/content.css',
            'css/covehead/channel.css',
        ),
        'dnt': (
            'css/mozilla-expanders.less',
            'css/firefox/dnt.less',
        ),
        'firefox': (
            'css/firefox/template.less',
        ),
        'firefox-resp': (
            'css/firefox/template-resp.less',
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
        'firefox_devices': (
            'css/firefox/devices.less',
            'css/firefox/template.less'
        ),
        'firefox_features': (
            'css/sandstone/video.less',
            'css/firefox/features.less',
        ),
        'mobile_features': (
            'css/firefox/template-resp.less',
            'css/firefox/mobile-features.less',
        ),
        'firefox_sms': (
            'css/firefox/template-resp.less',
            'css/sandstone/video-resp.less',
            'css/firefox/mobile-sms.less',
        ),
        'firefox_faq': (
            'css/firefox/template-resp.less',
            'css/mozilla-expanders.less',
        ),
        'firefox_firstrun': (
            'css/sandstone/video.less',
            'css/firefox/firstrun.less',
        ),
        'firefox_fx': (
            'css/firefox/fx.less',
            'css/sandstone/video.less',
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
        'firefox_platforms': (
            'css/firefox/template-resp.less',
            'css/mozilla-expanders.less',
            'css/firefox/platforms.less',
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
        'firefox_whatsnew': (
            'css/sandstone/video.less',
            'css/firefox/whatsnew.less',
            'css/firefox/whatsnew-android.less',
        ),
        'installer_help': (
            'css/firefox/template-resp.less',
            'css/firefox/installer-help.less',
        ),
        'home': (
            'css/home.less',
        ),
        'marketplace': (
            'css/marketplace.less',
        ),
        'mission': (
            'css/sandstone/video-resp.less',
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
        'fb_privacy': (
            'css/fb-privacy.less',
        ),
        'products': (
            'css/products.less',
        ),
        'projects_mozilla_based': (
            'css/projects/mozilla-based.less',
        ),
        'research': (
            'css/research/research.less',
        ),
        'sandstone_guide': (
            'css/sandstone-guide.less',
        ),
        'styleguide': (
            'css/styleguide/styleguide.less',
            'css/styleguide/websites-sandstone.less',
            'css/styleguide/identity-mozilla.less',
            'css/styleguide/identity-firefox.less',
            'css/styleguide/identity-firefox-family.less',
            'css/styleguide/identity-firefoxos.less',
            'css/styleguide/identity-marketplace.less',
            'css/styleguide/identity-thunderbird.less',
            'css/styleguide/identity-webmaker.less',
            'css/styleguide/communications.less',
            'css/styleguide/products-firefox-os.less',
        ),
        'video': (
            'css/sandstone/video.less',
        ),
        'page_not_found': (
            'css/page-not-found.less',
        ),
        'annual_2011': (
            'css/foundation/annual2011.less',
        ),
    },
    'js': {
        'site': (
            'js/site.js',  # this is automatically included on every page
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
        'firefox-resp': (
            'js/libs/jquery-1.7.1.min.js',
            'js/global.js',
            'js/nav-main-resp.js',
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
        'firefox_fx': (
            'js/mozilla-pager.js',
            'js/mozilla-video-tools.js',
        ),
        'firefox_happy': (
            'js/libs/jquery-1.4.4.min.js',
            'js/firefox/happy.js',
        ),
        'firefox_platforms': (
            'js/mozilla-expanders.js',
        ),
        'firefox_faq': (
            'js/mozilla-expanders.js',
        ),
        'firefox_speed': (
            'js/libs/jquery-1.4.4.min.js',
            'js/firefox/speed.js',
        ),
        'firefox_tech': (
            'js/firefox/technology/tech.js',
        ),
        'firefox_sms': (
            'js/firefox/sms.js',
            'js/libs/socialshare.min.js',
        ),
        'geolocation': (
            'js/libs/jquery-1.4.4.min.js',
            'js/libs/jquery.nyroModal.pack.js',
            'js/mozilla-expanders.js',
            'js/geolocation-demo.js',
            'js/footer-email-form.js',
        ),
        'marketplace': (
            'js/nav-main-resp.js',
            'js/mozilla-pager.js',
            'js/marketplace/marketplace.js',
        ),
        'box2d': (
            'js/libs/jquery-box2dweb/Box2dWeb-2.1.a.3.js',
            'js/libs/jquery-box2dweb/jQbox2D.Alpha.js',
        ),
        'mozorg-resp': (
            'js/libs/jquery-1.7.1.min.js',
            'js/global.js',
            'js/nav-main-resp.js',
            'js/footer-email-form.js',
        ),
        'pager': (
            'js/mozilla-pager.js',
        ),
        'partnerships': (
            'js/libs/jquery.validate.js',
            'js/partnerships.js',
            'js/mozilla-input-placeholder.js',
        ),
        'privacy': (
            'js/mozilla-pager.js',
            'js/privacy.js',
        ),
        'styleguide': (
            'js/styleguide.js',
        ),
        'video': (
            'js/mozilla-video-tools.js',
        ),
        'firefox_devices': (
            'js/libs/jquery-1.4.4.min.js',
            'js/global.js',
            'js/nav-main.js',
            'js/libs/jquery.cycle.all.js',
            'js/libs/jquery.ba-hashchange.min.js',
            'js/firefox/devices.js'
        ),
        'mosaic': (
            'js/libs/modernizr.custom.26887.js',
            'js/libs/jquery.transit.min.js',
            'js/libs/jquery.gridrotator.js',
        ),
        'annual_2011': (
            'js/libs/jquery.hoverIntent.minified.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.jcarousel.min.js',
            'js/annual2011.js',
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
    'mozorg.middleware.MozorgRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'funfactory.middleware.LocaleURLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'commonware.middleware.FrameOptionsHeader',
    'mozorg.middleware.CacheMiddleware',
    'mozorg.middleware.NewsletterMiddleware',
    'dnt.middleware.DoNotTrackMiddleware',
    'l10n_utils.middleware.FixLangFileTranslationsMiddleware',
)

INSTALLED_APPS = (
    # Local apps
    'funfactory',  # Content common to most playdoh-based apps.
    'jingo_minify',
    'tower',  # for ./manage.py extract (L10n)
    'django_statsd',

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
    'firefoxos',
    'foundation',
    'gameon',
    'grants',
    'collusion',
    'firefox',
    'marketplace',
    'mozorg',
    'persona',
    'research',
    'styleguide',
    'privacy',
    'redirects',
    'legal',

    # libs
    'l10n_utils',
    'captcha',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'mozorg.context_processors.current_year',
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
                           'tr', 'uk', 'vi', 'zh-CN', 'zh-TW']

# reCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_USE_SSL = True

TEST_RUNNER = 'test_utils.runner.NoDBTestSuiterunner'


def lazy_email_backend():
    from django.conf import settings
    return ('django.core.mail.backends.console.EmailBackend' if settings.DEBUG
            else 'django.core.mail.backends.smtp.EmailBackend')

EMAIL_BACKEND = lazy(lazy_email_backend, str)()

AURORA_STUB_INSTALLER = False

# Google Analytics
GA_ACCOUNT_CODE = ''
