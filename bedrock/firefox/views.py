# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import hashlib
import hmac
import re
from collections import OrderedDict
from urllib.parse import urlparse

import basket
import querystringsafe_base64
from django.conf import settings
from django.http import (
    HttpResponsePermanentRedirect,
    JsonResponse,
)

from django.utils.cache import patch_response_headers
from django.utils.encoding import force_text
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.generic.base import TemplateView
from lib import l10n_utils
from lib.l10n_utils import L10nTemplateView
from lib.l10n_utils.dotlang import lang_file_is_active
from lib.l10n_utils.fluent import ftl, ftl_file_is_active
from product_details.version_compare import Version

from bedrock.base.urlresolvers import reverse
from bedrock.base.waffle import switch
from bedrock.contentcards.models import get_page_content_cards
from bedrock.firefox.firefox_details import firefox_android, firefox_desktop
from bedrock.firefox.forms import SendToDeviceWidgetForm
from bedrock.newsletter.forms import NewsletterFooterForm
from bedrock.releasenotes import version_re
from bedrock.base.views import GeoRedirectView


UA_REGEXP = re.compile(r"Firefox/(%s)" % version_re)

INSTALLER_CHANNElS = [
    'release',
    'beta',
    'alpha',
    'nightly',
    'aurora',  # deprecated name for dev edition
]
SEND_TO_DEVICE_MESSAGE_SETS = settings.SEND_TO_DEVICE_MESSAGE_SETS

STUB_VALUE_NAMES = [
    # name, default value
    ('utm_source', '(not set)'),
    ('utm_medium', '(direct)'),
    ('utm_campaign', '(not set)'),
    ('utm_content', '(not set)'),
    ('experiment', '(not set)'),
    ('variation', '(not set)'),
    ('ua', '(not set)'),
]
STUB_VALUE_RE = re.compile(r'^[a-z0-9-.%():_]+$', flags=re.IGNORECASE)

class InstallerHelpView(L10nTemplateView):
    ftl_files_map = {
        'firefox/installer-help-redesign.html': ['firefox/installer-help']
    }

    def get_context_data(self, **kwargs):
        ctx = super(InstallerHelpView, self).get_context_data(**kwargs)
        installer_lang = self.request.GET.get('installer_lang', None)
        installer_channel = self.request.GET.get('channel', None)
        ctx['installer_lang'] = None
        ctx['installer_channel'] = None

        if installer_lang and installer_lang in firefox_desktop.languages:
            ctx['installer_lang'] = installer_lang

        if installer_channel and installer_channel in INSTALLER_CHANNElS:
            if installer_channel == 'aurora':
                ctx['installer_channel'] = 'alpha'
            else:
                ctx['installer_channel'] = installer_channel

        return ctx

    def get_template_names(self):
        if ftl_file_is_active('firefox/installer-help'):
            template_name = 'firefox/installer-help-redesign.html'
        else:
            template_name = 'firefox/installer-help.html'

        return [template_name]


@require_GET
def stub_attribution_code(request):
    """Return a JSON response containing the HMAC signed stub attribution value"""
    if not request.is_ajax():
        return JsonResponse({'error': 'Resource only available via XHR'}, status=400)

    response = None
    if not settings.STUB_ATTRIBUTION_RATE:
        # return as though it was rate limited, since it was
        response = JsonResponse({'error': 'rate limited'}, status=429)
    elif not settings.STUB_ATTRIBUTION_HMAC_KEY:
        response = JsonResponse({'error': 'service not configured'}, status=403)

    if response:
        patch_response_headers(response, 300)  # 5 min
        return response

    data = request.GET
    codes = OrderedDict()
    has_value = False
    for name, default_value in STUB_VALUE_NAMES:
        val = data.get(name, '')
        # remove utm_
        if name.startswith('utm_'):
            name = name[4:]

        if val and STUB_VALUE_RE.match(val):
            codes[name] = val
            has_value = True
        else:
            codes[name] = default_value

    if codes['source'] == '(not set)' and 'referrer' in data:
        try:
            domain = urlparse(data['referrer']).netloc
            if domain and STUB_VALUE_RE.match(domain):
                codes['source'] = domain
                codes['medium'] = 'referral'
                has_value = True
        except Exception:
            # any problems and we should just ignore it
            pass

    if not has_value:
        codes['source'] = 'www.mozilla.org'
        codes['medium'] = '(none)'

    code_data = sign_attribution_codes(codes)
    if code_data:
        response = JsonResponse(code_data)
    else:
        response = JsonResponse({'error': 'Invalid code'}, status=400)

    patch_response_headers(response, 300)  # 5 min
    return response


def get_attrribution_code(codes):
    """
    Take the attribution codes and return the URL encoded string
    respecting max length.
    """
    code = '&'.join('='.join(attr) for attr in codes.items())
    if len(codes['campaign']) > 5 and len(code) > settings.STUB_ATTRIBUTION_MAX_LEN:
        # remove 5 char at a time
        codes['campaign'] = codes['campaign'][:-5] + '_'
        code = get_attrribution_code(codes)

    return code


def sign_attribution_codes(codes):
    """
    Take the attribution codes and return the base64 encoded string
    respecting max length and HMAC signature.
    """
    key = settings.STUB_ATTRIBUTION_HMAC_KEY
    code = get_attrribution_code(codes)
    if len(code) > settings.STUB_ATTRIBUTION_MAX_LEN:
        return None

    code = querystringsafe_base64.encode(code.encode())
    sig = hmac.new(key.encode(), code, hashlib.sha256).hexdigest()
    return {'attribution_code': code.decode(), 'attribution_sig': sig}


@require_POST
@csrf_exempt
def send_to_device_ajax(request):
    locale = l10n_utils.get_locale(request)
    phone_or_email = request.POST.get('phone-or-email')

    # ensure a value was entered in phone or email field
    if not phone_or_email:
        return JsonResponse({'success': False, 'errors': ['phone-or-email']})

    # pull message set from POST (not part of form, so wont be in cleaned_data)
    message_set = request.POST.get('message-set', 'default')

    # begin collecting data to pass to form constructor
    data = {'platform': request.POST.get('platform')}

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

            # for testing purposes return success
            if phone_or_email == '5555555555':
                return JsonResponse({'success': True})

            if platform in MESSAGES['sms']:
                data = {
                    'mobile_number': phone_or_email,
                    'msg_name': MESSAGES['sms'][platform],
                    'lang': locale,
                }
                country = request.POST.get('country')
                if country and re.match(r'^[a-z]{2}$', country, flags=re.I):
                    data['country'] = country

                try:
                    basket.request('post', 'subscribe_sms', data=data)
                except basket.BasketException as e:
                    if e.desc == 'mobile_number is invalid':
                        return JsonResponse({'success': False, 'errors': ['number']})
                    else:
                        return JsonResponse(
                            {'success': False, 'errors': ['system']}, status=400
                        )
            else:
                return JsonResponse({'success': False, 'errors': ['platform']})
        else:  # email
            if platform in MESSAGES['email']:
                try:
                    basket.subscribe(
                        phone_or_email,
                        MESSAGES['email'][platform],
                        source_url=request.POST.get('source-url'),
                        lang=locale,
                    )
                except basket.BasketException:
                    return JsonResponse(
                        {'success': False, 'errors': ['system']}, status=400
                    )
            else:
                return JsonResponse({'success': False, 'errors': ['platform']})

        resp_data = {'success': True}
    else:
        resp_data = {'success': False, 'errors': list(form.errors)}

    return JsonResponse(resp_data)


def firefox_all(request):
    ftl_files = 'firefox/all'
    product_android = firefox_android
    product_desktop = firefox_desktop

    # Human-readable product labels
    products = OrderedDict(
        [
            ('desktop_release', ftl('firefox-all-product-firefox', ftl_files=ftl_files)),
            ('desktop_beta', ftl('firefox-all-product-firefox-beta', ftl_files=ftl_files)),
            ('desktop_developer', ftl('firefox-all-product-firefox-developer', ftl_files=ftl_files)),
            ('desktop_nightly', ftl('firefox-all-product-firefox-nightly', ftl_files=ftl_files)),
            ('desktop_esr', ftl('firefox-all-product-firefox-esr', ftl_files=ftl_files)),
            ('android_release', ftl('firefox-all-product-firefox-android', ftl_files=ftl_files)),
            ('android_beta', ftl('firefox-all-product-firefox-android-beta', ftl_files=ftl_files)),
            ('android_nightly', ftl('firefox-all-product-firefox-android-nightly', ftl_files=ftl_files)),
        ]
    )

    channel_release = 'release'
    channel_beta = 'beta'
    channel_dev = 'devedition'
    channel_nightly = 'nightly'
    channel_esr = 'esr'
    channel_esr_next = 'esr_next'

    latest_release_version_desktop = product_desktop.latest_version(channel_release)
    latest_beta_version_desktop = product_desktop.latest_version(channel_beta)
    latest_developer_version_desktop = product_desktop.latest_version(channel_dev)
    latest_nightly_version_desktop = product_desktop.latest_version(channel_nightly)
    latest_esr_version_desktop = product_desktop.latest_version(channel_esr)
    latest_esr_next_version_desktop = product_desktop.latest_version(channel_esr_next)

    latest_release_version_android = product_android.latest_version(channel_release)
    latest_beta_version_android = product_android.latest_version(channel_beta)
    latest_nightly_version_android = product_android.latest_version(channel_nightly)

    context = {
        'products': products.items(),
        'desktop_release_platforms': product_desktop.platforms(channel_release),
        'desktop_release_full_builds': product_desktop.get_filtered_full_builds(
            channel_release, latest_release_version_desktop
        ),
        'desktop_release_channel_label': product_desktop.channel_labels.get(
            channel_release, 'Firefox'
        ),
        'desktop_release_latest_version': latest_release_version_desktop,
        'desktop_beta_platforms': product_desktop.platforms(channel_beta),
        'desktop_beta_full_builds': product_desktop.get_filtered_full_builds(
            channel_beta, latest_beta_version_desktop
        ),
        'desktop_beta_channel_label': product_desktop.channel_labels.get(
            channel_beta, 'Firefox'
        ),
        'desktop_beta_latest_version': latest_beta_version_desktop,
        'desktop_developer_platforms': product_desktop.platforms(channel_dev),
        'desktop_developer_full_builds': product_desktop.get_filtered_full_builds(
            channel_dev, latest_developer_version_desktop
        ),
        'desktop_developer_channel_label': product_desktop.channel_labels.get(
            channel_dev, 'Firefox'
        ),
        'desktop_developer_latest_version': latest_developer_version_desktop,
        'desktop_nightly_platforms': product_desktop.platforms(channel_nightly),
        'desktop_nightly_full_builds': product_desktop.get_filtered_full_builds(
            channel_nightly, latest_nightly_version_desktop
        ),
        'desktop_nightly_channel_label': product_desktop.channel_labels.get(
            channel_nightly, 'Firefox'
        ),
        'desktop_nightly_latest_version': latest_nightly_version_desktop,
        'desktop_esr_platforms': product_desktop.platforms(channel_esr),
        'desktop_esr_full_builds': product_desktop.get_filtered_full_builds(
            channel_esr, latest_esr_version_desktop
        ),
        'desktop_esr_channel_label': product_desktop.channel_labels.get(
            channel_esr, 'Firefox'
        ),
        'desktop_esr_latest_version': latest_esr_version_desktop,
        'android_release_platforms': product_android.platforms(channel_release),
        'android_release_full_builds': product_android.get_filtered_full_builds(
            channel_release, latest_release_version_android
        ),
        'android_release_channel_label': product_android.channel_labels.get(
            channel_release, 'Firefox'
        ),
        'android_release_latest_version': latest_release_version_android,
        'android_beta_platforms': product_android.platforms(channel_beta),
        'android_beta_full_builds': product_android.get_filtered_full_builds(
            channel_beta, latest_beta_version_android
        ),
        'android_beta_channel_label': product_android.channel_labels.get(
            channel_beta, 'Firefox'
        ),
        'android_beta_latest_version': latest_beta_version_android,
        'android_nightly_platforms': product_android.platforms(channel_nightly),
        'android_nightly_full_builds': product_android.get_filtered_full_builds(
            channel_nightly, latest_nightly_version_android
        ),
        'android_nightly_channel_label': product_android.channel_labels.get(
            channel_nightly, 'Firefox'
        ),
        'android_nightly_latest_version': latest_nightly_version_android,
    }

    if latest_esr_next_version_desktop:
        context['desktop_esr_platforms_next'] = product_desktop.platforms(
            channel_esr_next, True
        )
        context[
            'desktop_esr_full_builds_next'
        ] = product_desktop.get_filtered_full_builds(
            channel_esr_next, latest_esr_next_version_desktop
        )
        context['desktop_esr_channel_label_next'] = (
            product_desktop.channel_labels.get(channel_esr_next, 'Firefox'),
        )
        context['desktop_esr_next_version'] = latest_esr_next_version_desktop

    return l10n_utils.render(request, 'firefox/all-unified.html',
                             context, ftl_files=ftl_files)


def detect_channel(version):
    match = re.match(r'\d{1,2}', version)
    if match:
        num_version = int(match.group(0))
        if num_version >= 35:
            if version.endswith('a1'):
                return 'nightly'
            if version.endswith('a2'):
                return 'developer'
            if version.endswith('beta'):
                return 'beta'

    return 'unknown'


def show_38_0_5_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('38.0.5')


def show_57_dev_whatsnew(version):
    version = version[:-2]
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('57.0')


def show_62_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('62.0')


def show_57_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('57.0')


def show_57_dev_firstrun(version):
    version = version[:-2]
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('57.0')


def show_70_0_2_whatsnew(oldversion):
    try:
        oldversion = Version(oldversion)
    except ValueError:
        return False

    return oldversion >= Version('70.0')


def redirect_old_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version < Version('40.0')


def show_default_account_whatsnew(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('60.0')


def show_firefox_lite_whatsnew(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    if not switch('firefox-lite-whatsnew'):
        return False

    return version >= Version('79.0')


class FirstrunView(l10n_utils.LangFilesMixin, TemplateView):
    def get(self, *args, **kwargs):
        version = self.kwargs.get('version') or ''

        # redirect legacy /firstrun URLs to /firefox/new/
        if redirect_old_firstrun(version):
            return HttpResponsePermanentRedirect(reverse('firefox.new'))
        else:
            return super(FirstrunView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(FirstrunView, self).get_context_data(**kwargs)

        # add version to context for use in templates
        ctx['version'] = self.kwargs.get('version') or ''

        return ctx

    def get_template_names(self):
        version = self.kwargs.get('version') or ''

        if detect_channel(version) == 'developer':
            if show_57_dev_firstrun(version):
                template = 'firefox/developer/firstrun.html'
            else:
                template = 'firefox/firstrun/firstrun.html'
        else:
            template = 'firefox/firstrun/firstrun.html'

        # return a list to conform with original intention
        return [template]


class WhatsNewRedirectorView(GeoRedirectView):
    # https://bedrock.readthedocs.io/en/latest/coding.html#geo-redirect-view
    geo_urls = {
        'IN': 'firefox.whatsnew.india',
        'NG': 'firefox.whatsnew.africa',
        'ZA': 'firefox.whatsnew.africa',
        'KE': 'firefox.whatsnew.africa',
        'GH': 'firefox.whatsnew.africa',
        'UG': 'firefox.whatsnew.africa',
        'TZ': 'firefox.whatsnew.africa',
        'ZW': 'firefox.whatsnew.africa',
        'ZM': 'firefox.whatsnew.africa',
    }
    default_url = 'firefox.whatsnew.all'

    def get_redirect_url(self, *args, **kwargs):
        if 'version' in kwargs and kwargs['version'] is None:
            del kwargs['version']

        return super().get_redirect_url(*args, **kwargs)


class WhatsnewView(L10nTemplateView):

    ftl_files_map = {
        'firefox/nightly/whatsnew.html': ['firefox/nightly/whatsnew', 'firefox/whatsnew/whatsnew'],
        'firefox/whatsnew/index-account.html': ['firefox/whatsnew/whatsnew-account', 'firefox/whatsnew/whatsnew'],
        'firefox/whatsnew/index.html': ['firefox/whatsnew/whatsnew-s2d', 'firefox/whatsnew/whatsnew'],
        'firefox/whatsnew/whatsnew-fx79.html': ['firefox/whatsnew/whatsnew-fx79', 'firefox/whatsnew/whatsnew'],
        'firefox/whatsnew/whatsnew-fx80.html': ['firefox/whatsnew/whatsnew-fx80', 'firefox/whatsnew/whatsnew'],
        'firefox/whatsnew/whatsnew-fx81.html': ['firefox/whatsnew/whatsnew-fx81', 'firefox/whatsnew/whatsnew'],
    }

    def get_context_data(self, **kwargs):
        ctx = super(WhatsnewView, self).get_context_data(**kwargs)
        version = self.kwargs.get('version') or ''
        pre_release_channels = ['nightly', 'developer', 'beta']
        channel = detect_channel(version)

        # add active_locales for hard-coded locale templates
        locale = l10n_utils.get_locale(self.request)
        hard_coded_templates = ['id']
        if locale in hard_coded_templates and channel not in pre_release_channels:
            ctx['active_locales'] = locale

        # add version to context for use in templates
        match = re.match(r'\d{1,2}', version)
        num_version = int(match.group(0)) if match else ''
        ctx['version'] = version
        ctx['num_version'] = num_version

        # add analytics parameters to context for use in templates
        if channel not in pre_release_channels:
            channel = ''

        analytics_version = str(num_version) + channel
        entrypoint = 'mozilla.org-whatsnew' + analytics_version
        if version.startswith('79.') and channel not in ['nightly', 'developer', 'beta']:
            campaign = 'mozilla-vpn-v1-0-announcement'
        else:
            campaign = 'whatsnew' + analytics_version
        ctx['analytics_version'] = analytics_version
        ctx['entrypoint'] = entrypoint
        ctx['campaign'] = campaign
        ctx['utm_params'] = 'utm_source={0}&utm_medium=referral&utm_campaign={1}&entrypoint={2}'.format(
                             entrypoint, campaign, entrypoint)

        return ctx

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)

        version = self.kwargs.get('version') or ''
        oldversion = self.request.GET.get('oldversion', '')
        # old versions of Firefox sent a prefixed version
        if oldversion.startswith('rv:'):
            oldversion = oldversion[3:]

        channel = detect_channel(version)

        if channel == 'nightly':
            template = 'firefox/nightly/whatsnew.html'
        elif channel == 'developer':
            if show_57_dev_whatsnew(version):
                template = 'firefox/developer/whatsnew.html'
            else:
                template = 'firefox/whatsnew/index.html'
        elif locale == 'id' and show_firefox_lite_whatsnew(version):
            template = 'firefox/whatsnew/firefox-lite.id.html'
        elif version.startswith('81.') and ftl_file_is_active('firefox/whatsnew/whatsnew-fx81'):
            template = 'firefox/whatsnew/whatsnew-fx81.html'
        elif version.startswith('80.') and ftl_file_is_active('firefox/whatsnew/whatsnew-fx80'):
            template = 'firefox/whatsnew/whatsnew-fx80.html'
        elif version.startswith('79.') and ftl_file_is_active('firefox/whatsnew/whatsnew-fx79'):
            template = 'firefox/whatsnew/whatsnew-fx79.html'
        elif version.startswith('78.'):
            template = 'firefox/whatsnew/index.html'
        elif version.startswith('77.') and lang_file_is_active('firefox/whatsnew_77', locale):
            # YouTube is blocked in China so zh-CN gets an alternative, self-hosted video.
            # If we run into bandwidth trouble we can turn the video off and zh-CN falls back to the 76 page.
            if locale == 'zh-CN' and not switch('firefox-whatsnew77-video-zhCN'):
                template = 'firefox/whatsnew/whatsnew-fx76.html'
            else:
                template = 'firefox/whatsnew/whatsnew-fx77.html'
        elif version.startswith('76.') and lang_file_is_active('firefox/whatsnew_76', locale):
            template = 'firefox/whatsnew/whatsnew-fx76.html'
        else:
            if show_default_account_whatsnew(version) and ftl_file_is_active('firefox/whatsnew/whatsnew-account'):
                template = 'firefox/whatsnew/index-account.html'
            else:
                template = 'firefox/whatsnew/index.html'

        # return a list to conform with original intention
        return [template]


class WhatsNewFirefoxLiteView(WhatsnewView):
    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)
        version = self.kwargs.get('version') or ''
        channel = detect_channel(version)
        pre_release_channels = ['nightly', 'alpha', 'beta']

        if show_firefox_lite_whatsnew(version) and locale == 'en-US' and channel not in pre_release_channels:
            # return a list to conform with original intention
            template = ['firefox/whatsnew/firefox-lite.html']
        else:
            template = super().get_template_names()

        return template


class DownloadThanksView(L10nTemplateView):
    ftl_files_map = {
        'firefox/new/trailhead/thanks.html': ['firefox/new/download'],
        'firefox/new/desktop/thanks.html': ['firefox/new/desktop'],
    }
    activation_files = [
        'firefox/new/download',
        'firefox/new/desktop',
    ]

    # place expected ?v= values in this list
    variations = ['a', 'b', 'c']

    def get_context_data(self, **kwargs):
        ctx = super(DownloadThanksView, self).get_context_data(**kwargs)
        variant = self.request.GET.get('v', None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        ctx['variant'] = variant

        return ctx

    def get_template_names(self):

        if ftl_file_is_active('firefox/new/desktop') and switch('new-redesign'):
            template = 'firefox/new/desktop/thanks.html'
        else:
            template = 'firefox/new/trailhead/thanks.html'

        return [template]


class NewView(L10nTemplateView):
    ftl_files_map = {
        'firefox/new/trailhead/download.html': ['firefox/new/download', 'banners/firefox-mobile'],
        'firefox/new/trailhead/download-yandex.html': ['firefox/new/download', 'banners/firefox-mobile'],
        'firefox/new/desktop/download.html': ['firefox/new/desktop'],
    }
    activation_files = [
        'firefox/new/download',
        'firefox/new/desktop',
    ]

    # place expected ?v= values in this list
    variations = ['a', 'b']

    def get(self, *args, **kwargs):
        # Remove legacy query parameters (Bug 1236791)
        if self.request.GET.get('product', None) or self.request.GET.get('os', None):
            return HttpResponsePermanentRedirect(reverse('firefox.new'))

        scene = self.request.GET.get('scene', None)
        if scene == '2':
            # send to new permanent scene2 URL (bug 1438302)
            thanks_url = reverse('firefox.download.thanks')
            query_string = self.request.META.get('QUERY_STRING', '')
            if query_string:
                thanks_url = '?'.join(
                    [thanks_url, force_text(query_string, errors='ignore')]
                )
            return HttpResponsePermanentRedirect(thanks_url)

        return super(NewView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(NewView, self).get_context_data(**kwargs)

        # note: v and xv params only allow a-z, A-Z, 0-9, -, and _ characters
        variant = self.request.GET.get('v', None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        ctx['variant'] = variant

        return ctx

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)
        variant = self.request.GET.get('v', None)

        # ensure variant matches pre-defined value
        if variant not in self.variations:
            variant = None

        if locale == 'ru' and switch('firefox-yandex'):
            template = 'firefox/new/trailhead/download-yandex.html'
        elif ftl_file_is_active('firefox/new/desktop') and switch('new-redesign'):
            template = 'firefox/new/desktop/download.html'
        else:
            template = 'firefox/new/trailhead/download.html'

        return [template]


def ios_testflight(request):
    # no country field, so no need to send locale
    newsletter_form = NewsletterFooterForm('ios-beta-test-flight', '')

    return l10n_utils.render(
        request, 'firefox/testflight.html', {'newsletter_form': newsletter_form}
    )


class FirefoxHomeView(L10nTemplateView):
    ftl_files_map = {
        'firefox/home/index-master.html': ['firefox/home']
    }
    activation_files = ['firefox/home', 'firefox/home/index-quantum.html']

    def get_template_names(self):
        if ftl_file_is_active('firefox/home'):
            template_name = 'firefox/home/index-master.html'
        else:
            template_name = 'firefox/home/index-quantum.html'

        return [template_name]


def election_with_cards(request):
    locale = l10n_utils.get_locale(request)
    ctx = {
        'page_content_cards': get_page_content_cards('election-en', locale),
        'active_locales': ['de', 'fr', 'en-US'],
    }

    if locale == 'de':
        template_name = 'firefox/election/index-de.html'
        ctx['page_content_cards'] = get_page_content_cards('election-de', 'de')
    elif locale == 'fr':
        template_name = 'firefox/election/index-fr.html'
        ctx['page_content_cards'] = get_page_content_cards('election-fr', 'fr')
    else:
        template_name = 'firefox/election/index.html'
        ctx['page_content_cards'] = get_page_content_cards('election-en', 'en-US')

    return l10n_utils.render(request, template_name, ctx)


BREACH_TIPS_URLS = {
    'de': 'https://blog.mozilla.org/firefox/de/was-macht-man-nach-einem-datenleck/',
    'fr': 'https://blog.mozilla.org/firefox/fr/que-faire-en-cas-de-fuite-de-donnees/',
    'en-CA': 'https://blog.mozilla.org/firefox/what-to-do-after-a-data-breach/',
    'en-GB': 'https://blog.mozilla.org/firefox/what-to-do-after-a-data-breach/',
    'en-US': 'https://blog.mozilla.org/firefox/what-to-do-after-a-data-breach/',
}


def firefox_welcome_page1(request):
    locale = l10n_utils.get_locale(request)

    # get localized blog post URL for 2019 page
    breach_tips_query = (
        '?utm_source=mozilla.org-firefox-welcome-1&amp;utm_medium=referral'
        '&amp;utm_campaign=welcome-1-monitor&amp;entrypoint=mozilla.org-firefox-welcome-1'
    )
    breach_tips_url = BREACH_TIPS_URLS.get(locale, BREACH_TIPS_URLS['en-US'])

    context = {'breach_tips_url': breach_tips_url + breach_tips_query}

    template_name = 'firefox/welcome/page1.html'

    return l10n_utils.render(request, template_name, context,
                             ftl_files='firefox/welcome/page1')
