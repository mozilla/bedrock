# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import hashlib
import hmac
import re
from collections import OrderedDict
from time import time
from urlparse import urlparse

from django.conf import settings
from django.http import (Http404, HttpResponseRedirect,
                         HttpResponsePermanentRedirect)
from django.utils.cache import patch_response_headers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.views.generic.base import TemplateView

import basket
import querystringsafe_base64
from product_details.version_compare import Version

from lib import l10n_utils
from lib.l10n_utils.dotlang import lang_file_is_active
from bedrock.base.urlresolvers import reverse
from bedrock.firefox.firefox_details import firefox_desktop, firefox_android
from bedrock.firefox.forms import SendToDeviceWidgetForm
from bedrock.mozorg.util import HttpResponseJSON
from bedrock.newsletter.forms import NewsletterFooterForm
from bedrock.releasenotes import version_re
from bedrock.wordpress.views import BlogPostsView


UA_REGEXP = re.compile(r"Firefox/(%s)" % version_re)

INSTALLER_CHANNElS = [
    'release',
    'beta',
    'alpha',
    # 'nightly',  # soon
]

SEND_TO_DEVICE_MESSAGE_SETS = {
    'default': {
        'sms': {
            'ios': 'ff-ios-download',
            'android': 'SMS_Android',
        },
        'email': {
            'android': 'download-firefox-android',
            'ios': 'download-firefox-ios',
            'all': 'download-firefox-mobile',
        }
    },
    'fx-android': {
        'sms': {
            'ios': 'ff-ios-download',
            'android': 'android-download-embed',
        },
        'email': {
            'android': 'get-android-embed',
            'ios': 'download-firefox-ios',
            'all': 'download-firefox-mobile',
        }
    },
    'fx-mobile-download-desktop': {
        'sms': {
            'all': 'mobile-heartbeat',
        },
        'email': {
            'all': 'download-firefox-mobile-reco',
        }
    },
    'fx-50-whatsnew': {
        'sms': {
            'all': 'whatsnewfifty',
        },
        'email': {
            'all': 'download-firefox-mobile-whatsnew',
        }
    }
}

STUB_VALUE_NAMES = [
    # name, default value
    ('utm_source', '(not set)'),
    ('utm_medium', '(direct)'),
    ('utm_campaign', '(not set)'),
    ('utm_content', '(not set)'),
]
STUB_VALUE_RE = re.compile(r'^[a-z0-9-.%()_]+$', flags=re.IGNORECASE)


def installer_help(request):
    installer_lang = request.GET.get('installer_lang', None)
    installer_channel = request.GET.get('channel', None)
    context = {
        'installer_lang': None,
        'installer_channel': None,
    }

    if installer_lang and installer_lang in firefox_desktop.languages:
        context['installer_lang'] = installer_lang

    if installer_channel and installer_channel in INSTALLER_CHANNElS:
        context['installer_channel'] = installer_channel

    return l10n_utils.render(request, 'firefox/installer-help.html', context)


@require_GET
def stub_attribution_code(request):
    """Return a JSON response containing the HMAC signed stub attribution value"""
    if not request.is_ajax():
        return HttpResponseJSON({'error': 'Resource only available via XHR'}, status=400)

    response = None
    rate = settings.STUB_ATTRIBUTION_RATE
    key = settings.STUB_ATTRIBUTION_HMAC_KEY
    if not rate:
        # return as though it was rate limited, since it was
        response = HttpResponseJSON({'error': 'rate limited'}, status=429)
    elif not key:
        response = HttpResponseJSON({'error': 'service not configured'}, status=403)

    if response:
        patch_response_headers(response, 300)  # 5 min
        return response

    data = request.GET
    codes = OrderedDict()
    has_value = False
    for name, default_value in STUB_VALUE_NAMES:
        val = data.get(name, '')
        # remove utm_
        name = name[4:]
        if val and STUB_VALUE_RE.match(val):
            codes[name] = val
            has_value = True
        else:
            codes[name] = default_value

    if codes['source'] == '(not set)' and 'referrer' in data:
        try:
            codes['source'] = urlparse(data['referrer']).netloc
            codes['medium'] = 'referral'
            has_value = True
        except Exception:
            # any problems and we should just ignore it
            pass

    if has_value:
        codes['timestamp'] = str(int(time()))
        code = '&'.join('='.join(attr) for attr in codes.items())
        code = querystringsafe_base64.encode(code)
        sig = hmac.new(key, code, hashlib.sha256).hexdigest()
        response = HttpResponseJSON({
            'attribution_code': code,
            'attribution_sig': sig,
        })
    else:
        response = HttpResponseJSON({'error': 'no params'}, status=400)

    patch_response_headers(response, 300)  # 5 min
    return response


@require_POST
@csrf_exempt
def send_to_device_ajax(request):
    locale = l10n_utils.get_locale(request)
    phone_or_email = request.POST.get('phone-or-email')

    # ensure a value was entered in phone or email field
    if not phone_or_email:
        return HttpResponseJSON({'success': False, 'errors': ['phone-or-email']})

    # pull message set from POST (not part of form, so wont be in cleaned_data)
    message_set = request.POST.get('message-set', 'default')

    # begin collecting data to pass to form constructor
    data = {
        'platform': request.POST.get('platform'),
    }

    # determine if email or phone number was submitted
    data_type = 'email' if '@' in phone_or_email else 'number'

    # populate data type in form data dict
    data[data_type] = phone_or_email

    # instantiate the form with processed POST data
    form = SendToDeviceWidgetForm(data)

    if form.is_valid():
        phone_or_email = form.cleaned_data.get(data_type)
        platform = form.cleaned_data.get('platform')

        # if no platform specified, default to 'all'
        if not platform:
            platform = 'all'

        # ensure we have a valid message set. if not, fall back to default
        if message_set not in SEND_TO_DEVICE_MESSAGE_SETS:
            MESSAGES = SEND_TO_DEVICE_MESSAGE_SETS['default']
        else:
            MESSAGES = SEND_TO_DEVICE_MESSAGE_SETS[message_set]

        if data_type == 'number':
            if platform in MESSAGES['sms']:
                try:
                    basket.send_sms(phone_or_email, MESSAGES['sms'][platform])
                except basket.BasketException:
                    return HttpResponseJSON({'success': False, 'errors': ['system']},
                                            status=400)
            else:
                return HttpResponseJSON({'success': False, 'errors': ['platform']})
        else:  # email
            if platform in MESSAGES['email']:
                try:
                    basket.subscribe(phone_or_email, MESSAGES['email'][platform],
                                     source_url=request.POST.get('source-url'),
                                     lang=locale)
                except basket.BasketException:
                    return HttpResponseJSON({'success': False, 'errors': ['system']},
                                            status=400)
            else:
                return HttpResponseJSON({'success': False, 'errors': ['platform']})

        resp_data = {'success': True}
    else:
        resp_data = {
            'success': False,
            'errors': form.errors.keys(),
        }

    return HttpResponseJSON(resp_data)


def windows_billboards(req):
    major_version = req.GET.get('majorVersion')
    minor_version = req.GET.get('minorVersion')

    if major_version and minor_version:
        major_version = float(major_version)
        minor_version = float(minor_version)
        if major_version == 5 and minor_version == 1:
            return l10n_utils.render(req, 'firefox/unsupported/winxp.html')
    return l10n_utils.render(req, 'firefox/unsupported/win2k.html')


def dnt(request):
    response = l10n_utils.render(request, 'firefox/dnt.html')
    response['Vary'] = 'DNT'
    return response


def all_downloads(request, platform, channel):
    if platform is None:
        platform = 'desktop'
    if platform == 'desktop':
        product = firefox_desktop
    if platform == 'android':
        product = firefox_android

    if channel is None:
        channel = 'release'
    if channel in ['developer', 'aurora']:
        channel = 'alpha'
    if channel == 'organizations':
        channel = 'esr'

    # Since the regex in urls.py matches various URL patterns, we have to handle
    # nonexistent pages here as 404 Not Found
    if platform == 'ios':
        raise Http404
    if platform == 'android' and channel == 'esr':
        raise Http404

    # Aurora for Android is gone; the population has been migrated to Nightly.
    # Redirect /firefox/android/aurora/all/ to /firefox/android/nightly/all/
    if platform == 'android' and channel == 'alpha':
        return HttpResponsePermanentRedirect(
            reverse('firefox.all', kwargs={'platform': 'android', 'channel': 'nightly'}))

    version = product.latest_version(channel)
    query = request.GET.get('q')

    context = {
        'platform': platform,
        'platforms': product.platforms(channel),
        'full_builds_version': version.split('.', 1)[0],
        'full_builds': product.get_filtered_full_builds(channel, version, query),
        'test_builds': product.get_filtered_test_builds(channel, version, query),
        'query': query,
        'channel': channel,
        'channel_label': product.channel_labels.get(channel, 'Firefox'),
    }

    if platform == 'desktop' and channel == 'esr':
        next_version = firefox_desktop.latest_version('esr_next')
        if next_version:
            context['full_builds_next_version'] = next_version.split('.', 1)[0]
            context['full_builds_next'] = firefox_desktop.get_filtered_full_builds('esr_next',
                                                                                   next_version, query)
            context['test_builds_next'] = firefox_desktop.get_filtered_test_builds('esr_next',
                                                                                   next_version, query)
    return l10n_utils.render(request, 'firefox/all.html', context)


def detect_channel(version):
    match = re.match(r'\d{1,2}', version)
    if match:
        num_version = int(match.group(0))
        if num_version >= 35:
            if version.endswith('a1'):
                return 'nightly'
            if version.endswith('a2'):
                return 'alpha'

    return 'unknown'


def show_38_0_5_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('38.0.5')


def show_42_whatsnew(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('42.0')


def show_49_0_whatsnew(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version == Version('49.0')


def show_50_whatsnew(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('50.0')


def show_54_whatsnew(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('54.0')


def show_40_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('40.0')


class FirstrunView(l10n_utils.LangFilesMixin, TemplateView):
    def get_context_data(self, **kwargs):
        ctx = super(FirstrunView, self).get_context_data(**kwargs)

        # add version to context for use in templates
        ctx['version'] = self.kwargs.get('version') or ''

        return ctx

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)
        version = self.kwargs.get('version') or ''

        if detect_channel(version) == 'alpha':
            template = 'firefox/dev-firstrun.html'
        elif show_40_firstrun(version):
            if lang_file_is_active('firefox/new/onboarding', locale):
                template = 'firefox/firstrun/onboarding.html'
            else:
                template = 'firefox/firstrun/firstrun-horizon.html'
        elif show_38_0_5_firstrun(version):
            template = 'firefox/australis/fx38_0_5/firstrun.html'
        else:
            template = 'firefox/australis/firstrun.html'

        # return a list to conform with original intention
        return [template]


class WhatsnewView(l10n_utils.LangFilesMixin, TemplateView):
    def get_context_data(self, **kwargs):
        ctx = super(WhatsnewView, self).get_context_data(**kwargs)

        # add version to context for use in templates
        version = self.kwargs.get('version') or ''
        match = re.match(r'\d{1,2}', version)
        ctx['version'] = version
        ctx['num_version'] = int(match.group(0)) if match else ''

        return ctx

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)

        version = self.kwargs.get('version') or ''
        oldversion = self.request.GET.get('oldversion', '')
        # old versions of Firefox sent a prefixed version
        if oldversion.startswith('rv:'):
            oldversion = oldversion[3:]

        channel = detect_channel(version)
        if channel == 'alpha':
            template = 'firefox/dev-whatsnew.html'
        elif channel == 'nightly':
            template = 'firefox/nightly_whatsnew.html'
        elif show_54_whatsnew(version):
            # ja, zh-CN, and zh-TW have locale-specific templates
            template = 'firefox/whatsnew/fx54/whatsnew-54.html'
        elif show_50_whatsnew(version):
            # zh-TW has locale-specific template: whatsnew-50.zh-TW.html
            template = 'firefox/whatsnew/whatsnew-50.html'
        # zh-TW on 49.0 gets a special template
        elif locale == 'zh-TW' and show_49_0_whatsnew(version):
            template = 'firefox/whatsnew/whatsnew-zh-tw-49.html'
        elif show_42_whatsnew(version):
            template = 'firefox/whatsnew/whatsnew-42.html'
        else:
            template = 'firefox/australis/whatsnew.html'

        # return a list to conform with original intention
        return [template]


class FeedbackView(TemplateView):

    donate_url = ('https://donate.mozilla.org/'
       '?utm_source=Heartbeat_survey&utm_medium=referral'
       '&utm_content=Heartbeat_{0}stars')

    def get_score(self):
        return self.request.GET.get('score', 0)

    def get_template_names(self):
        score = self.get_score()
        if score > '3':
            template = 'firefox/feedback/happy.html'
        else:
            template = 'firefox/feedback/unhappy.html'

        return [template]

    def get_context_data(self, **kwargs):
        context = super(FeedbackView, self).get_context_data(**kwargs)
        score = self.get_score()

        if score in ['3', '4', '5']:
            context['donate_stars_url'] = self.donate_url.format(score)

        return context


class TrackingProtectionTourView(l10n_utils.LangFilesMixin, TemplateView):
    template_name = 'firefox/tracking-protection-tour.html'


def new(request):
    # Remove legacy query parameters (Bug 1236791)
    if request.GET.get('product', None) or request.GET.get('os', None):
        return HttpResponsePermanentRedirect(reverse('firefox.new'))

    scene = request.GET.get('scene', None)
    experience = request.GET.get('xv', None)
    variant = request.GET.get('v', None)
    locale = l10n_utils.get_locale(request)

    if scene == '2':
        if locale == 'en-US':
            if experience == 'breakfree':
                template = 'firefox/new/break-free/scene2.html'
            elif experience == 'wayofthefox':
                template = 'firefox/new/way-of-the-fox/scene2.html'
            elif experience == 'privatenotoption':
                template = 'firefox/new/fx-lifestyle/private-not-option/scene2.html'
            elif experience == 'conformitynotdefault':
                template = 'firefox/new/fx-lifestyle/conformity-not-default/scene2.html'
            elif experience == 'browseuptoyou':
                template = 'firefox/new/fx-lifestyle/browse-up-to-you/scene2.html'
            elif experience == 'moreprotection':
                template = 'firefox/new/fx-lifestyle/more-protection/scene2.html'
            elif experience == 'workingout':
                template = 'firefox/new/fx-lifestyle/working-out/scene2.html'
            elif experience == 'youdoyou':
                template = 'firefox/new/fx-lifestyle/you-do-you/scene2.html'
            elif experience == 'itsyourweb':
                template = 'firefox/new/fx-lifestyle/its-your-web/scene2.html'
            elif experience in ['batmfree', 'batmprivate', 'batmnimble', 'batmresist']:
                template = 'firefox/new/batm/scene2.html'
            else:
                template = 'firefox/new/onboarding/scene2.html'
        elif lang_file_is_active('firefox/new/onboarding', locale):
            template = 'firefox/new/onboarding/scene2.html'
        else:
            template = 'firefox/new/scene2.html'
    # if no/incorrect scene specified, show scene 1
    else:
        if locale == 'en-US':
            if experience == 'breakfree':
                template = 'firefox/new/break-free/scene1.html'
            elif experience == 'wayofthefox':
                template = 'firefox/new/way-of-the-fox/scene1.html'
            elif experience == 'privatenotoption':
                template = 'firefox/new/fx-lifestyle/private-not-option/scene1.html'
            elif experience == 'conformitynotdefault':
                template = 'firefox/new/fx-lifestyle/conformity-not-default/scene1.html'
            elif experience == 'browseuptoyou':
                template = 'firefox/new/fx-lifestyle/browse-up-to-you/scene1.html'
            elif experience == 'moreprotection':
                template = 'firefox/new/fx-lifestyle/more-protection/scene1.html'
            elif experience == 'workingout':
                template = 'firefox/new/fx-lifestyle/working-out/scene1.html'
            elif experience == 'youdoyou':
                template = 'firefox/new/fx-lifestyle/you-do-you/scene1.html'
            elif experience == 'itsyourweb':
                template = 'firefox/new/fx-lifestyle/its-your-web/scene1.html'
            elif experience == 'batmfree':
                template = 'firefox/new/batm/free.html'
            elif experience == 'batmprivate':
                if variant == 'a':
                    template = 'firefox/new/batm/machine-a.html'
                elif variant == 'b':
                    template = 'firefox/new/batm/machine-b.html'
                else:
                    template = 'firefox/new/batm/private.html'
            elif experience == 'batmnimble':
                template = 'firefox/new/batm/nimble.html'
            elif experience == 'batmresist':
                template = 'firefox/new/batm/resist.html'
            else:
                template = 'firefox/new/onboarding/scene1.html'
        elif lang_file_is_active('firefox/new/onboarding', locale):
            template = 'firefox/new/onboarding/scene1.html'
        else:
            template = 'firefox/new/scene1.html'

    return l10n_utils.render(request, template)


def ios_testflight(request):
    # no country field, so no need to send locale
    newsletter_form = NewsletterFooterForm('ios-beta-test-flight', '')

    return l10n_utils.render(request,
                             'firefox/testflight.html',
                             {'newsletter_form': newsletter_form})


def features_landing(request):
    locale = l10n_utils.get_locale(request)

    if lang_file_is_active('firefox/features/index', locale):
        template = 'firefox/features/index.html'
    else:
        template = 'firefox/features.html'

    return l10n_utils.render(request, template)


class FeaturesPrivateBrowsingView(BlogPostsView):
    template_name = 'firefox/features/private-browsing.html'
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['privacy', 'security', 'featured']


class FeaturesFastView(BlogPostsView):
    template_name = 'firefox/features/fast.html'
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['fastest', 'featured']


class FeaturesIndependentView(BlogPostsView):
    template_name = 'firefox/features/independent.html'
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['browser', 'featured']


class FeaturesMemoryView(BlogPostsView):
    template_name = 'firefox/features/memory.html'
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['memory', 'featured']


class FeaturesBookmarksView(BlogPostsView):
    template_name = 'firefox/features/bookmarks.html'
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['modern', 'private', 'featured']


class FeaturesPasswordManagerView(BlogPostsView):
    template_name = 'firefox/features/password-manager.html'
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['modern', 'private', 'featured']


def FeaturesSyncView(request):
    locale = l10n_utils.get_locale(request)

    if locale.startswith('en-'):
        template = 'firefox/features/sync-en.html'
    else:
        template = 'firefox/features/sync.html'

    return l10n_utils.render(request, template)


class FirefoxProductDesktopView(BlogPostsView):
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['browser', 'featured']

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)

        if lang_file_is_active('firefox/products/desktop', locale):
            template_name = 'firefox/products/desktop.html'
        else:
            template_name = 'firefox/desktop/index.html'

        return [template_name]


class FirefoxProductAndroidView(BlogPostsView):
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['mobile', 'featured']

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)

        if lang_file_is_active('firefox/products/android', locale):
            template_name = 'firefox/products/android.html'
        else:
            template_name = 'firefox/android/index.html'

        return [template_name]


class FirefoxProductIOSView(BlogPostsView):
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['mobile', 'featured']

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)

        if lang_file_is_active('firefox/products/ios', locale):
            template_name = 'firefox/products/ios.html'
        else:
            template_name = 'firefox/ios.html'

        return [template_name]


class FirefoxFocusView(BlogPostsView):
    template_name = 'firefox/products/focus.html'
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['privacy', 'mobile', 'featured']


class FirefoxHubView(BlogPostsView):
    blog_posts_limit = 1
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['home']
    template_name = 'firefox/hub/home.html'

    def get(self, request, *args, **kwargs):
        locale = l10n_utils.get_locale(request)

        # If locale does not have hub page translated, redirect to /new.
        if lang_file_is_active('firefox/hub/home', locale):
            return super(FirefoxHubView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('firefox.new'))


def FirefoxProductDevEditionView(request, template='firefox/products/developer.html'):
    locale = l10n_utils.get_locale(request)

    if lang_file_is_active('firefox/products/developer', locale):
        template = 'firefox/products/developer.html'
    else:
        template = 'firefox/developer.html'

    return l10n_utils.render(request, template)
