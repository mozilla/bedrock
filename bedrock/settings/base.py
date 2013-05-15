# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Django settings file for bedrock.

import os

from django.utils.functional import lazy

from funfactory.settings_base import *  # noqa

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

# Accepted locales
PROD_LANGUAGES = ('ach', 'af', 'ak', 'an', 'ar', 'as', 'ast', 'be', 'bg',
                  'bn-BD', 'bn-IN', 'br', 'bs', 'ca', 'cs', 'csb', 'cy',
                  'da', 'de', 'el', 'en-GB', 'en-US', 'en-ZA', 'eo', 'es-AR',
                  'es-CL', 'es-ES', 'es-MX', 'et', 'eu', 'fa', 'ff', 'fi', 'fr',
                  'fy-NL', 'ga-IE', 'gd', 'gl', 'gu-IN', 'he', 'hi-IN', 'hr',
                  'hu', 'hy-AM', 'id', 'is', 'it', 'ja', 'ja-JP-mac',
                  'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'lg', 'lij', 'lt', 'lv',
                  'mai', 'mk', 'ml', 'mn', 'mr', 'ms', 'my', 'nb-NO', 'nl',
                  'nn-NO', 'nso', 'oc', 'or', 'pa-IN', 'pl', 'pt-BR', 'pt-PT',
                  'rm', 'ro', 'ru', 'sah', 'si', 'sk', 'sl', 'son', 'sq', 'sr',
                  'sv-SE', 'sw', 'ta', 'ta-LK', 'te', 'th', 'tr', 'uk',
                  'ur', 'vi', 'wo', 'zh-CN', 'zh-TW', 'zu')
DEV_LANGUAGES = list(DEV_LANGUAGES) + ['en-US']
NEWSLETTER_LANGUAGES = ['de', 'en', 'es', 'fr', 'id', 'pt', 'ru']

FEED_CACHE = 3900
DOTLANG_CACHE = 60

DOTLANG_FILES = ['main', 'download_button', 'newsletter']

# Paths that don't require a locale code in the URL.
# matches the first url component (e.g. mozilla.org/gameon/)
SUPPORTED_NONLOCALES += [
    # from redirects.urls
    'telemetry',
    'webmaker',
    'gameon',
]

ALLOWED_HOSTS = [
    'www.mozilla.org',
    'www.ipv6.mozilla.org',
    'www.allizom.org',
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ssssshhhhh'

TEMPLATE_DIRS = (
    path('locale'),
)


# has to stay a callable because tower expects that.
def JINJA_CONFIG():
    return {
        'extensions': [
            'lib.l10n_utils.template.i18n', 'jinja2.ext.do', 'jinja2.ext.with_',
            'jinja2.ext.loopcontrols', 'lib.l10n_utils.template.l10n_blocks',
            'lib.l10n_utils.template.lang_blocks'
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
            'css/mozorg/about.less',
        ),
        'about-base': (
            'css/mozorg/about-base.less',
        ),
        'mobile_overview': (
            'css/mozorg/mobile.less',
        ),
        'firefoxos': (
            'css/firefoxos/firefoxos.less',
        ),
        'grants': (
            'css/grants/grants.less',
        ),
        'collusion': (
            'css/collusion/collusion.less',
        ),
        'itu': (
            'css/mozorg/itu.less',
        ),
        'common': (
            'css/sandstone/sandstone.less',
        ),
        'responsive': (
            'css/sandstone/sandstone-resp.less',
        ),
        'contribute': (
            'css/mozorg/contribute.less',
            'css/sandstone/video-resp.less',
            'css/mozorg/mozilla15.less',
        ),
        'contribute-page': (
            'css/mozorg/contribute-page.less',
        ),
        'contribute-university-ambassadors': (
            'css/mozorg/contribute-ambassadors.less',
        ),
        'dnt': (
            'css/base/mozilla-expanders.less',
            'css/firefox/dnt.less',
        ),
        'firefox': (
            'css/firefox/template.less',
        ),
        'firefox_all': (
            'css/firefox/all.less',
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
            'css/base/mozilla-expanders.less',
        ),
        'firefox_firstrun': (
            'css/sandstone/video.less',
            'css/firefox/firstrun.less',
        ),
        'nightly_firstrun': (
            'css/sandstone/video.less',
            'css/firefox/nightly_firstrun.less',
        ),
        'firefox_firstrun_new_a': (
            'css/sandstone/video.less',
            'css/firefox/firstrun/a.less',
        ),
        'firefox_firstrun_new_b': (
            'css/sandstone/video.less',
            'css/firefox/firstrun/b.less',
        ),
        'firefox_fx': (
            'css/firefox/fx.less',
            'css/sandstone/video.less',
        ),
        'firefox_geolocation': (
            'css/base/mozilla-expanders.less',
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
            'css/base/mozilla-expanders.less',
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
            'css/base/mozilla-expanders.less',
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
            'css/mozorg/home.less',
            'js/libs/video-js/video-js.css',
            'js/libs/video-js/video-js-sandstone.css',
        ),
        'marketplace': (
            'css/marketplace/marketplace.less',
        ),
        'mission': (
            'css/sandstone/video-resp.less',
            'css/mozorg/mission.less',
        ),
        'mozilla_expanders': (
            'css/base/mozilla-expanders.less',
        ),
        'partnerships': (
            'css/mozorg/partnerships.less',
        ),
        'persona': (
            'css/persona/persona.less',
        ),
        'powered-by': (
            'css/mozorg/powered-by.less',
        ),
        'plugincheck': (
            'css/plugincheck/plugincheck.less',
            'css/plugincheck/qtip.css',
        ),
        'privacy': (
            'css/privacy/privacy.less',
        ),
        'fb_privacy': (
            'css/privacy/fb-privacy.less',
        ),
        'products': (
            'css/mozorg/products.less',
        ),
        'projects_mozilla_based': (
            'css/mozorg/projects-mozilla-based.less',
        ),
        'research': (
            'css/research/research.less',
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
        'tabzilla': (
            'css/tabzilla/tabzilla.less',
        ),
        'video': (
            'css/sandstone/video.less',
        ),
        'page_not_found': (
            'css/base/page-not-found.less',
        ),
        'annual_2011': (
            'css/foundation/annual2011.less',
        ),
        'partners': (
            'css/libs/jquery.pageslide.css',
            'css/firefox/partners.less',
        ),
        'partners-ie7': (
            'css/firefox/partners/ie7.less',
        ),
        'facebookapps_downloadtab': (
            'css/libs/h5bp_main.css',
            'css/facebookapps/downloadtab.less',
        ),
    },
    'js': {
        'site': (
            'js/base/site.js',  # this is automatically included on every page
        ),
        'collusion': (
            'js/collusion/collusion.js',
            'js/libs/jquery.validate.js',
        ),
        'collusion_demo': (
            'js/collusion/d3.layout.js',
            'js/collusion/d3.geom.js',
            'js/collusion/collusion-addon.js',
            'js/collusion/demo.js',
            'js/collusion/graphrunner.js',
        ),
        'common': (
            'js/libs/jquery-1.7.1.min.js',
            'js/base/global.js',
            'js/base/footer-email-form.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'common-resp': (
            'js/libs/jquery-1.7.1.min.js',
            'js/base/global.js',
            'js/base/nav-main-resp.js',
            'js/base/footer-email-form.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'contribute': (
            'js/libs/jquery.sequence.js',
            'js/mozorg/mozilla15.js',
            'js/mozorg/contribute-page.js',
            'js/base/mozilla-pager.js',
            'js/base/mozilla-video-tools.js',
        ),
        'contribute-form': (
            'js/mozorg/contribute-form.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'contribute-university-ambassadors': (
            'js/mozorg/contribute-university-ambassadors.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'expanders': (
            'js/base/mozilla-expanders.js',
        ),
        'firefox': (
            'js/libs/jquery-1.7.1.min.js',
            'js/base/global.js',
            'js/base/nav-main.js',
            'js/base/footer-email-form.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'firefox_all': (
            'js/firefox/firefox-language-search.js',
        ),
        'firefox-resp': (
            'js/libs/jquery-1.7.1.min.js',
            'js/base/global.js',
            'js/base/nav-main-resp.js',
            'js/base/footer-email-form.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'firefox_central': (
            'js/base/mozilla-video-tools.js',
            'js/firefox/central.js',
            'js/base/mozilla-pager.js',
        ),
        'firefox_channel': (
            'js/base/mozilla-pager.js',
            'js/firefox/channel.js',
        ),
        'firefox_customize': (
            'js/base/mozilla-video-tools.js',
            'js/firefox/customize.js',
        ),
        'firefox_features': (
            'js/base/mozilla-video-tools.js',
            'js/firefox/features.js',
        ),
        'firefox_firstrun': (
            'js/firefox/firstrun/firstrun.js',
        ),
        'firefox_firstrun_new_a': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/base/mozilla-modal.js',
            'js/firefox/firstrun/common.js',
            'js/firefox/firstrun/a.js',
        ),
        'firefox_firstrun_new_b': (
            'js/base/mozilla-modal.js',
            'js/firefox/firstrun/common.js',
        ),
        'firefox_fx': (
            'js/base/mozilla-pager.js',
            'js/base/mozilla-video-tools.js',
        ),
        'firefox_happy': (
            'js/libs/jquery-1.4.4.min.js',
            'js/firefox/happy.js',
        ),
        'firefox_new': (
            'js/libs/modernizr.custom.csstransitions.js',
            'js/firefox/new.js',
        ),
        'firefox_platforms': (
            'js/base/mozilla-expanders.js',
        ),
        'firefox_faq': (
            'js/base/mozilla-expanders.js',
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
            'js/base/mozilla-expanders.js',
            'js/firefox/geolocation-demo.js',
            'js/base/footer-email-form.js',
        ),
        'home': (
            'js/base/mozilla-pager.js',
            'js/libs/video-js/video.js',
            'js/mozorg/home.js'
        ),
        'marketplace': (
            'js/base/nav-main-resp.js',
            'js/base/mozilla-pager.js',
            'js/marketplace/marketplace.js',
        ),
        'mozorg-resp': (
            'js/libs/jquery-1.7.1.min.js',
            'js/base/global.js',
            'js/base/nav-main-resp.js',
            'js/base/footer-email-form.js',
        ),
        'pager': (
            'js/base/mozilla-pager.js',
        ),
        'partnerships': (
            'js/libs/jquery.validate.js',
            'js/mozorg/partnerships.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'plugincheck': (
            'js/plugincheck/plugincheck.min.js',
            'js/plugincheck/lib/mustache.js',
            'js/plugincheck/tmpl/plugincheck.ui.tmpl.js',
            'js/plugincheck/check-plugins.js',
        ),
        'privacy': (
            'js/base/mozilla-pager.js',
            'js/privacy/privacy.js',
        ),
        'privacy-firefoxos': (
            'js/privacy_firefoxos.js',
        ),
        'styleguide': (
            'js/styleguide/styleguide.js',
        ),
        'video': (
            'js/base/mozilla-video-tools.js',
        ),
        'firefox_devices': (
            'js/libs/jquery-1.4.4.min.js',
            'js/base/global.js',
            'js/base/nav-main.js',
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
            'js/foundation/annual2011.js',
        ),
        'partners': (
            'js/libs/modernizr.custom.shiv-load.js',
            'js/base/mozilla-input-placeholder.js',
            'js/base/mozilla-pager.js',
            'js/firefox/partners.js',
        ),
        'partners_common': (
            'js/libs/enquire.min.js',
            'js/firefox/partners/common.js',
        ),
        'partners_mobile': (
            'js/firefox/partners/mobile.js',
        ),
        'partners_desktop': (
            'js/libs/jquery.pageslide.min.js',
            'js/libs/tweenmax.min.js',
            'js/libs/superscrollorama.js',
            'js/libs/jquery.spritely-0.6.1.js',
            'js/firefox/partners/desktop.js',
        ),
        'facebookapps_redirect': (
            'js/libs/jquery-1.7.1.min.js',
            'js/facebookapps/redirect.js',
        ),
        'facebookapps_downloadtab': (
            'js/facebookapps/downloadtab-init.js',
            'js/facebookapps/Base.js',
            'js/facebookapps/Facebook.js',
            'js/facebookapps/Theater.js',
            'js/facebookapps/Slider.js',
            'js/facebookapps/App.js',
            'js/facebookapps/downloadtab.js',
        ),
    }
}

PROJECT_MODULE = 'bedrock'

ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS = {
    'messages': [
        ('%s/**.py' % PROJECT_MODULE,
            'tower.management.commands.extract.extract_tower_python'),
        ('%s/**/templates/**.html' % PROJECT_MODULE,
            'tower.management.commands.extract.extract_tower_template'),
        ('%s/**/templates/**.js' % PROJECT_MODULE,
            'tower.management.commands.extract.extract_tower_template'),
    ],
}

# Dynamically process LESS server-side? (usually true to local
# development)
LESS_PREPROCESS = False
LESS_BIN = 'lessc'

MIDDLEWARE_CLASSES = (
    'bedrock.mozorg.middleware.MozorgRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'bedrock.tabzilla.middleware.TabzillaLocaleURLMiddleware',
) + get_middleware(exclude=(
    'funfactory.middleware.LocaleURLMiddleware',
    'multidb.middleware.PinningRouterMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_csrf.CsrfMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'mobility.middleware.DetectMobileMiddleware',
    'mobility.middleware.XMobileMiddleware',
), append=(
    'bedrock.mozorg.middleware.CacheMiddleware',
    'bedrock.mozorg.middleware.NewsletterMiddleware',
    'dnt.middleware.DoNotTrackMiddleware',
    'lib.l10n_utils.middleware.FixLangFileTranslationsMiddleware',
))

INSTALLED_APPS = get_apps(exclude=(
    'compressor',
    'django_browserid',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'session_csrf',
), append=(
    # Local apps
    'jingo_minify',
    'django_statsd',

    # Django contrib apps
    'django_sha2',  # Load after auth to monkey-patch it.
    
    # Local apps
    '%s.base' % PROJECT_MODULE,
    '%s.collusion' % PROJECT_MODULE,
    '%s.firefox' % PROJECT_MODULE,
    '%s.foundation' % PROJECT_MODULE,
    '%s.grants' % PROJECT_MODULE,
    '%s.legal' % PROJECT_MODULE,
    '%s.marketplace' % PROJECT_MODULE,
    '%s.mozorg' % PROJECT_MODULE,
    '%s.persona' % PROJECT_MODULE,
    '%s.privacy' % PROJECT_MODULE,
    '%s.redirects' % PROJECT_MODULE,
    '%s.research' % PROJECT_MODULE,
    '%s.styleguide' % PROJECT_MODULE,
    '%s.tabzilla' % PROJECT_MODULE,
    '%s.facebookapps' % PROJECT_MODULE,

    # libs
    'lib.l10n_utils',
    'captcha',
))

LOCALE_PATHS = (
    path('locale'),
)

TEMPLATE_CONTEXT_PROCESSORS = get_template_context_processors(append=(
    'bedrock.mozorg.context_processors.current_year',
))

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

# Locales showing the 15th Anniversary slideshow on /contribute
LOCALES_WITH_MOZ15 = ['de', 'el', 'en-GB', 'en-US', 'es-AR', 'es-CL', 'es-ES',
                      'es-MX', 'fr', 'id', 'nl', 'pt-BR', 'ru', 'sq', 'zh-CN',
                      'zh-TW']

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

FACEBOOK_LOCALES = ['en-US', 'es-ES', 'pt-BR', 'id', 'de']
FACEBOOK_PAGE_NAMESPACE = 'DUMMY_PAGE_NAMESPACE'
FACEBOOK_APP_ID = 'DUMMY_APP_ID'


# FACEBOOK_TAB_URL is lazily evaluated because it depends on the namespace
# and app ID settings in local settings.
def facebook_tab_url_lazy():
    from django.conf import settings
    return '//www.facebook.com/{page}/app_{id}'.format(page=settings.FACEBOOK_PAGE_NAMESPACE, id=settings.FACEBOOK_APP_ID)
FACEBOOK_TAB_URL = lazy(facebook_tab_url_lazy, str)()

# Prefix for media. No trailing slash.
# e.g. '//mozorg.cdn.mozilla.net'
CDN_BASE_URL = ''
