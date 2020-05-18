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
from lib.l10n_utils.fluent import ftl_file_is_active
from product_details.version_compare import Version

from bedrock.base.urlresolvers import reverse
from bedrock.base.waffle import switch
from bedrock.contentcards.models import get_page_content_cards
from bedrock.firefox.firefox_details import firefox_android, firefox_desktop
from bedrock.firefox.forms import SendToDeviceWidgetForm
from bedrock.newsletter.forms import NewsletterFooterForm
from bedrock.releasenotes import version_re
from bedrock.wordpress.views import BlogPostsView
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


def installer_help(request):
    locale = l10n_utils.get_locale(request)
    installer_lang = request.GET.get('installer_lang', None)
    installer_channel = request.GET.get('channel', None)
    context = {'installer_lang': None, 'installer_channel': None}

    if installer_lang and installer_lang in firefox_desktop.languages:
        context['installer_lang'] = installer_lang

    if installer_channel and installer_channel in INSTALLER_CHANNElS:
        if installer_channel == 'aurora':
            context['installer_channel'] = 'alpha'
        else:
            context['installer_channel'] = installer_channel

    if lang_file_is_active('firefox/installer-help-redesign', locale):
        template = 'firefox/installer-help-redesign.html'
    else:
        template = 'firefox/installer-help.html'

    return l10n_utils.render(request, template, context)


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
    product_android = firefox_android
    product_desktop = firefox_desktop

    # Human-readable product labels
    products = OrderedDict(
        [
            ('desktop_release', 'Firefox'),
            ('desktop_beta', 'Firefox Beta'),
            ('desktop_developer', 'Firefox Developer Edition'),
            ('desktop_nightly', 'Firefox Nightly'),
            ('desktop_esr', 'Firefox Extended Support Release'),
            ('android_release', 'Firefox Android'),
            ('android_beta', 'Firefox Android Beta'),
            ('android_nightly', 'Firefox Android Nightly'),
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

    return l10n_utils.render(request, 'firefox/all-unified.html', context)


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
    geo_urls = {
        'IN': 'firefox.whatsnew.india'
    }
    default_url = 'firefox.whatsnew.all'

    def get_redirect_url(self, *args, **kwargs):
        if 'version' in kwargs and kwargs['version'] is None:
            del kwargs['version']

        return super().get_redirect_url(*args, **kwargs)


class WhatsnewView(L10nTemplateView):

    ftl_files_map = {
        'firefox/whatsnew/index-account.html': ['firefox/whatsnew/whatsnew-account', 'firefox/whatsnew/whatsnew']
    }

    def get_context_data(self, **kwargs):
        ctx = super(WhatsnewView, self).get_context_data(**kwargs)

        # add version to context for use in templates
        version = self.kwargs.get('version') or ''
        match = re.match(r'\d{1,2}', version)
        num_version = int(match.group(0)) if match else ''
        ctx['version'] = version
        ctx['num_version'] = num_version

        # add analytics parameters to context for use in templates
        channel = detect_channel(version)
        if channel not in ['nightly', 'developer', 'beta']:
            channel = ''

        analytics_version = str(num_version) + channel
        entrypoint = 'mozilla.org-whatsnew' + analytics_version
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
            template = 'firefox/nightly_whatsnew.html'
        elif channel == 'developer':
            if show_57_dev_whatsnew(version):
                template = 'firefox/developer/whatsnew.html'
            else:
                template = 'firefox/whatsnew/index.html'
        elif channel == 'beta':
            if version.startswith('74.'):
                if locale in ['en-US', 'en-CA', 'en-GB']:
                    template = 'firefox/whatsnew/whatsnew-fx70-en.html'
                elif locale == 'de':
                    template = 'firefox/whatsnew/whatsnew-fx70-de.html'
                elif locale == 'fr':
                    template = 'firefox/whatsnew/whatsnew-fx70-fr.html'
                else:
                    template = 'firefox/whatsnew/index.html'
            else:
                template = 'firefox/whatsnew/index.html'
        elif locale == 'id':
            template = 'firefox/whatsnew/index-lite.id.html'
        elif version.startswith('77.') and lang_file_is_active('firefox/whatsnew_77', locale):
            template = 'firefox/whatsnew/whatsnew-fx77.html'
        elif version.startswith('76.') and lang_file_is_active('firefox/whatsnew_76', locale):
            template = 'firefox/whatsnew/whatsnew-fx76.html'
        elif version.startswith('75.') and lang_file_is_active('firefox/whatsnew_75', locale):
            template = 'firefox/whatsnew/whatsnew-fx75.html'
        elif version.startswith('74.'):
            # Facebook isn't used in China so zh-CN should fall back to more relevant content
            if locale != 'zh-CN' and lang_file_is_active('firefox/whatsnew_74', locale):
                template = 'firefox/whatsnew/whatsnew-fx74.html'
            elif lang_file_is_active('firefox/whatsnew_73', locale):
                template = 'firefox/whatsnew/whatsnew-fx73.html'
            else:
                template = 'firefox/whatsnew/index.html'
        elif version.startswith('73.') and lang_file_is_active('firefox/whatsnew_73', locale):
            template = 'firefox/whatsnew/whatsnew-fx73.html'
        elif version.startswith('72.') and lang_file_is_active('firefox/whatsnew_71', locale):
            template = 'firefox/whatsnew/whatsnew-fx71.html'
        elif version.startswith('71.') and lang_file_is_active('firefox/whatsnew_71', locale):
            template = 'firefox/whatsnew/whatsnew-fx71.html'
        elif version.startswith('70.'):
            if locale in ['en-US', 'en-CA', 'en-GB']:
                template = 'firefox/whatsnew/whatsnew-fx70-en.html'
            elif locale == 'de':
                template = 'firefox/whatsnew/whatsnew-fx70-de.html'
            elif locale == 'fr':
                template = 'firefox/whatsnew/whatsnew-fx70-fr.html'
            else:
                template = 'firefox/whatsnew/index.html'
        else:
            if show_default_account_whatsnew(version) and ftl_file_is_active('firefox/whatsnew/whatsnew-account'):
                template = 'firefox/whatsnew/index-account.html'
            else:
                template = 'firefox/whatsnew/index.html'

        # return a list to conform with original intention
        return [template]


class WhatsNewIndiaView(WhatsnewView):
    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)
        version = self.kwargs.get('version') or ''
        channel = detect_channel(version)

        if locale.startswith('en-') and channel not in ['nightly', 'alpha', 'beta']:
            # return a list to conform with original intention
            template = ['firefox/whatsnew/index-lite.html']
        else:
            template = super().get_template_names()

        return template


def download_thanks(request):
    locale = l10n_utils.get_locale(request)
    variant = request.GET.get('v', None)
    newsletter = request.GET.get('n', None)
    show_newsletter = locale in [
        'en-US',
        'en-GB',
        'en-CA',
        'es-ES',
        'es-AR',
        'es-CL',
        'es-MX',
        'pt-BR',
        'fr',
        'ru',
        'id',
        'de',
        'pl',
    ]

    # ensure variant matches pre-defined value
    if variant not in ['b']:  # place expected ?v= values in this list
        variant = None

    # check to see if a URL explicitly asks to hide the newsletter
    if newsletter == 'f':
        show_newsletter = False

    if lang_file_is_active('firefox/new/trailhead', locale):
        template = 'firefox/new/trailhead/thanks.html'
    else:
        template = 'firefox/new/protocol/thanks.html'

    return l10n_utils.render(request, template, {'show_newsletter': show_newsletter})


def new(request):
    # Remove legacy query parameters (Bug 1236791)
    if request.GET.get('product', None) or request.GET.get('os', None):
        return HttpResponsePermanentRedirect(reverse('firefox.new'))

    scene = request.GET.get('scene', None)

    # note: v and xv params only allow a-z, A-Z, 0-9, -, and _ characters
    experience = request.GET.get('xv', None)
    variant = request.GET.get('v', None)

    locale = l10n_utils.get_locale(request)

    # ensure variant matches pre-defined value

    if variant not in ['a', 'b']:  # place expected ?v= values in this list
        variant = None

    if scene == '2':
        # send to new permanent scene2 URL (bug 1438302)
        thanks_url = reverse('firefox.download.thanks')
        query_string = request.META.get('QUERY_STRING', '')
        if query_string:
            thanks_url = '?'.join(
                [thanks_url, force_text(query_string, errors='ignore')]
            )
        return HttpResponsePermanentRedirect(thanks_url)
    # if no/incorrect scene specified, show scene 1
    else:
        if locale == 'ru' and switch('firefox-yandex'):
            template = 'firefox/new/trailhead/download-yandex.html'
        elif lang_file_is_active('firefox/new/trailhead', locale):
            template = 'firefox/new/trailhead/download.html'
        else:
            template = 'firefox/new/protocol/download.html'

    # no harm done by passing 'v' to template, even when no experiment is running
    # (also makes tests easier to maintain by always sending a context)
    return l10n_utils.render(
        request, template, {'experience': experience, 'v': variant}
    )


def ios_testflight(request):
    # no country field, so no need to send locale
    newsletter_form = NewsletterFooterForm('ios-beta-test-flight', '')

    return l10n_utils.render(
        request, 'firefox/testflight.html', {'newsletter_form': newsletter_form}
    )


def ad_blocker(request):
    return l10n_utils.render(request, 'firefox/features/adblocker.html')


class FeaturesBookmarksView(BlogPostsView):
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['modern', 'privacy', 'featured']
    template_name = 'firefox/features/bookmarks.html'


class FeaturesFastView(BlogPostsView):
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['fastest', 'featured']
    template_name = 'firefox/features/fast.html'


class FeaturesIndependentView(BlogPostsView):
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['browser', 'featured']
    template_name = 'firefox/features/independent.html'


class FeaturesMemoryView(BlogPostsView):
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['memory', 'featured']
    template_name = 'firefox/features/memory.html'


class FeaturesPasswordManagerView(BlogPostsView):
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['modern', 'privacy', 'featured']
    template_name = 'firefox/features/password-manager.html'


class FeaturesPrivateBrowsingView(BlogPostsView):
    blog_posts_limit = 3
    blog_posts_template_variable = 'articles'
    blog_slugs = 'firefox'
    blog_tags = ['privacy', 'security', 'featured']
    template_name = 'firefox/features/private-browsing.html'


def firefox_home(request):
    locale = l10n_utils.get_locale(request)

    if lang_file_is_active('firefox/home-master', locale):
        template_name = 'firefox/home/index-master.html'
    else:
        template_name = 'firefox/home/index-quantum.html'
    return l10n_utils.render(request, template_name)


def firefox_accounts(request):
    return l10n_utils.render(request, 'firefox/accounts-2019.html')


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

    return l10n_utils.render(request, template_name, context)
