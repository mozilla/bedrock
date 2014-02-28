# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Django settings file for bedrock.

from django.utils.functional import lazy

from funfactory.settings_base import *  # noqa

# Production uses MySQL, but Sqlite should be sufficient for local development.
# Our CI server tests against MySQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'bedrock.db',
    }
}

# Override in local.py for memcached.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'translations'
    }
}

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

# Accepted locales
PROD_LANGUAGES = ('ach', 'af', 'ak', 'an', 'ar', 'as', 'ast', 'az', 'be', 'bg',
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
                  'ur', 'vi', 'wo', 'xh', 'zh-CN', 'zh-TW', 'zu')
DEV_LANGUAGES = list(DEV_LANGUAGES) + ['en-US']

FEED_CACHE = 3900
DOTLANG_CACHE = 600

DOTLANG_FILES = ['main', 'download_button', 'newsletter']

# Paths that don't require a locale code in the URL.
# matches the first url component (e.g. mozilla.org/gameon/)
SUPPORTED_NONLOCALES += [
    # from redirects.urls
    'telemetry',
    'webmaker',
    'gameon',
    'robots.txt',
]

ALLOWED_HOSTS = [
    'www.mozilla.org',
    'www.ipv6.mozilla.org',
    'www.allizom.org',
]

# The canonical, production URL without a trailing slash
CANONICAL_URL = 'http://www.mozilla.org'

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
            'lib.l10n_utils.template.lang_blocks',
            'jingo_markdown.extensions.MarkdownExtension',
        ],
        # Make None in templates render as ''
        'finalize': lambda x: x if x is not None else '',
        'auto_reload': True,
    }

JINGO_MINIFY_USE_STATIC = False
CACHEBUST_IMGS = False

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'csrf-failure': (
            'css/csrf-failure.less',
        ),
        'about': (
            'css/mozorg/about.less',
        ),
        'about-base': (
            'css/mozorg/about-base.less',
        ),
        'foundation': (
            'css/foundation/foundation.less',
        ),
        'gigabit': (
            'css/gigabit/gigabit.less',
        ),
        'grants': (
            'css/grants/grants.less',
        ),
        'lightbeam': (
            'css/lightbeam/lightbeam.less',
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
        'newsletter': (
            'css/newsletter/newsletter.less',
        ),
        'contact-spaces': (
            'css/libs/mapbox.css',
            'css/libs/magnific-popup.css',
            'css/mozorg/contact-spaces.less',
        ),
        'contact-spaces-ie8': (
            'css/libs/mapbox.ie.css',
        ),
        'contact-spaces-ie7': (
            'css/mozorg/contact-spaces-ie7.less',
        ),
        'contribute': (
            'css/mozorg/contribute.less',
            'css/sandstone/video-resp.less',
            'css/mozorg/mozilla15.less',
        ),
        'contribute-page': (
            'css/mozorg/contribute-page.less',
        ),
        'contribute-studentambassadors-landing': (
            'css/mozorg/contribute/studentambassadors/landing.less',
        ),
        'contribute-studentambassadors-join': (
            'css/mozorg/contribute/studentambassadors/join.less',
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
        'firefox_unsupported': (
            'css/firefox/unsupported.less',
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
        'firefox_features': (
            'css/sandstone/video.less',
            'css/firefox/features.less',
        ),
        'mobile_features': (
            'css/firefox/template-resp.less',
            'css/firefox/mobile-features.less',
        ),
        'firefox_sms': (
            'css/libs/socialshare/socialshare.less',
            'css/firefox/template-resp.less',
            'css/sandstone/video-resp.less',
            'css/firefox/mobile-sms.less',
        ),
        'firefox_faq': (
            'css/firefox/faq.less',
            'css/firefox/template-resp.less',
            'css/base/mozilla-expanders.less',
        ),
        'firefox_firstrun': (
            'css/sandstone/video.less',
            'css/base/mozilla-modal.less',
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
            'css/base/mozilla-modal.less',
            'css/libs/mapbox.css',
            'css/firefox/geolocation.less'
        ),
        'firefox_happy': (
            'css/firefox/happy.less',
        ),
        'firefox_new': (
            'css/libs/socialshare/socialshare.less',
            'css/firefox/new.less',
        ),
        'firefox_organizations': (
            'css/firefox/organizations.less',
        ),
        'firefox_os': (
            'css/base/mozilla-modal.less',
            'css/libs/jquery.pageslide.css',
            'css/firefox/os/firefox-os.less',
        ),
        'firefox_os_ie': (
            'css/firefox/os/firefox-os-ie.less',
        ),
        'firefox_os_devices': (
            'css/libs/tipsy.css',
            'css/base/mozilla-modal.less',
            'css/firefox/os/devices.less',
        ),
        'firefox_os_devices_ie': (
            'css/firefox/os/devices-ie.less',
        ),
        'firefox_os_mwc_2014_preview': (
            'css/base/mozilla-modal.less',
            'css/firefox/os/mwc-2014-preview.less',
        ),
        'firefox_os_mwc_2014_preview_ie7': (
            'css/firefox/os/mwc-2014-preview-ie7.less',
        ),
        'firefox_releases_index': (
            'css/firefox/releases-index.less',
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
        'firefox_whatsnew': (
            'css/sandstone/video.less',
            'css/firefox/whatsnew.less',
            'css/firefox/whatsnew-android.less',
        ),
        'firefox_whatsnew_aurora_29': (
            'css/firefox/australis/australis-ui-tour.less',
            'css/firefox/australis/aurora-whatsnew.less',
        ),
        'firefox_whatsnew_fxos': (
            'css/firefox/whatsnew-fxos.less',
        ),
        'firefox_windows_8_touch': (
            'css/firefox/windows-8-touch.less',
        ),
        'firefox_releasenotes': (
            'css/firefox/releasenotes.less',
        ),
        'installer_help': (
            'css/base/mozilla-modal.less',
            'css/firefox/template-resp.less',
            'css/firefox/installer-help.less',
        ),
        'home': (
            'css/mozorg/home.less',
            'css/mozorg/home-promo.less',
        ),
        'home-ie9': (
            'css/mozorg/home-ie9.less',
        ),
        'home-ie8': (
            'css/mozorg/home-ie8.less',
        ),
        'home-ie': (
            'css/mozorg/home-ie.less',
        ),
        'legal_fraud_report': (
            'css/legal/fraud-report.less',
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
        'press_speaker_request': (
            'css/press/speaker-request.less',
        ),
        'privacy': (
            'css/privacy/privacy.less',
        ),
        'privacy-day': (
            'css/privacy/privacy-day.less',
        ),
        'fb_privacy': (
            'css/privacy/fb-privacy.less',
        ),
        'web-privacy': (
            'css/privacy/web-privacy.less',
        ),
        'products': (
            'css/mozorg/products.less',
        ),
        'projects_mozilla_based': (
            'css/mozorg/projects/mozilla-based.less',
        ),
        'projects-calendar': (
            'css/mozorg/projects/calendar.less',
        ),
        'research': (
            'css/research/research.less',
        ),
        'security-tld-idn': (
            'css/mozorg/security-tld-idn.less',
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
        'video-resp': (
            'css/sandstone/video-resp.less',
        ),
        'page_not_found': (
            'css/base/page-not-found.less',
        ),
        'annual_2011': (
            'css/foundation/annual2011.less',
        ),
        'annual_2012': (
            'css/base/mozilla-modal.less',
            'css/foundation/annual2012.less',
        ),
        'partners': (
            'css/base/mozilla-modal.less',
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
        'lightbeam': (
            'js/lightbeam/d3.v3.min.js',
            'js/lightbeam/rAF.js',
            'js/lightbeam/lightbeam.js',
            'js/lightbeam/ui.js',
            'js/libs/jquery.validate.js',
        ),
        'projects-calendar': (
            'js/mozorg/calendar.js',
        ),
        'common': (
            'js/libs/jquery-1.7.1.min.js',
            'js/base/global.js',
            'js/base/footer-email-form.js',
            'js/base/mozilla-input-placeholder.js',
            'js/base/mozilla-image-helper.js',
        ),
        'common-resp': (
            'js/libs/jquery-1.7.1.min.js',
            'js/base/global.js',
            'js/base/nav-main-resp.js',
            'js/base/footer-email-form.js',
            'js/base/mozilla-input-placeholder.js',
            'js/base/mozilla-image-helper.js',
        ),
        'contact-spaces': (
            'js/libs/mapbox.js',
            'js/libs/jquery.history.js',
            'js/mozorg/contact-data.js',
            'js/libs/jquery.magnific-popup.min.js',
            'js/mozorg/contact-spaces.js',
        ),
        'contact-spaces-ie7': (
            'js/mozorg/contact-spaces-ie7.js',
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
        'contribute-studentambassadors-join': (
            'js/mozorg/contribute-studentambassadors-join.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'existing': (
            'js/newsletter/existing.js',
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
            'js/base/mozilla-image-helper.js',
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
            'js/base/mozilla-image-helper.js',
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
            'js/base/mozilla-modal.js',
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
            'js/firefox/fx.js',
        ),
        'firefox_happy': (
            'js/firefox/happy.js',
        ),
        'firefox_new': (
            'js/libs/socialshare.min.js',
            'js/libs/modernizr.custom.csstransitions.js',
            'js/firefox/new.js',
        ),
        'firefox_os': (
            'js/base/mozilla-modal.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/libs/tweenmax.1.9.7.min.js',
            'js/libs/superscrollorama-1.0.1.js',
            'js/libs/jquery.plusslider.js',
            'js/libs/jquery.color.js',
            'js/libs/script.js',
            'js/libs/socialshare.min.js',
            'js/firefox/os/partner_data.js',
            'js/firefox/os/firefox-os.js',
            'js/firefox/os/desktop.js',
            'js/firefox/os/have-it.js',
        ),
        'firefox_os_ie9': (
            'js/libs/matchMedia.addListener.js',
        ),
        'firefox_os_devices': (
            'js/libs/jquery.tipsy.js',
            'js/base/mozilla-pager.js',
            'js/base/mozilla-modal.js',
            'js/libs/matchMedia.js',
            'js/libs/matchMedia.addListener.js',
            'js/firefox/os/partner_data.js',
            'js/firefox/os/devices.js',
        ),
        'firefox_os_mwc_2014_preview': (
            'js/base/mozilla-modal.js',
            'js/firefox/mwc-2014-map.js',
            'js/firefox/os/mwc-2014-preview.js',
        ),
        'firefox_faq': (
            'js/base/mozilla-expanders.js',
        ),
        'firefox_speed': (
            'js/firefox/speed.js',
        ),
        'firefox_tech': (
            'js/firefox/technology/tech.js',
        ),
        'firefox_sms': (
            'js/firefox/sms.js',
            'js/libs/socialshare.min.js',
        ),
        'firefox_whatsnew_aurora_29': (
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/australis/browser-tour.js',
            'js/firefox/australis/aurora-whatsnew.js',
        ),
        'firefox_whatsnew_fxos': (
            'js/firefox/whatsnew-fxos.js',
        ),
        'geolocation': (
            'js/libs/mapbox.js',
            'js/base/mozilla-expanders.js',
            'js/firefox/geolocation-demo.js',
            'js/base/mozilla-modal.js',
        ),
        'home': (
            'js/libs/jquery.ellipsis.min.js',
            'js/libs/jquery.cycle2.min.js',
            'js/libs/jquery.cycle2.carousel.min.js',
            'js/mozorg/home.js',
        ),
        'installer_help': (
            'js/base/mozilla-modal.js',
            'js/firefox/installer-help.js',
        ),
        'legal_fraud_report': (
            'js/libs/jquery.validate.js',
            'js/legal/fraud-report.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'mozorg-resp': (
            'js/libs/jquery-1.11.0.min.js',
            'js/base/global.js',
            'js/base/nav-main-resp.js',
            'js/base/footer-email-form.js',
            'js/base/mozilla-image-helper.js',
        ),
        'pager': (
            'js/base/mozilla-pager.js',
        ),
        'partnerships': (
            'js/libs/jquery.validate.js',
            'js/base/mozilla-form-helper.js',
            'js/mozorg/partnerships.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'plugincheck': (
            'js/plugincheck/plugincheck.min.js',
            'js/plugincheck/lib/mustache.js',
            'js/plugincheck/tmpl/plugincheck.ui.tmpl.js',
            'js/plugincheck/check-plugins.js',
        ),
        'press_speaker_request': (
            'js/libs/jquery.validate.js',
            'js/libs/modernizr.custom.inputtypes.js',
            'js/press/speaker-request.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'privacy': (
            'js/base/mozilla-pager.js',
            'js/privacy/privacy.js',
        ),
        'privacy-day': (
            'js/privacy/privacy-day.js',
        ),
        'privacy-firefoxos': (
            'js/privacy_firefoxos.js',
        ),
        'products': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/mozorg/products.js',
        ),
        'styleguide': (
            'js/styleguide/styleguide.js',
        ),
        'video': (
            'js/base/mozilla-video-tools.js',
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
        'annual_2012': (
            'js/base/mozilla-modal.js',
            'js/foundation/annual2012.js',
        ),
        'partners': (
            'js/libs/modernizr.custom.shiv-load.js',
            'js/base/mozilla-input-placeholder.js',
            'js/base/mozilla-pager.js',
            'js/base/mozilla-modal.js',
            'js/firefox/mwc-2014-map.js',
            'js/firefox/partners.js',
        ),
        'partners_common': (
            'js/libs/enquire.min.js',
            'js/base/mozilla-form-helper.js',
            'js/firefox/partners/common.js',
        ),
        'partners_mobile': (
            'js/firefox/partners/mobile.js',
        ),
        'partners_desktop': (
            'js/libs/jquery.pageslide.min.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/tweenmax.1.9.7.min.js',
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
            'tower.extract_tower_python'),
        ('%s/**/templates/**.html' % PROJECT_MODULE,
            'tower.extract_tower_template'),
        ('%s/**/templates/**.js' % PROJECT_MODULE,
            'tower.extract_tower_template'),
        ('%s/**/templates/**.jsonp' % PROJECT_MODULE,
            'tower.extract_tower_template'),
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
    'commonware.middleware.RobotsTagHeader',
) + get_middleware(exclude=(
    'funfactory.middleware.LocaleURLMiddleware',
    'multidb.middleware.PinningRouterMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_csrf.CsrfMiddleware',
    'mobility.middleware.DetectMobileMiddleware',
    'mobility.middleware.XMobileMiddleware',
), append=(
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'bedrock.mozorg.middleware.CacheMiddleware',
    'dnt.middleware.DoNotTrackMiddleware',
    'lib.l10n_utils.middleware.FixLangFileTranslationsMiddleware',
))

INSTALLED_APPS = get_apps(exclude=(
    'compressor',
    'django_browserid',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'session_csrf',
    'djcelery',
), append=(
    # Local apps
    'jingo_markdown',
    'jingo_minify',
    'django_statsd',
    'waffle',
    'south',

    # Django contrib apps
    'django_sha2',  # Load after auth to monkey-patch it.
    'django.contrib.contenttypes',
    'django.contrib.messages',

    # Local apps
    '%s.base' % PROJECT_MODULE,
    '%s.lightbeam' % PROJECT_MODULE,
    '%s.firefox' % PROJECT_MODULE,
    '%s.foundation' % PROJECT_MODULE,
    '%s.gigabit' % PROJECT_MODULE,
    '%s.grants' % PROJECT_MODULE,
    '%s.legal' % PROJECT_MODULE,
    '%s.mozorg' % PROJECT_MODULE,
    '%s.newsletter' % PROJECT_MODULE,
    '%s.persona' % PROJECT_MODULE,
    '%s.press' % PROJECT_MODULE,
    '%s.privacy' % PROJECT_MODULE,
    '%s.redirects' % PROJECT_MODULE,
    '%s.research' % PROJECT_MODULE,
    '%s.styleguide' % PROJECT_MODULE,
    '%s.tabzilla' % PROJECT_MODULE,
    '%s.facebookapps' % PROJECT_MODULE,

    # libs
    'django_extensions',
    'lib.l10n_utils',
    'captcha',
    'rna',
))

LOCALE_PATHS = (
    path('locale'),
)

TEMPLATE_CONTEXT_PROCESSORS = get_template_context_processors(append=(
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
    'bedrock.mozorg.context_processors.canonical_path',
    'bedrock.mozorg.context_processors.current_year',
    'bedrock.mozorg.context_processors.funnelcake_param',
    'bedrock.mozorg.context_processors.facebook_locale',
    'bedrock.firefox.context_processors.latest_firefox_versions',
    'jingo_minify.helpers.build_ids',
))

## Auth
PWD_ALGORITHM = 'bcrypt'
HMAC_KEYS = {
    #'2011-01-01': 'cheesecake',
}

FEEDS = {
    'mozilla': 'https://blog.mozilla.org/feed/'
}

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
LOCALES_WITH_MOZ15 = ['ar', 'bg', 'cs', 'cy', 'de', 'el', 'en-GB', 'en-US', 'es-AR',
                      'es-CL', 'es-ES', 'es-MX', 'fr', 'fy-NL', 'hr', 'id', 'it',
                      'lt', 'ms', 'nl', 'pl', 'pt-BR', 'ro', 'ru', 'sl', 'sq',
                      'sr', 'ta', 'tr', 'zh-CN', 'zh-TW']

# reCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_USE_SSL = True

TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'

# Use a message storage mechanism that doesn't need a database.
# This can be changed to use session once we do add a database.
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


def lazy_email_backend():
    from django.conf import settings
    return ('django.core.mail.backends.console.EmailBackend' if settings.DEBUG
            else 'django.core.mail.backends.smtp.EmailBackend')

EMAIL_BACKEND = lazy(lazy_email_backend, str)()

AURORA_STUB_INSTALLER = False

# special value that means all locales are enabled.
STUB_INSTALLER_ALL = '__ALL__'
# values should be a list of lower case locales per platform for which a
# stub installer is available. Hopefully this can all be moved to bouncer.
STUB_INSTALLER_LOCALES = {
    'win': STUB_INSTALLER_ALL,
    'osx': [],
    'linux': [],
}

# Force download via SSL
FORCE_SSL_DOWNLOAD_VERSIONS = ['27.0', '27.0.1']

# Google Analytics
GA_ACCOUNT_CODE = ''

FACEBOOK_LOCALES = ['en-US', 'es-ES', 'pt-BR', 'id', 'de']
FACEBOOK_PAGE_NAMESPACE = 'DUMMY_PAGE_NAMESPACE'
FACEBOOK_APP_ID = 'DUMMY_APP_ID'

# Facebook Like button supported locales
# https://www.facebook.com/translations/FacebookLocales.xml
FACEBOOK_LIKE_LOCALES = ['af_ZA', 'ar_AR', 'az_AZ', 'be_BY', 'bg_BG',
                         'bn_IN', 'bs_BA', 'ca_ES', 'cs_CZ', 'cy_GB',
                         'da_DK', 'de_DE', 'el_GR', 'en_GB', 'en_PI',
                         'en_UD', 'en_US', 'eo_EO', 'es_ES', 'es_LA',
                         'et_EE', 'eu_ES', 'fa_IR', 'fb_LT', 'fi_FI',
                         'fo_FO', 'fr_CA', 'fr_FR', 'fy_NL', 'ga_IE',
                         'gl_ES', 'he_IL', 'hi_IN', 'hr_HR', 'hu_HU',
                         'hy_AM', 'id_ID', 'is_IS', 'it_IT', 'ja_JP',
                         'ka_GE', 'km_KH', 'ko_KR', 'ku_TR', 'la_VA',
                         'lt_LT', 'lv_LV', 'mk_MK', 'ml_IN', 'ms_MY',
                         'nb_NO', 'ne_NP', 'nl_NL', 'nn_NO', 'pa_IN',
                         'pl_PL', 'ps_AF', 'pt_BR', 'pt_PT', 'ro_RO',
                         'ru_RU', 'sk_SK', 'sl_SI', 'sq_AL', 'sr_RS',
                         'sv_SE', 'sw_KE', 'ta_IN', 'te_IN', 'th_TH',
                         'tl_PH', 'tr_TR', 'uk_UA', 'vi_VN', 'zh_CN',
                         'zh_HK', 'zh_TW']


# FACEBOOK_TAB_URL is lazily evaluated because it depends on the namespace
# and app ID settings in local settings.
def facebook_tab_url_lazy():
    from django.conf import settings
    return '//www.facebook.com/{page}/app_{id}'.format(page=settings.FACEBOOK_PAGE_NAMESPACE, id=settings.FACEBOOK_APP_ID)
FACEBOOK_TAB_URL = lazy(facebook_tab_url_lazy, str)()

# Prefix for media. No trailing slash.
# e.g. '//mozorg.cdn.mozilla.net'
CDN_BASE_URL = ''

CSRF_FAILURE_VIEW = 'bedrock.mozorg.views.csrf_failure'

from .newsletters import DEFAULT_NEWSLETTERS  # noqa

# Regional press blogs map to locales
PRESS_BLOG_ROOT = 'https://blog.mozilla.org/'
PRESS_BLOGS = {
    'de': 'press-de/',
    'en-GB': 'press-uk/',
    'en-US': 'press/',
    'es-AR': 'press-latam/',
    'es-CL': 'press-latam/',
    'es-ES': 'press-es/',
    'es-MX': 'press-latam/',
    'fr': 'press-fr/',
    'it': 'press-it/',
    'pl': 'press-pl/',
}

MOBILIZER_LOCALE_LINK = {
    'en-US': 'https://wiki.mozilla.org/FirefoxOS/Community/Mobilizers',
    'hu': 'https://www.facebook.com/groups/mobilizerhungary/',
    'pt-BR': 'https://wiki.mozilla.org/Mobilizers/MobilizerBrasil/',
    'pl': 'https://wiki.mozilla.org/Mobilizers/MobilizerPolska/',
    'gr': 'https://wiki.mozilla.org/Mobilizer/MobilizerGreece/',
    'cs': 'https://wiki.mozilla.org/Mobilizer/MobilizerCzechRepublic/'
}

DONATE_LOCALE_LINK = {
    'de': 'https://sendto.mozilla.org/page/contribute/EOYFR2013-webDE',
    'en-US': 'https://sendto.mozilla.org/page/contribute/EOYFR2013-tabzilla',
    'fr': 'https://sendto.mozilla.org/page/contribute/EOYFR2013-webFR',
    'pt-BR': 'https://sendto.mozilla.org/page/contribute/EOYFR2013-webPTBR',
}

# Official Firefox Twitter accounts
FIREFOX_TWITTER_ACCOUNTS = {
    'en-US': 'https://twitter.com/firefox',
    'es-ES': 'https://twitter.com/firefox_es',
    'pt-BR': 'https://twitter.com/firefoxbrasil',
}

# Mapbox token for spaces and communities pages
MAPBOX_TOKEN = 'examples.map-9ijuk24y'

TABZILLA_INFOBAR_OPTIONS = 'translation'

# Optimize.ly project code for base template JS snippet
OPTIMIZELY_PROJECT_ID = None

# Link to Firefox for Android on the Google Play store with Google Analytics
# campaign parameters
GOOGLE_PLAY_FIREFOX_LINK = ('https://play.google.com/store/apps/details?'
                            'id=org.mozilla.firefox&utm_source=mozilla&'
                            'utm_medium=Referral&utm_campaign=mozilla-org')

# Use bedrock Gruntfile.js for live reload
USE_GRUNT_LIVERELOAD = False

# Publishing system config
RNA = {
    'BASE_URL': os.environ.get('RNA_BASE_URL', 'https://nucleus.mozilla.org/rna/'),

    # default False as temporary workaround for bug 973499
    'VERIFY_SSL_CERT': os.environ.get('VERIFY_SSL_CERT', False),
}
