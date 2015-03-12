# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Django settings file for bedrock.

from os.path import abspath

from funfactory.settings_base import *  # noqa
from django.utils.http import urlquote

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

USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

# Accepted locales
PROD_LANGUAGES = ('ach', 'af', 'an', 'ar', 'as', 'ast', 'az', 'be', 'bg',
                  'bn-BD', 'bn-IN', 'br', 'bs', 'ca', 'cs', 'cy',
                  'da', 'de', 'dsb', 'el', 'en-GB', 'en-US', 'en-ZA',
                  'eo', 'es-AR', 'es-CL', 'es-ES', 'es-MX', 'et', 'eu',
                  'fa', 'ff', 'fi', 'fr', 'fy-NL', 'ga-IE', 'gd', 'gl',
                  'gu-IN', 'ha', 'he', 'hi-IN', 'hr', 'hsb', 'hu',
                  'hy-AM', 'id', 'ig', 'is', 'it', 'ja', 'ja-JP-mac',
                  'ka', 'kk', 'km', 'kn', 'ko', 'lij', 'lt', 'lv',
                  'mai', 'mk', 'ml', 'mr', 'ms', 'my', 'nb-NO', 'nl',
                  'nn-NO', 'oc', 'or', 'pa-IN', 'pl', 'pt-BR', 'pt-PT',
                  'rm', 'ro', 'ru', 'sat', 'si', 'sk', 'sl', 'son', 'sq', 'sr',
                  'sv-SE', 'sw', 'ta', 'te', 'th', 'tr', 'uk', 'ur',
                  'uz', 'vi', 'wo', 'xh', 'zh-CN', 'zh-TW', 'zu')
DEV_LANGUAGES = list(DEV_LANGUAGES) + ['en-US']

# Map short locale names to long, preferred locale names. This overrides the
# setting in funfactory and will be used in urlresolvers to determine the
# best-matching locale from the user's Accept-Language header.
CANONICAL_LOCALES = {
    'en': 'en-US',
    'es': 'es-ES',
    'ja-jp-mac': 'ja',
    'no': 'nb-NO',
    'pt': 'pt-BR',
    'sv': 'sv-SE',
}

FEED_CACHE = 3900
DOTLANG_CACHE = 600

DOTLANG_FILES = ['main', 'download_button', 'newsletter']

# Paths that don't require a locale code in the URL.
# matches the first url component (e.g. mozilla.org/gameon/)
SUPPORTED_NONLOCALES += [
    # from redirects.urls
    'admin',
    'contribute.json',
    'credits',
    'gameon',
    'rna',
    'robots.txt',
    'telemetry',
    'webmaker',
    'contributor-data',
]

ALLOWED_HOSTS = [
    'www.mozilla.org',
    'www.ipv6.mozilla.org',
    'www.allizom.org',
]

# The canonical, production URL without a trailing slash
CANONICAL_URL = 'https://www.mozilla.org'

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
            'pipeline.jinja2.ext.PipelineExtension',
        ],
        # Make None in templates render as ''
        'finalize': lambda x: x if x is not None else '',
        'auto_reload': True,
    }

MEDIA_URL = '/user-media/'
STATIC_URL = '/media/'
STATIC_ROOT = path('static')
STATICFILES_STORAGE = 'bedrock.base.storage.ManifestPipelineStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
)
STATICFILES_DIRS = (
    path('media'),
)

JINGO_EXCLUDE_APPS = (
    'admin', 'registration', 'rest_framework', 'rna', 'waffle')

PIPELINE_DISABLE_WRAPPER = True
PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)
PIPELINE_LESS_BINARY = path('node_modules', 'less', 'bin', 'lessc')
PIPELINE_LESS_ARGUMENTS = '-s'
WHITENOISE_ROOT = path('root_files')
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'
PIPELINE_UGLIFYJS_BINARY = path('node_modules', 'uglify-js', 'bin', 'uglifyjs')
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_CSSMIN_BINARY = path('node_modules', 'cssmin', 'bin', 'cssmin')

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
PIPELINE_CSS = {
    'csrf-failure': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/csrf-failure.less',
        ),
        'output_filename': 'css/csrf-failure-bundle.css',
    },
    'about': {
        'source_filenames': (
            'css/sandstone/video-resp.less',
            'css/mozorg/about-base.less',
            'css/mozorg/mosaic.less',
        ),
        'output_filename': 'css/about-bundle.css',
    },
    'about-base': {
        'source_filenames': (
            'css/mozorg/about-base.less',
        ),
        'output_filename': 'css/about-base-bundle.css',
    },
    'credits-faq': {
        'source_filenames': (
            'css/mozorg/credits-faq.less',
        ),
        'output_filename': 'css/credits-faq-bundle.css',
    },
    'commit-access-policy': {
        'source_filenames': (
            'css/mozorg/commit-access-policy.less',
        ),
        'output_filename': 'css/commit-access-policy-bundle.css',
    },
    'commit-access-requirements': {
        'source_filenames': (
            'css/mozorg/commit-access-requirements.less',
        ),
        'output_filename': 'css/commit-access-requirements.css',
    },
    'about-forums': {
        'source_filenames': (
            'css/mozorg/about-forums.less',
        ),
        'output_filename': 'css/about-forums-bundle.css',
    },
    'foundation': {
        'source_filenames': (
            'css/foundation/foundation.less',
        ),
        'output_filename': 'css/foundation-bundle.css',
    },
    'gigabit': {
        'source_filenames': (
            'css/gigabit/gigabit.less',
        ),
        'output_filename': 'css/gigabit-bundle.css',
    },
    'grants': {
        'source_filenames': (
            'css/grants/grants.less',
        ),
        'output_filename': 'css/grants-bundle.css',
    },
    'lightbeam': {
        'source_filenames': (
            'css/lightbeam/lightbeam.less',
        ),
        'output_filename': 'css/lightbeam-bundle.css',
    },
    'itu': {
        'source_filenames': (
            'css/mozorg/itu.less',
        ),
        'output_filename': 'css/itu-bundle.css',
    },
    'common': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
        ),
        'output_filename': 'css/common-bundle.css',
    },
    'responsive': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
        ),
        'output_filename': 'css/responsive-bundle.css',
    },
    'oldIE': {
        'source_filenames': (
            'css/sandstone/oldIE.less',
        ),
        'output_filename': 'css/oldIE-bundle.css',
    },
    'newsletter': {
        'source_filenames': (
            'css/newsletter/newsletter.less',
        ),
        'output_filename': 'css/newsletter-bundle.css',
    },
    'contact-spaces': {
        'source_filenames': (
            'css/libs/mapbox-2.1.5.css',
            'css/libs/magnific-popup.css',
            'css/base/mozilla-video-poster.less',
            'css/mozorg/contact-spaces.less',
        ),
        'output_filename': 'css/contact-spaces-bundle.css',
    },
    'contact-spaces-ie7': {
        'source_filenames': (
            'css/mozorg/contact-spaces-ie7.less',
        ),
        'output_filename': 'css/contact-spaces-ie7-bundle.css',
    },
    'contribute-old': {
        'source_filenames': (
            'css/mozorg/contribute/contribute-form.less',
            'css/mozorg/contribute/contribute-old.less',
            'css/sandstone/video-resp.less',
        ),
        'output_filename': 'css/contribute-old-bundle.css',
    },
    'contribute-studentambassadors-landing': {
        'source_filenames': (
            'css/base/social-widgets.less',
            'css/mozorg/contribute/studentambassadors/landing.less',
        ),
        'output_filename': 'css/contribute-studentambassadors-landing-bundle.css',
    },
    'contribute-studentambassadors-join': {
        'source_filenames': (
            'css/mozorg/contribute/studentambassadors/join.less',
        ),
        'output_filename': 'css/contribute-studentambassadors-join-bundle.css',
    },
    'dnt': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/family-nav.less',
            'css/base/mozilla-accordion.less',
            'css/firefox/dnt.less',
        ),
        'output_filename': 'css/dnt-bundle.css',
    },
    'firefox': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/firefox/menu.less',
            'css/firefox/template.less',
        ),
        'output_filename': 'css/firefox-bundle.css',
    },
    'firefox_all': {
        'source_filenames': (
            'css/base/mozilla-share-cta.less',
            'css/sandstone/sandstone-resp.less',
            'css/firefox/menu-resp.less',
            'css/firefox/all.less',
        ),
        'output_filename': 'css/firefox_all-bundle.css',
    },
    'firefox_android': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/family-nav.less',
            'css/base/mozilla-accordion.less',
            'css/firefox/android.less',
        ),
        'output_filename': 'css/firefox_android-bundle.css',
    },
    'firefox_unsupported': {
        'source_filenames': (
            'css/firefox/unsupported.less',
        ),
        'output_filename': 'css/firefox_unsupported-bundle.css',
    },
    'firefox_unsupported_systems': {
        'source_filenames': (
            'css/firefox/unsupported-systems.less',
        ),
        'output_filename': 'css/firefox_unsupported_systems-bundle.css',
    },
    'firefox-resp': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
        ),
        'output_filename': 'css/firefox-resp-bundle.css',
    },
    'firefox_channel': {
        'source_filenames': (
            'css/firefox/channel.less',
        ),
        'output_filename': 'css/firefox_channel-bundle.css',
    },
    'firefox-dashboard': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/base/mozilla-accordion.less',
            'css/firefox/menu-resp.less',
            'css/firefox/dashboard.less',
        ),
        'output_filename': 'css/firefox-dashboard-bundle.css',
    },
    'firefox_desktop': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/family-nav.less',
            'css/firefox/desktop/intro-anim.less',
            'css/base/svg-animation-check.less',
            'css/firefox/desktop/index.less',
        ),
        'output_filename': 'css/firefox_desktop-bundle.css',
    },
    'firefox_desktop_fast': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/family-nav.less',
            'css/firefox/desktop/fast.less',
        ),
        'output_filename': 'css/firefox_desktop_fast-bundle.css',
    },
    'firefox_desktop_customize': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/family-nav.less',
            'css/firefox/desktop/customize.less',
        ),
        'output_filename': 'css/firefox_desktop_customize-bundle.css',
    },
    'firefox_desktop_tips': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/libs/socialshare/socialshare.less',
            'css/firefox/desktop/tips.less',
        ),
        'output_filename': 'css/firefox_desktop_tips-bundle.css',
    },
    'firefox_desktop_trust': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/family-nav.less',
            'css/firefox/desktop/trust.less',
        ),
        'output_filename': 'css/firefox_desktop_trust-bundle.css',
    },
    'firefox_sms': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/base/mozilla-share-cta.less',
            'css/firefox/template-resp.less',
            'css/sandstone/video-resp.less',
            'css/firefox/mobile-sms.less',
        ),
        'output_filename': 'css/firefox_sms-bundle.css',
    },
    'firefox-interest-dashboard': {
        'source_filenames': (
            'css/firefox/family-nav.less',
            'css/firefox/interest-dashboard.less',
        ),
        'output_filename': 'css/firefox-interest-dashboard-bundle.css',
    },
    'firefox-tiles': {
        'source_filenames': (
            'css/firefox/family-nav.less',
            'css/firefox/tiles.less',
        ),
        'output_filename': 'css/firefox-tiles-bundle.css',
    },
    'firefox_faq': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/menu-resp.less',
            'css/firefox/faq.less',
            'css/firefox/template-resp.less',
            'css/base/mozilla-accordion.less',
        ),
        'output_filename': 'css/firefox_faq-bundle.css',
    },
    'firefox_firstrun': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/sandstone/video.less',
            'css/base/mozilla-modal.less',
            'css/firefox/firstrun.less',
        ),
        'output_filename': 'css/firefox_firstrun-bundle.css',
    },
    'firefox_fx36_firstrun': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/firefox/australis/australis-ui-tour.less',
            'css/firefox/hello-animation.less',
            'css/firefox/australis/fx36/common.less',
        ),
        'output_filename': 'css/firefox_fx36_firstrun-bundle.css',
    },
    'firefox_fx36_whatsnew': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/firefox/australis/australis-ui-tour.less',
            'css/firefox/hello-animation.less',
            'css/firefox/australis/fx36/common.less',
        ),
        'output_filename': 'css/firefox_fx36_whatsnew-bundle.css',
    },
    'firefox_fx36_whatsnew_no_tour': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/firefox/hello-animation.less',
            'css/firefox/australis/fx36/common.less',
        ),
        'output_filename': 'css/firefox_fx36_whatsnew_no_tour-bundle.css',
    },
    'firefox_developer_firstrun': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/base/mozilla-modal.less',
            'css/firefox/dev-firstrun.less',
        ),
        'output_filename': 'css/firefox_developer_firstrun-bundle.css',
    },
    'nightly_firstrun': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/firefox/nightly_firstrun.less',
        ),
        'output_filename': 'css/nightly_firstrun-bundle.css',
    },
    'firefox_geolocation': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/firefox/menu-resp.less',
            'css/base/mozilla-accordion.less',
            'css/base/mozilla-modal.less',
            'css/libs/mapbox-2.1.5.css',
            'css/firefox/geolocation.less'
        ),
        'output_filename': 'css/firefox_geolocation-bundle.css',
    },
    'firefox_developer': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/base/mozilla-modal.less',
            'css/base/mozilla-share-cta.less',
            'css/firefox/menu-resp.less',
            'css/firefox/developer.less',
        ),
        'output_filename': 'css/firefox_developer-bundle.css',
    },
    'firefox_hello_start': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/hello/start.less',
        ),
        'output_filename': 'css/firefox_hello_start-bundle.css',
    },
    'firefox_hello': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/family-nav.less',
            'css/base/mozilla-modal.less',
            'css/base/svg-animation-check.less',
            'css/base/mozilla-share-cta.less',
            'css/firefox/hello/index.less',
        ),
        'output_filename': 'css/firefox_hello-bundle.css',
    },
    'firefox_new': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/libs/socialshare/socialshare.less',
            'css/firefox/simple_footer-resp.less',
            'css/firefox/new.less',
        ),
        'output_filename': 'css/firefox_new-bundle.css',
    },
    'firefox_organizations': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/firefox/organizations.less',
        ),
        'output_filename': 'css/firefox_organizations-bundle.css',
    },
    'firefox_os': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/base/mozilla-modal.less',
            'css/libs/jquery.pageslide.css',
            'css/firefox/os/get_device.less',
            'css/firefox/os/firefox-os.less',
        ),
        'output_filename': 'css/firefox_os-bundle.css',
    },
    'firefox_os_new': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/base/mozilla-modal.less',
            'css/firefox/family-nav.less',
            'css/firefox/os/get_device.less',
            'css/firefox/os/firefox-os-new.less',
        ),
        'output_filename': 'css/firefox_os_new-bundle.css',
    },
    'firefox_os_ie': {
        'source_filenames': (
            'css/firefox/os/firefox-os-ie.less',
        ),
        'output_filename': 'css/firefox_os_ie-bundle.css',
    },
    'firefox_os_devices': {
        'source_filenames': (
            'css/libs/tipsy.css',
            'css/sandstone/sandstone-resp.less',
            'css/firefox/family-nav.less',
            'css/base/mozilla-modal.less',
            'css/firefox/os/get_device.less',
            'css/firefox/os/devices.less',
        ),
        'output_filename': 'css/firefox_os_devices-bundle.css',
    },
    'firefox_os_devices_ie': {
        'source_filenames': (
            'css/firefox/os/devices-ie.less',
        ),
        'output_filename': 'css/firefox_os_devices_ie-bundle.css',
    },
    'firefox_os_mwc_2015_preview': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/base/mozilla-modal.less',
            'css/firefox/family-nav.less',
            'css/firefox/os/mwc-2015-preview.less',
        ),
        'output_filename': 'css/firefox_os_mwc_2015_preview-bundle.css',
    },
    'firefox_os_tv': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/firefox/os/tv.less',
        ),
        'output_filename': 'css/firefox_os_tv-bundle.css',
    },
    'firefox_releases_index': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/firefox/menu-resp.less',
            'css/firefox/releases-index.less',
        ),
        'output_filename': 'css/firefox_releases_index-bundle.css',
    },
    'firefox_privacy_tour': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/base/mozilla-modal.less',
            'css/base/mozilla-share-cta.less',
            'css/firefox/independent-splash.less',
            'css/firefox/australis/australis-ui-tour.less',
            'css/firefox/privacy_tour/common.less',
            'css/firefox/privacy_tour/tour.less',
        ),
        'output_filename': 'css/firefox_privacy_tour-bundle.css',
    },
    'firefox_privacy_no_tour': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/base/mozilla-modal.less',
            'css/base/mozilla-share-cta.less',
            'css/firefox/independent-splash.less',
            'css/firefox/privacy_tour/common.less',
            'css/firefox/privacy_tour/no-tour.less',
        ),
        'output_filename': 'css/firefox_privacy_no_tour-bundle.css',
    },
    'firefox_search_tour': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/firefox/search_tour/common.less',
            'css/firefox/search_tour/tour.less',
        ),
        'output_filename': 'css/firefox_search_tour-bundle.css',
    },
    'firefox_search_no_tour': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/firefox/search_tour/common.less',
        ),
        'output_filename': 'css/firefox_search_no_tour-bundle.css',
    },
    'firefox_tour': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/firefox/australis/australis-ui-tour.less',
            'css/firefox/australis/australis-page-common.less',
            'css/firefox/sync-animation.less',
            'css/firefox/australis/australis-page-stacked.less',
        ),
        'output_filename': 'css/firefox_tour-bundle.css',
    },
    'firefox_whatsnew': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/sandstone/video.less',
            'css/firefox/whatsnew.less',
            'css/firefox/whatsnew-android.less',
        ),
        'output_filename': 'css/firefox_whatsnew-bundle.css',
    },
    'firefox_whatsnew_37': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/firefox/whatsnew-fx37.less',
        ),
        'output_filename': 'css/firefox_whatsnew_37-bundle.css',
    },
    'firefox_whatsnew_fxos': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/firefox/simple_footer.less',
            'css/firefox/whatsnew-fxos.less',
        ),
        'output_filename': 'css/firefox_whatsnew_fxos-bundle.css',
    },
    'firefox_releasenotes': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/firefox/menu-resp.less',
            'css/firefox/releasenotes.less',
        ),
        'output_filename': 'css/firefox_releasenotes-bundle.css',
    },
    'firefox_sync': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/family-nav.less',
            'css/firefox/sync.less',
        ),
        'output_filename': 'css/firefox_sync-bundle.css',
    },
    'firefox_sync_old': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/menu-resp.less',
            'css/firefox/sync-old.less',
        ),
        'output_filename': 'css/firefox_sync_old-bundle.css',
    },
    'firefox_sync_anim': {
        'source_filenames': (
            'css/firefox/sync-animation.less',
        ),
        'output_filename': 'css/firefox_sync_anim-bundle.css',
    },
    'firefox_independent': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/base/mozilla-share-cta.less',
            'css/firefox/independent-splash.less',
            'css/firefox/independent.less',
        ),
        'output_filename': 'css/firefox_independent-bundle.css',
    },
    'installer_help': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/firefox/template-resp.less',
            'css/firefox/menu-resp.less',
            'css/base/mozilla-modal.less',
            'css/firefox/installer-help.less',
        ),
        'output_filename': 'css/installer_help-bundle.css',
    },
    'growth_firstrun_test1': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/firefox/australis/australis-page-common.less',
            'css/firefox/sync-animation.less',
            'css/firefox/australis/australis-page-stacked.less',
            'css/firefox/australis/growth-firstrun-test-common.less',
            'css/firefox/australis/growth-firstrun-test1.less',
        ),
        'output_filename': 'css/growth-firstrun-test1-bundle.css'
    },
    'growth_firstrun_test2': {
        'source_filenames': (
            'css/sandstone/sandstone.less',
            'css/firefox/australis/australis-page-common.less',
            'css/firefox/sync-animation.less',
            'css/firefox/australis/australis-page-stacked.less',
            'css/firefox/australis/growth-firstrun-test-common.less',
            'css/firefox/australis/growth-firstrun-test2.less',
        ),
        'output_filename': 'css/growth-firstrun-test2-bundle.css'
    },
    'history-slides': {
        'source_filenames': (
            'css/mozorg/history-slides.less',
        ),
        'output_filename': 'css/history-slides-bundle.css',
    },
    'home': {
        'source_filenames': (
            'css/mozorg/home.less',
            'css/mozorg/home-promo.less',
        ),
        'output_filename': 'css/home-bundle.css',
    },
    'home-ie9': {
        'source_filenames': (
            'css/mozorg/home-ie9.less',
        ),
        'output_filename': 'css/home-ie9-bundle.css',
    },
    'home-ie8': {
        'source_filenames': (
            'css/mozorg/home-ie8.less',
        ),
        'output_filename': 'css/home-ie8-bundle.css',
    },
    'home-ie': {
        'source_filenames': (
            'css/mozorg/home-ie.less',
        ),
        'output_filename': 'css/home-ie-bundle.css',
    },
    'home-2015': {
        'source_filenames': (
            'css/mozorg/home/home.less',
            'css/mozorg/home/home-promo.less',
        ),
        'output_filename': 'css/home-2015-bundle.css',
    },
    'home-2015-ie8': {
        'source_filenames': (
            'css/mozorg/home/home-ie8.less',
        ),
        'output_filename': 'css/home-2015-ie8-bundle.css',
    },
    'legal': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/legal/legal.less',
        ),
        'output_filename': 'css/legal-bundle.css',
    },
    'legal-eula': {
        'source_filenames': (
            'css/legal/eula.less',
        ),
        'output_filename': 'css/legal-eula-bundle.css',
    },
    'legal_fraud_report': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/legal/fraud-report.less',
        ),
        'output_filename': 'css/legal_fraud_report-bundle.css',
    },
    'manifesto': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/libs/socialshare/socialshare.less',
            'css/mozorg/mosaic.less',
            'css/mozorg/manifesto.less',
        ),
        'output_filename': 'css/manifesto-bundle.css',
    },
    'mission': {
        'source_filenames': (
            'css/sandstone/video-resp.less',
            'css/mozorg/mosaic.less',
            'css/mozorg/mission.less',
        ),
        'output_filename': 'css/mission-bundle.css',
    },
    'mozilla_accordion': {
        'source_filenames': (
            'css/base/mozilla-accordion.less',
        ),
        'output_filename': 'css/mozilla_accordion-bundle.css',
    },
    'newsletter_ios': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/newsletter/ios.less',
        ),
        'output_filename': 'css/newsletter_ios-bundle.css',
    },
    'partnerships': {
        'source_filenames': (
            'css/mozorg/partnerships.less',
        ),
        'output_filename': 'css/partnerships-bundle.css',
    },
    'persona': {
        'source_filenames': (
            'css/persona/persona.less',
        ),
        'output_filename': 'css/persona-bundle.css',
    },
    'powered-by': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/mozorg/powered-by.less',
        ),
        'output_filename': 'css/powered-by-bundle.css',
    },
    'plugincheck': {
        'source_filenames': (
            'css/base/mozilla-share-cta.less',
            'css/plugincheck/plugincheck.less',
            'css/plugincheck/qtip.css',
        ),
        'output_filename': 'css/plugincheck-bundle.css',
    },
    'press_speaker_request': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/press/speaker-request.less',
        ),
        'output_filename': 'css/press_speaker_request-bundle.css',
    },
    'privacy': {
        'source_filenames': (
            'css/privacy/privacy.less',
        ),
        'output_filename': 'css/privacy-bundle.css',
    },
    'privacy-day': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/base/mozilla-share-cta.less',
            'css/privacy/privacy-day.less',
        ),
        'output_filename': 'css/privacy-day-bundle.css',
    },
    'fb_privacy': {
        'source_filenames': (
            'css/privacy/fb-privacy.less',
        ),
        'output_filename': 'css/fb_privacy-bundle.css',
    },
    'products': {
        'source_filenames': (
            'css/mozorg/products.less',
        ),
        'output_filename': 'css/products-bundle.css',
    },
    'projects_mozilla_based': {
        'source_filenames': (
            'css/mozorg/projects/mozilla-based.less',
        ),
        'output_filename': 'css/projects_mozilla_based-bundle.css',
    },
    'projects-calendar': {
        'source_filenames': (
            'css/mozorg/projects/calendar.less',
        ),
        'output_filename': 'css/projects-calendar-bundle.css',
    },
    'research': {
        'source_filenames': (
            'css/research/research.less',
        ),
        'output_filename': 'css/research-bundle.css',
    },
    'security': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/security/security.less',
        ),
        'output_filename': 'css/security-bundle.css',
    },
    'security-bug-bounty-hall-of-fame': {
        'source_filenames': (
            'css/security/hall-of-fame.less',
            'css/base/mozilla-accordion.less',
        ),
        'output_filename': 'css/security-bug-bounty-hall-of-fame-bundle.css',
    },
    'security-tld-idn': {
        'source_filenames': (
            'css/mozorg/security-tld-idn.less',
        ),
        'output_filename': 'css/security-tld-idn-bundle.css',
    },
    'styleguide': {
        'source_filenames': (
            'css/sandstone/fonts.less',
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
        'output_filename': 'css/styleguide-bundle.css',
    },
    'styleguide-docs-mozilla-accordion': {
        'source_filenames': (
            'css/base/mozilla-accordion.less',
            'css/sandstone/sandstone-resp.less',
        ),
        'output_filename': 'css/styleguide-docs-mozilla-accordion-bundle.css',
    },
    'styleguide-docs-mozilla-pager': {
        'source_filenames': (
            'css/sandstone/sandstone-resp.less',
            'css/styleguide/docs/mozilla-pager.less',
        ),
        'output_filename': 'css/styleguide-docs-mozilla-pager-bundle.css',
    },
    'tabzilla': {
        'source_filenames': (
            'css/tabzilla/tabzilla.less',
        ),
        'output_filename': 'css/tabzilla-min.css',
    },
    'contribute-2015': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/mozorg/contribute/contribute-2015.less',
        ),
        'output_filename': 'css/contribute-2015-bundle.css',
    },
    'video': {
        'source_filenames': (
            'css/sandstone/video.less',
        ),
        'output_filename': 'css/video-bundle.css',
    },
    'video-resp': {
        'source_filenames': (
            'css/sandstone/video-resp.less',
        ),
        'output_filename': 'css/video-resp-bundle.css',
    },
    'page_not_found': {
        'source_filenames': (
            'css/base/page-not-found.less',
        ),
        'output_filename': 'css/page_not_found-bundle.css',
    },
    'annual_2011': {
        'source_filenames': (
            'css/foundation/annual2011.less',
        ),
        'output_filename': 'css/annual_2011-bundle.css',
    },
    'annual_2012': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/foundation/annual2012.less',
        ),
        'output_filename': 'css/annual_2012-bundle.css',
    },
    'annual_2013': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/foundation/annual2013.less',
        ),
        'output_filename': 'css/annual_2013-bundle.css',
    },
    'partners': {
        'source_filenames': (
            'css/base/mozilla-modal.less',
            'css/libs/jquery.pageslide.css',
            'css/firefox/partners.less',
            'css/firefox/family-nav.less',
            'css/firefox/mwc-2015-schedule.less',
            'css/firefox/mwc-2015-map.less',
        ),
        'output_filename': 'css/partners-bundle.css',
    },
    'partners-ie7': {
        'source_filenames': (
            'css/firefox/partners/ie7.less',
        ),
        'output_filename': 'css/partners-ie7-bundle.css',
    },
    'facebookapps_downloadtab': {
        'source_filenames': (
            'css/libs/h5bp_main.css',
            'css/facebookapps/downloadtab.less',
        ),
        'output_filename': 'css/facebookapps_downloadtab-bundle.css',
    },
    'thunderbird-start': {
        'source_filenames': (
            'css/sandstone/fonts.less',
            'css/thunderbird/start.less',
        ),
        'output_filename': 'css/thunderbird-start-bundle.css',
    },
}

PIPELINE_JS = {
    'site': {
        'source_filenames': (
            'js/base/site.js',  # this is automatically included on every page
        ),
        'output_filename': 'js/site-bundle.js',
    },
    'lightbeam': {
        'source_filenames': (
            'js/lightbeam/d3.v3.min.js',
            'js/lightbeam/rAF.js',
            'js/lightbeam/lightbeam.js',
            'js/lightbeam/ui.js',
            'js/libs/jquery.validate.js',
        ),
        'output_filename': 'js/lightbeam-bundle.js',
    },
    'projects-calendar': {
        'source_filenames': (
            'js/mozorg/calendar.js',
        ),
        'output_filename': 'js/projects-calendar-bundle.js',
    },
    'common': {
        'source_filenames': (
            'js/libs/jquery-1.11.0.min.js',
            'js/libs/spin.min.js',
            'js/base/global.js',
            'js/base/global-init.js',
            'js/newsletter/form.js',
            'js/base/mozilla-input-placeholder.js',
            'js/base/mozilla-image-helper.js',
        ),
        'output_filename': 'js/common-bundle.js',
    },
    'common-resp': {
        'source_filenames': (
            'js/libs/jquery-1.11.0.min.js',
            'js/libs/spin.min.js',
            'js/base/global.js',
            'js/base/global-init.js',
            'js/newsletter/form.js',
            'js/base/nav-main-resp.js',
            'js/base/mozilla-input-placeholder.js',
            'js/base/mozilla-image-helper.js',
        ),
        'output_filename': 'js/common-resp-bundle.js',
    },
    'contact-spaces': {
        'source_filenames': (
            'js/libs/mapbox-2.1.5.js',
            'js/libs/jquery.history.js',
            'js/mozorg/contact-data.js',
            'js/libs/jquery.magnific-popup.min.js',
            'js/base/mozilla-video-poster.js',
            'js/mozorg/contact-spaces.js',
        ),
        'output_filename': 'js/contact-spaces-bundle.js',
    },
    'contact-spaces-ie7': {
        'source_filenames': (
            'js/mozorg/contact-spaces-ie7.js',
        ),
        'output_filename': 'js/contact-spaces-ie7-bundle.js',
    },
    'contribute-faces': {
        'source_filenames': (
            'js/mozorg/contribute/contribute-faces.js',
        ),
        'output_filename': 'js/contribute-faces-bundle.js',
    },
    'contribute-form': {
        'source_filenames': (
            'js/mozorg/contribute/contribute-form.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'output_filename': 'js/contribute-form-bundle.js',
    },
    'contribute-studentambassadors-landing': {
        'source_filenames': (
            'js/base/social-widgets.js',
        ),
        'output_filename': 'js/contribute-studentambassadors-landing-bundle.js',
    },
    'contribute-studentambassadors-join': {
        'source_filenames': (
            'js/mozorg/contribute/contribute-studentambassadors-join.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'output_filename': 'js/contribute-studentambassadors-join-bundle.js',
    },
    'existing': {
        'source_filenames': (
            'js/newsletter/existing.js',
        ),
        'output_filename': 'js/existing-bundle.js',
    },
    'accordion': {
        'source_filenames': (
            'js/base/mozilla-accordion.js',
            'js/base/mozilla-accordion-gatrack.js',
        ),
        'output_filename': 'js/accordion-bundle.js',
    },
    'dnt': {
        'source_filenames': (
            'js/base/mozilla-accordion.js',
            'js/base/mozilla-accordion-gatrack.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/firefox/dnt.js',
        ),
        'output_filename': 'js/firefox_dnt-bundle.js',
    },
    'firefox': {
        'source_filenames': (
            'js/libs/jquery-1.11.0.min.js',
            'js/libs/spin.min.js',
            'js/base/global.js',
            'js/base/global-init.js',
            'js/newsletter/form.js',
            'js/base/nav-main.js',
            'js/base/mozilla-input-placeholder.js',
            'js/base/mozilla-image-helper.js',
        ),
        'output_filename': 'js/firefox-bundle.js',
    },
    'firefox_all': {
        'source_filenames': (
            'js/base/mozilla-share-cta.js',
            'js/base/mozilla-pager.js',
            'js/firefox/firefox-language-search.js',
        ),
        'output_filename': 'js/firefox_all-bundle.js',
    },
    'firefox_android': {
        'source_filenames': (
            'js/base/mozilla-accordion.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.cycle2.min.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/firefox/sync-animation.js',
            'js/firefox/android.js',
        ),
        'output_filename': 'js/firefox_android-bundle.js',
    },
    'firefox-resp': {
        'source_filenames': (
            'js/libs/jquery-1.11.0.min.js',
            'js/libs/spin.min.js',
            'js/base/global.js',
            'js/base/global-init.js',
            'js/newsletter/form.js',
            'js/base/nav-main-resp.js',
            'js/base/mozilla-input-placeholder.js',
            'js/base/mozilla-image-helper.js',
        ),
        'output_filename': 'js/firefox-resp-bundle.js',
    },
    'firefox_channel': {
        'source_filenames': (
            'js/base/mozilla-pager.js',
            'js/firefox/channel.js',
        ),
        'output_filename': 'js/firefox_channel-bundle.js',
    },
    'firefox_desktop_customize': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/firefox/sync-animation.js',
            'js/firefox/desktop/common.js',
            'js/firefox/desktop/customize.js',
        ),
        'output_filename': 'js/firefox_desktop_customize-bundle.js',
    },
    'firefox_desktop_fast': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/firefox/desktop/common.js',
            'js/firefox/desktop/speed-graph.js',
            'js/firefox/desktop/fast.js',
        ),
        'output_filename': 'js/firefox_desktop_fast-bundle.js',
    },
    'firefox_desktop_index': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/firefox/desktop/common.js',
            'js/firefox/desktop/speed-graph.js',
            'js/base/svg-animation-check.js',
            'js/firefox/desktop/intro-anim.js',
            'js/firefox/desktop/index.js',
        ),
        'output_filename': 'js/firefox_desktop_index-bundle.js',
    },
    'firefox_desktop_tips': {
        'source_filenames': (
            'js/base/mozilla-pager.js',
            'js/libs/hammer.1.1.2.min.js',
            'js/libs/socialshare.min.js',
            'js/firefox/desktop/tips.js',
        ),
        'output_filename': 'js/firefox_desktop_tips-bundle.js',
    },
    'firefox_desktop_trust': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/firefox/desktop/common.js',
            'js/firefox/desktop/trust.js',
        ),
        'output_filename': 'js/firefox_desktop_trust-bundle.js',
    },
    'firefox_developer': {
        'source_filenames': (
            'js/firefox/developer.js',
            'js/base/mozilla-modal.js',
            'js/base/mozilla-share-cta.js',
        ),
        'output_filename': 'js/firefox_developer-bundle.js',
    },
    'firefox_firstrun': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/firefox/firstrun/firstrun.js',
        ),
        'output_filename': 'js/firefox_firstrun-bundle.js',
    },
    'firefox_fx36_firstrun': {
        'source_filenames': (
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/australis/browser-tour.js',
            'js/firefox/australis/fx36/common.js',
            'js/firefox/australis/fx36/firstrun.js',
        ),
        'output_filename': 'js/firefox_fx36_firstrun-bundle.js',
    },
    'firefox_fx36_whatsnew': {
        'source_filenames': (
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/australis/browser-tour.js',
            'js/firefox/australis/fx36/common.js',
            'js/firefox/australis/fx36/whatsnew.js',
        ),
        'output_filename': 'js/firefox_fx36_whatsnew-bundle.js',
    },
    'firefox_fx36_whatsnew_no_tour': {
        'source_filenames': (
            'js/firefox/australis/fx36/common.js',
            'js/firefox/australis/fx36/whatsnew-notour.js',
        ),
        'output_filename': 'js/firefox_fx36_whatsnew_no_tour-bundle.js',
    },
    'firefox_developer_firstrun': {
        'source_filenames': (
            'js/firefox/australis/australis-uitour.js',
            'js/base/mozilla-modal.js',
            'js/firefox/dev-firstrun.js',
        ),
        'output_filename': 'js/firefox_developer_firstrun-bundle.js',
    },
    'firefox_new': {
        'source_filenames': (
            'js/libs/jquery-1.11.0.min.js',
            'js/libs/spin.min.js',
            'js/base/global.js',
            'js/base/global-init.js',
            'js/newsletter/form.js',
            'js/base/mozilla-input-placeholder.js',
            'js/base/mozilla-image-helper.js',
            'js/libs/socialshare.min.js',
            'js/libs/modernizr.custom.csstransitions.js',
            'js/firefox/new.js',
        ),
        'output_filename': 'js/firefox_new-bundle.js',
    },
    'firefox_independent': {
        'source_filenames': (
            'js/base/mozilla-share-cta.js',
            'js/base/firefox-anniversary-video.js',
            'js/firefox/independent.js',
        ),
        'output_filename': 'js/firefox_independent-bundle.js',
    },
    'firefox_os': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/libs/tweenmax.1.9.7.min.js',
            'js/libs/superscrollorama-1.0.1.js',
            'js/libs/jquery.plusslider.js',
            'js/libs/jquery.color.js',
            'js/libs/script.js',
            'js/libs/socialshare.min.js',
            'js/firefox/os/firefox-os.js',
            'js/firefox/os/desktop.js',
            'js/firefox/os/have-it.js',
        ),
        'output_filename': 'js/firefox_os-bundle.js',
    },
    'firefox_os_new': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/libs/script.js',
            'js/firefox/family-nav.js',
            'js/firefox/os/firefox-os-new.js',
        ),
        'output_filename': 'js/firefox_os_new-bundle.js',
    },
    'firefox_os_ie9': {
        'source_filenames': (
            'js/libs/matchMedia.addListener.js',
        ),
        'output_filename': 'js/firefox_os_ie9-bundle.js',
    },
    'firefox_os_devices': {
        'source_filenames': (
            'js/libs/jquery.tipsy.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/base/mozilla-pager.js',
            'js/base/mozilla-modal.js',
            'js/firefox/family-nav.js',
            'js/firefox/os/partner_data.js',
            'js/firefox/os/devices.js',
        ),
        'output_filename': 'js/firefox_os_devices-bundle.js',
    },
    'firefox_os_mwc_2015_preview': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/firefox/mwc-2015-map.js',
            'js/firefox/os/mwc-2015-preview.js',
        ),
        'output_filename': 'js/firefox_os_mwc_2015_preview-bundle.js',
    },
    'firefox_os_tv': {
        'source_filenames': (
            'js/base/mozilla-pager.js',
        ),
        'output_filename': 'js/firefox_os_tv-bundle.js',
    },
    'firefox_interest_dashboard': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/firefox/interest-dashboard.js',
        ),
        'output_filename': 'js/firefox_interest_dashboard-bundle.js',
    },
    'firefox_tiles': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/firefox/tiles.js',
        ),
        'output_filename': 'js/firefox_tiles-bundle.js',
    },
    'firefox_faq': {
        'source_filenames': (
            'js/base/mozilla-accordion.js',
            'js/base/mozilla-accordion-gatrack.js',
        ),
        'output_filename': 'js/firefox_faq-bundle.js',
    },
    'firefox_sync': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/firefox/sync-animation.js',
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/sync.js',
        ),
        'output_filename': 'js/firefox_sync-bundle.js',
    },
    'firefox_sync_old': {
        'source_filenames': (
            'js/firefox/sync-animation.js',
            'js/firefox/sync-old.js',
        ),
        'output_filename': 'js/firefox_sync_old-bundle.js',
    },
    'firefox_hello_start': {
        'source_filenames': (
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/hello/start.js',
        ),
        'output_filename': 'js/firefox_hello_start-bundle.js',
    },
    'firefox_hello': {
        'source_filenames': (
            'js/firefox/australis/australis-uitour.js',
            'js/base/mozilla-modal.js',
            'js/base/svg-animation-check.js',
            'js/base/mozilla-share-cta.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/firefox/hello/index.js',
        ),
        'output_filename': 'js/firefox_hello-bundle.js',
    },
    'firefox_hello_ie9': {
        'source_filenames': (
            'js/libs/matchMedia.js',
            'js/libs/matchMedia.addListener.js',
        ),
        'output_filename': 'js/firefox_hello_ie9-bundle.js',
    },
    'firefox_privacy_tour': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/base/mozilla-share-cta.js',
            'js/base/firefox-anniversary-video.js',
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/australis/browser-tour.js',
            'js/firefox/privacy_tour/common.js',
            'js/firefox/privacy_tour/tour.js',
        ),
        'output_filename': 'js/firefox_privacy_tour-bundle.js',
    },
    'firefox_privacy_no_tour': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/base/mozilla-share-cta.js',
            'js/base/firefox-anniversary-video.js',
            'js/firefox/privacy_tour/common.js',
            'js/firefox/privacy_tour/no-tour.js',
        ),
        'output_filename': 'js/firefox_privacy_no_tour-bundle.js',
    },
    'firefox_search_tour': {
        'source_filenames': (
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/search_tour/common.js',
            'js/firefox/search_tour/tour.js',
        ),
        'output_filename': 'js/firefox_search_tour-bundle.js',
    },
    'firefox_search_tour_34.0.5': {
        'source_filenames': (
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/search_tour/common.js',
            'js/firefox/search_tour/tour-34.0.5.js',
        ),
        'output_filename': 'js/firefox_search_tour_34.0.5-bundle.js',
    },
    'firefox_search_no_tour': {
        'source_filenames': (
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/search_tour/common.js',
        ),
        'output_filename': 'js/firefox_search_no_tour-bundle.js',
    },
    'firefox_tour': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/australis/browser-tour.js',
            'js/firefox/australis/common.js',
            'js/firefox/australis/tour.js',
        ),
        'output_filename': 'js/firefox_tour-bundle.js',
    },
    'firefox_tour_none': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/australis/common.js',
            'js/firefox/australis/no-tour.js',
        ),
        'output_filename': 'js/firefox_tour_none-bundle.js',
    },
    'firefox_sms': {
        'source_filenames': (
            'js/firefox/sms.js',
            'js/base/mozilla-share-cta.js',
        ),
        'output_filename': 'js/firefox_sms-bundle.js',
    },
    'firefox_whatsnew_fx37': {
        'source_filenames': (
            'js/firefox/whatsnew-fx37.js',
        ),
        'output_filename': 'js/firefox_whatsnew_fx37-bundle.js',
    },
    'firefox_whatsnew_fxos': {
        'source_filenames': (
            'js/firefox/whatsnew-fxos.js',
        ),
        'output_filename': 'js/firefox_whatsnew_fxos-bundle.js',
    },
    'geolocation': {
        'source_filenames': (
            'js/libs/mapbox-2.1.5.js',
            'js/base/mozilla-accordion.js',
            'js/base/mozilla-accordion-gatrack.js',
            'js/firefox/geolocation-demo.js',
            'js/base/mozilla-modal.js',
        ),
        'output_filename': 'js/geolocation-bundle.js',
    },
    'home': {
        'source_filenames': (
            'js/libs/jquery.ellipsis.min.js',
            'js/libs/jquery.cycle2.min.js',
            'js/libs/jquery.cycle2.carousel.min.js',
            'js/mozorg/home.js',
        ),
        'output_filename': 'js/home-bundle.js',
    },
    'growth_firstrun_test1': {
        'source_filenames': (
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/australis/growth-browser-tour.js',
            'js/libs/fxa-relier-client.min.js',
            'js/firefox/sync-animation.js',
            'js/firefox/australis/growth-firstrun-test1.js',
        ),
        'output_filename': 'js/growth-firstrun-test1-bundle.js',
    },
    'growth_firstrun_test2': {
        'source_filenames': (
            'js/firefox/australis/australis-uitour.js',
            'js/firefox/australis/growth-browser-tour.js',
            'js/firefox/sync-animation.js',
            'js/firefox/australis/growth-firstrun-test2.js',
        ),
        'output_filename': 'js/growth-firstrun-test2-bundle.js',
    },
    'home-2015': {
        'source_filenames': (
            'js/base/mozilla-share-cta.js',
            'js/base/firefox-anniversary-video.js',
            'js/libs/jquery.waypoints.min.js',
            'js/mozorg/home/home.js',
            'js/mozorg/home/ga-tracking.js',
            'js/mozorg/home/scroll-prompt.js',
        ),
        'output_filename': 'js/home-2015-bundle.js',
    },
    'home-2015-ie9': {
        'source_filenames': (
            'js/libs/matchMedia.addListener.js',
        ),
        'output_filename': 'js/home-2015-ie9-bundle.js',
    },
    'history-slides': {
        'source_filenames': (
            'js/libs/jquery.sequence.js',
            'js/mozorg/history-slides.js',
        ),
        'output_filename': 'js/history-slides-bundle.js',
    },
    'installer_help': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/firefox/installer-help.js',
        ),
        'output_filename': 'js/installer_help-bundle.js',
    },
    'legal_fraud_report': {
        'source_filenames': (
            'js/libs/jquery.validate.js',
            'js/legal/fraud-report.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'output_filename': 'js/legal_fraud_report-bundle.js',
    },
    'manifesto': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/libs/socialshare.min.js',
            'js/mozorg/manifesto.js',
        ),
        'output_filename': 'js/manifesto-bundle.js',
    },
    'manifesto_ie9': {
        'source_filenames': (
            'js/libs/matchMedia.addListener.js',
        ),
        'output_filename': 'js/manifesto_ie9-bundle.js',
    },
    'mozorg-resp': {
        'source_filenames': (
            'js/libs/jquery-1.11.0.min.js',
            'js/libs/spin.min.js',
            'js/base/global.js',
            'js/base/global-init.js',
            'js/newsletter/form.js',
            'js/base/nav-main-resp.js',
            'js/base/mozilla-image-helper.js',
        ),
        'output_filename': 'js/mozorg-resp-bundle.js',
    },
    'nightly-firstrun': {
        'source_filenames': (
            'js/firefox/firstrun/nightly-firstrun.js',
        ),
        'output_filename': 'js/nightly-firstrun-bundle.js',
    },
    'partnerships': {
        'source_filenames': (
            'js/libs/jquery.validate.js',
            'js/base/mozilla-form-helper.js',
            'js/mozorg/partnerships.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'output_filename': 'js/partnerships-bundle.js',
    },
    'plugincheck': {
        'source_filenames': (
            'js/plugincheck/lib/mustache.js',
            'js/base/mozilla-share-cta.js',
            'js/plugincheck/tmpl/plugincheck.ui.tmpl.js',
            'js/plugincheck/check-plugins.js',
        ),
        'output_filename': 'js/plugincheck-bundle.js',
    },
    'press_speaker_request': {
        'source_filenames': (
            'js/libs/jquery.validate.js',
            'js/libs/modernizr.custom.inputtypes.js',
            'js/press/speaker-request.js',
            'js/base/mozilla-input-placeholder.js',
        ),
        'output_filename': 'js/press_speaker_request-bundle.js',
    },
    'privacy': {
        'source_filenames': (
            'js/privacy/privacy.js',
        ),
        'output_filename': 'js/privacy-bundle.js',
    },
    'privacy-day': {
        'source_filenames': (
            'js/base/mozilla-pager.js',
            'js/base/mozilla-share-cta.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/privacy/privacy-day.js',
        ),
        'output_filename': 'js/privacy-day-bundle.js',
    },
    'products': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/mozorg/products.js',
        ),
        'output_filename': 'js/products-bundle.js',
    },
    'styleguide': {
        'source_filenames': (
            'js/styleguide/styleguide.js',
        ),
        'output_filename': 'js/styleguide-bundle.js',
    },
    'styleguide-docs-mozilla-accordion': {
        'source_filenames': (
            'js/base/mozilla-accordion.js',
            'js/styleguide/docs/mozilla-accordion.js',
        ),
        'output_filename': 'js/styleguide-docs-mozilla-accordion-bundle.js',
    },
    'styleguide-docs-mozilla-pager': {
        'source_filenames': (
            'js/base/mozilla-pager.js',
            'js/styleguide/docs/mozilla-pager.js',
        ),
        'output_filename': 'js/styleguide-docs-mozilla-pager-bundle.js',
    },
    'video': {
        'source_filenames': (
            'js/base/mozilla-video-tools.js',
        ),
        'output_filename': 'js/video-bundle.js',
    },
    'contribute-2015': {
        'source_filenames': (
            'js/mozorg/contribute/contribute-2015-ga.js',
            'js/mozorg/contribute/contribute-2015.js',
        ),
        'output_filename': 'js/contribute-2015-bundle.js',
    },
    'contribute-2015-landing': {
        'source_filenames': (
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.cycle2.min.js',
            'js/base/mozilla-modal.js',
        ),
        'output_filename': 'js/contribute-2015-landing-bundle.js',
    },
    'mosaic': {
        'source_filenames': (
            'js/libs/modernizr.custom.26887.js',
            'js/libs/jquery.transit.min.js',
            'js/libs/jquery.gridrotator.js',
        ),
        'output_filename': 'js/mosaic-bundle.js',
    },
    'annual_2011_ie9': {
        'source_filenames': (
            'js/libs/matchMedia.addListener.js',
        ),
        'output_filename': 'js/annual_2011_ie9-bundle.js',
    },
    'annual_2011': {
        'source_filenames': (
            'js/libs/jquery.hoverIntent.minified.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.jcarousel.min.js',
            'js/foundation/annual2011.js',
        ),
        'output_filename': 'js/annual_2011-bundle.js',
    },
    'annual_2012': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/foundation/annual2012.js',
        ),
        'output_filename': 'js/annual_2012-bundle.js',
    },
    'annual_2013': {
        'source_filenames': (
            'js/base/mozilla-modal.js',
            'js/foundation/annual2013.js',
        ),
        'output_filename': 'js/annual_2013-bundle.js',
    },
    'logo-prototype': {
        'source_filenames': (
            'js/styleguide/logo-prototype/vendor/raf.polyfill.js',
            'js/styleguide/logo-prototype/vendor/tween.js',
            'js/styleguide/logo-prototype/vendor/lodash.compat.min.js',
            'js/styleguide/logo-prototype/vendor/perlin.js',
            'js/styleguide/logo-prototype/vendor/dat.gui.js',
            'js/libs/jquery-1.11.0.min.js',
            'js/styleguide/logo-prototype/clock-data.js',
        ),
        'output_filename': 'js/logo-prototype-bundle.js',
    },
    'partners': {
        'source_filenames': (
            'js/libs/modernizr.custom.shiv-load.js',
            'js/base/mozilla-input-placeholder.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/jquery.waypoints-sticky.min.js',
            'js/firefox/family-nav.js',
            'js/base/mozilla-pager.js',
            'js/base/mozilla-modal.js',
            'js/firefox/partners.js',
        ),
        'output_filename': 'js/partners-bundle.js',
    },
    'partners_common': {
        'source_filenames': (
            'js/libs/enquire.min.js',
            'js/base/mozilla-form-helper.js',
            'js/firefox/partners/common.js',
        ),
        'output_filename': 'js/partners_common-bundle.js',
    },
    'partners_mobile': {
        'source_filenames': (
            'js/firefox/partners/mobile.js',
        ),
        'output_filename': 'js/partners_mobile-bundle.js',
    },
    'partners_desktop': {
        'source_filenames': (
            'js/libs/jquery.pageslide.min.js',
            'js/libs/jquery.waypoints.min.js',
            'js/libs/tweenmax.1.9.7.min.js',
            'js/libs/jquery.spritely-0.6.7.js',
            'js/firefox/partners/desktop.js',
        ),
        'output_filename': 'js/partners_desktop-bundle.js',
    },
    'facebookapps_redirect': {
        'source_filenames': (
            'js/libs/jquery-1.11.0.min.js',
            'js/facebookapps/redirect.js',
        ),
        'output_filename': 'js/facebookapps_redirect-bundle.js',
    },
    'facebookapps_downloadtab': {
        'source_filenames': (
            'js/facebookapps/downloadtab-init.js',
            'js/facebookapps/Base.js',
            'js/facebookapps/Facebook.js',
            'js/facebookapps/Theater.js',
            'js/facebookapps/Slider.js',
            'js/facebookapps/App.js',
            'js/facebookapps/downloadtab.js',
        ),
        'output_filename': 'js/facebookapps_downloadtab-bundle.js',
    },
    'newsletter_form': {
        'source_filenames': (
            'js/libs/jquery-1.11.0.min.js',
            'js/libs/spin.min.js',
            'js/newsletter/form.js',
        ),
        'output_filename': 'js/newsletter_form-bundle.js',
    },
    'matchmedia_addlistener': {
        'source_filenames': (
            'js/libs/matchMedia.addListener.js',
        ),
        'output_filename': 'js/matchmedia_addlistener-bundle.js',
    },
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
    'bedrock.mozorg.middleware.ClacksOverheadMiddleware',
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
    'bedrock.mozorg.middleware.ConditionalAuthMiddleware',
    'bedrock.mozorg.middleware.CrossOriginResourceSharingMiddleware',
))

AUTHENTICATED_URL_PREFIXES = ('/admin/', '/rna/')

INSTALLED_APPS = get_apps(exclude=(
    'compressor',
    'django_browserid',
    'django.contrib.sessions',
    'session_csrf',
    'djcelery',
), append=(
    # third-party apps
    'jingo_markdown',
    # 'jingo_minify',
    'django_statsd',
    'pagedown',
    'rest_framework',
    'waffle',
    'south',
    'pipeline',

    # Django contrib apps
    'django.contrib.admin',
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
    '%s.externalfiles' % PROJECT_MODULE,
    '%s.security' % PROJECT_MODULE,
    '%s.events' % PROJECT_MODULE,
    '%s.releasenotes' % PROJECT_MODULE,
    '%s.thunderbird' % PROJECT_MODULE,
    '%s.shapeoftheweb' % PROJECT_MODULE,

    # libs
    'django_extensions',
    'lib.l10n_utils',
    'captcha',
    'rna',
))

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

LOCALE_PATHS = (
    path('locale'),
)

TEMPLATE_CONTEXT_PROCESSORS = get_template_context_processors(append=(
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
    'bedrock.mozorg.context_processors.canonical_path',
    'bedrock.mozorg.context_processors.contrib_numbers',
    'bedrock.mozorg.context_processors.current_year',
    'bedrock.mozorg.context_processors.funnelcake_param',
    'bedrock.mozorg.context_processors.facebook_locale',
    'bedrock.firefox.context_processors.latest_firefox_versions',
    'jingo_minify.helpers.build_ids',
))

# Auth
PWD_ALGORITHM = 'bcrypt'
HMAC_KEYS = {
    # '2011-01-01': 'cheesecake',
}

FEEDS = {
    'mozilla': 'https://blog.mozilla.org/feed/'
}
REPS_ICAL_FEED = 'https://reps.mozilla.org/events/period/future/ical/'

# Twitter accounts to retrieve tweets with the API
TWITTER_ACCOUNTS = (
    'firefox',
    'firefox_es',
    'firefoxbrasil',
    'mozstudents',
)
# Add optional parameters specific to accounts here
# e.g. 'firefox': {'exclude_replies': False}
TWITTER_ACCOUNT_OPTS = {}

# Contribute numbers
# TODO: automate these
CONTRIBUTE_NUMBERS = {
    'num_mozillians': 10554,
    'num_languages': 87,
}

BASKET_URL = 'https://basket.mozilla.org'

# This prefixes /b/ on all URLs generated by `reverse` so that links
# work on the dev site while we have a mix of Python/PHP
FORCE_SLASH_B = False

# reCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_USE_SSL = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

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

# Google Analytics
GA_ACCOUNT_CODE = ''

# Files from The Web[tm]
EXTERNAL_FILES = {
    'credits': {
        'url': 'https://svn.mozilla.org/projects/mozilla.org/trunk/credits/names.csv',
        'type': 'bedrock.mozorg.credits.CreditsFile',
        'name': 'credits.csv',
    },
    'forums': {
        'url': 'https://svn.mozilla.org/projects/mozilla.org/trunk/about/forums/raw-ng-list.txt',
        'type': 'bedrock.mozorg.forums.ForumsFile',
        'name': 'forums.txt',
    },
}

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
    return '//www.facebook.com/{page}/app_{id}'.format(
        page=settings.FACEBOOK_PAGE_NAMESPACE, id=settings.FACEBOOK_APP_ID)
FACEBOOK_TAB_URL = lazy(facebook_tab_url_lazy, str)()

# Prefix for media. No trailing slash.
# e.g. '//mozorg.cdn.mozilla.net'
CDN_BASE_URL = ''

CSRF_FAILURE_VIEW = 'bedrock.mozorg.views.csrf_failure'

from .newsletters import (DEFAULT_NEWSLETTERS, OTHER_NEWSLETTERS,  # noqa
                          MARKETPLACE_NEWSLETTERS)

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

FXOS_PRESS_BLOG_LINKS = {
    'en': 'https://blog.mozilla.org/press/category/firefox-os/',
    'de': 'https://blog.mozilla.org/press-de/category/firefox-os/',
    'es-ES': 'https://blog.mozilla.org/press-es/category/firefox-os/',
    'es': 'https://blog.mozilla.org/press-latam/category/firefox-os/',
    'fr': 'https://blog.mozilla.org/press-fr/category/firefox-os/',
    'it': 'https://blog.mozilla.org/press-it/category/firefox-os/',
    'pb-BR': 'https://blog.mozilla.org/press-br/category/firefox-os/',
    'pl': 'https://blog.mozilla.org/press-pl/category/firefox-os/',
}

MOBILIZER_LOCALE_LINK = {
    'en-US': 'https://wiki.mozilla.org/FirefoxOS/Community/Mobilizers',
    'hu': 'https://www.facebook.com/groups/mobilizerhungary/',
    'pt-BR': 'https://wiki.mozilla.org/Mobilizers/MobilizerBrasil/',
    'pl': 'https://wiki.mozilla.org/Mobilizers/MobilizerPolska/',
    'gr': 'https://wiki.mozilla.org/Mobilizer/MobilizerGreece/',
    'cs': 'https://wiki.mozilla.org/Mobilizer/MobilizerCzechRepublic/'
}

DONATE_SPANISH_LINK = ('https://sendto.mozilla.org/page/contribute/givenow-seq-es?'
    'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
    '&utm_source=mozilla.org&utm_medium=referral&utm_content=mozillaorg_ES')

DONATE_LOCALE_LINK = {
    'default': (
        'https://sendto.mozilla.org/page/contribute/Give-Now?source={source}'
    ),
    'en-US': (
        'https://sendto.mozilla.org/page/contribute/givenow-seq?'
        'preset=2&source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content={source}'
    ),
    'cs': (
        'https://sendto.mozilla.org/page/content/paypal-donate-czk/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_CZK'
    ),
    'da': (
        'https://sendto.mozilla.org/page/content/paypal-donate-dkk/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source={source}&utm_medium=referral&utm_content=PPcurrency_DKK'
    ),
    'de': (
        'https://sendto.mozilla.org/page/contribute/givenow-seq-de?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=mozillaorg_DE'
    ),
    'es-AR': DONATE_SPANISH_LINK,
    'es-CL': DONATE_SPANISH_LINK,
    'es-ES': DONATE_SPANISH_LINK,
    'es-MX': DONATE_SPANISH_LINK,
    'fr': (
        'https://sendto.mozilla.org/page/contribute/givenow-seq-fr?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=mozillaorg_FR'
    ),
    'he': (
        'https://sendto.mozilla.org/page/content/paypal-donate-ils/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_ILS'
    ),
    'hu': (
        'https://sendto.mozilla.org/page/content/paypal-donate-huf/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_HUF'
    ),
    'ja': (
        'https://sendto.mozilla.org/page/content/paypal-donate-jpy/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_JPY'
    ),
    'nb-NO': (
        'https://sendto.mozilla.org/page/content/paypal-donate-nok/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_NOK'
    ),
    'nn-NO': (
        'https://sendto.mozilla.org/page/content/paypal-donate-nok/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_NOK'
    ),
    'pl': (
        'https://sendto.mozilla.org/page/content/paypal-donate-pln/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_PLN'
    ),
    'pt-BR': (
        'https://sendto.mozilla.org/page/contribute/givenow-seq-pt-br?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=mozillaorg_PTBR'
    ),
    'ru': (
        'https://sendto.mozilla.org/page/content/paypal-donate-rub/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_RUB'
    ),
    'sv-SE': (
        'https://sendto.mozilla.org/page/content/paypal-donate-sek/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_SEK'
    ),
    'th': (
        'https://sendto.mozilla.org/page/content/paypal-donate-thb/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_THB'
    ),
}

# Official Firefox Twitter accounts
FIREFOX_TWITTER_ACCOUNTS = {
    'en-US': 'https://twitter.com/firefox',
    'es-ES': 'https://twitter.com/firefox_es',
    'pt-BR': 'https://twitter.com/firefoxbrasil',
}

# Twitter accounts to display on homepage per locale
HOMEPAGE_TWITTER_ACCOUNTS = {
    'en-US': 'firefox',
    'es-AR': 'firefox_es',
    'es-CL': 'firefox_es',
    'es-ES': 'firefox_es',
    'es-MX': 'firefox_es',
    'pt-BR': 'firefoxbrasil',
}

# Mapbox token for spaces and communities pages
MAPBOX_TOKEN = 'examples.map-i86nkdio'
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoibW96aWxsYS13ZWJwcm9kIiwiYSI6Ii0xYVEtTW8ifQ.3ikA2IgKATeXStfC5wKDaQ'

# Tabzilla Information Bar default options
TABZILLA_INFOBAR_OPTIONS = 'update translation'

# Optimize.ly project code
OPTIMIZELY_PROJECT_ID = None

# Fx Accounts Relier Service Client ID
# Prod, stage, & dev all have these set in their local.py files.
# For local testing, override in your own local.py.

# For demo servers & localhost:
#   FXA_RELIER_CONTENT_HOST = 'https://stable.dev.lcip.org'
#   FXA_RELIER_CONTENT_OAUTH = 'https://oauth-stable.dev.lcip.org/v1'
#   FXA_RELIER_REDIRECT_URI = 'http://localhost:8000/'
#
#   Client IDs:
#       localhost:8000: efc5413fa614224e
#       demo5: 591e9db45a43f7e9
#
#   Additional dev IDs can be created here:
#   https://developer.mozilla.org/en-US/Firefox_Accounts_OAuth_Dashboard
#
# Below is full code needed for demo5:
# FXA_RELIER_CLIENT_ID = '591e9db45a43f7e9'
# FXA_RELIER_CONTENT_HOST = 'https://stable.dev.lcip.org'
# FXA_RELIER_CONTENT_OAUTH = 'https://oauth-stable.dev.lcip.org/v1'
# FXA_RELIER_REDIRECT_URI = 'http://localhost:8000/'
FXA_RELIER_CLIENT_ID = ''
FXA_RELIER_CONTENT_HOST = ''
FXA_RELIER_CONTENT_OAUTH = ''
FXA_RELIER_REDIRECT_URI = ''

# Link to Firefox for Android on the Google Play store with Google Analytics
# campaign parameters
GOOGLE_PLAY_FIREFOX_LINK = ('https://play.google.com/store/apps/details?' +
                            'id=org.mozilla.firefox&referrer=' +
                            urlquote('utm_source=mozilla&utm_medium=Referral&'
                                        'utm_campaign=mozilla-org'))

# Use bedrock Gruntfile.js for live reload
USE_GRUNT_LIVERELOAD = False

# Publishing system config
RNA = {
    'BASE_URL': os.environ.get('RNA_BASE_URL', 'https://nucleus.mozilla.org/rna/'),

    # default False as temporary workaround for bug 973499
    'VERIFY_SSL_CERT': os.environ.get('VERIFY_SSL_CERT', False),
}

MOFO_SECURITY_ADVISORIES_PATH = abspath(path('..', 'mofo_security_advisories'))
MOFO_SECURITY_ADVISORIES_REPO = 'https://github.com/mozilla/foundation-security-advisories.git'

CORS_URLS = {
    r'^/([a-zA-Z-]+/)?shapeoftheweb': '*',
}

LOGGING = {
    'root': {
        'level': 'WARNING',
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

PASSWORD_HASHERS = ['django.contrib.auth.hashers.PBKDF2PasswordHasher']

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rna.serializers.HyperlinkedModelSerializerWithPkField',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_FILTER_BACKENDS': ('rna.filters.TimestampedFilterBackend',)
}

FIREFOX_OS_FEEDS = (
    ('de', 'https://blog.mozilla.org/press-de/category/firefox-os/feed/'),
    ('en-US', 'https://blog.mozilla.org/blog/category/firefox-os/feed/'),
    ('es-ES', 'https://blog.mozilla.org/press-es/category/firefox-os/feed/'),
    ('es', 'https://blog.mozilla.org/press-latam/category/firefox-os/feed/'),
    ('fr', 'https://blog.mozilla.org/press-fr/category/firefox-os/feed/'),
    ('it', 'https://blog.mozilla.org/press-it/category/firefox-os/feed/'),
    ('pl', 'https://blog.mozilla.org/press-pl/category/firefox-os/feed/'),
    ('pt-BR', 'https://blog.mozilla.org/press-br/category/firefox-os/feed/'),
)
FIREFOX_OS_FEED_LOCALES = [feed[0] for feed in FIREFOX_OS_FEEDS]

TABLEAU_DB_URL = None

MAXMIND_DB_PATH = os.getenv('MAXMIND_DB_PATH', path('GeoIP2-Country.mmdb'))
MAXMIND_DEFAULT_COUNTRY = os.getenv('MAXMIND_DEFAULT_COUNTRY', 'US')
