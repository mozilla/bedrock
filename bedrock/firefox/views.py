# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import hashlib
import hmac
import re
from collections import OrderedDict
from urlparse import urlparse

from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect
from django.utils.cache import patch_response_headers
from django.utils.encoding import force_text
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.views.generic.base import TemplateView

import basket
import querystringsafe_base64
from product_details.version_compare import Version

from lib import l10n_utils
from lib.l10n_utils.dotlang import lang_file_is_active
from bedrock.base.urlresolvers import reverse
from bedrock.base.waffle import switch
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
SEND_TO_DEVICE_MESSAGE_SETS = settings.SEND_TO_DEVICE_MESSAGE_SETS

STUB_VALUE_NAMES = [
    # name, default value
    ('utm_source', '(not set)'),
    ('utm_medium', '(direct)'),
    ('utm_campaign', '(not set)'),
    ('utm_content', '(not set)'),
]
STUB_VALUE_RE = re.compile(r'^[a-z0-9-.%():_]+$', flags=re.IGNORECASE)


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
    if not settings.STUB_ATTRIBUTION_RATE:
        # return as though it was rate limited, since it was
        response = HttpResponseJSON({'error': 'rate limited'}, status=429)
    elif not settings.STUB_ATTRIBUTION_HMAC_KEY:
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
        response = HttpResponseJSON(code_data)
    else:
        response = HttpResponseJSON({'error': 'Invalid code'}, status=400)

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

    code = querystringsafe_base64.encode(code)
    sig = hmac.new(key, code, hashlib.sha256).hexdigest()
    return {
        'attribution_code': code,
        'attribution_sig': sig,
    }


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
                        return HttpResponseJSON({'success': False, 'errors': ['number']})
                    else:
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
        'platforms': product.platforms(channel, True),
        'platform_cls': product.platform_classification,
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


def show_57_dev_whatsnew(version):
    version = version[:-2]
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('57.0')


def show_57_whatsnew(version, oldversion):
    try:
        version = Version(version)
        if oldversion:
            oldversion = Version(oldversion)
    except ValueError:
        return False

    v57 = Version('57.0')
    v58 = Version('58.0')

    if oldversion:
        return version >= v57 and version < v58 and oldversion < v57
    else:
        return version == v57


def show_59_whatsnew(version, oldversion):
    try:
        version = Version(version)
        if oldversion:
            oldversion = Version(oldversion)
    except ValueError:
        return False

    v59 = Version('59.0')
    v60 = Version('60.0')

    if oldversion:
        return version >= v59 and version < v60 and oldversion < v59
    else:
        return version >= v59 and version < v60


def show_60_whatsnew(version, oldversion):
    try:
        version = Version(version)
        if oldversion:
            oldversion = Version(oldversion)
    except ValueError:
        return False

    v60 = Version('60.0')

    return version >= v60 and (oldversion < v60 if oldversion else True)


def show_61_whatsnew(version, oldversion):
    try:
        version = Version(version)
        if oldversion:
            oldversion = Version(oldversion)
    except ValueError:
        return False

    v61 = Version('61.0')

    return version >= v61 and (oldversion < v61 if oldversion else True)


def show_62_whatsnew(version, oldversion):
    try:
        version = Version(version)
        if oldversion:
            oldversion = Version(oldversion)
    except ValueError:
        return False

    v62 = Version('62.0')

    return version >= v62 and (oldversion < v62 if oldversion else True)


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


def redirect_old_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version < Version('40.0')


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
        experience = self.request.GET.get('xv', None)
        locale = l10n_utils.get_locale(self.request)

        # for copy test
        # https://bugzilla.mozilla.org/show_bug.cgi?id=1451051
        variation = self.request.GET.get('v', None)

        if detect_channel(version) == 'alpha':
            if show_57_dev_firstrun(version):
                template = 'firefox/developer/firstrun.html'
            else:
                template = 'firefox/dev-firstrun.html'
        elif show_62_firstrun(version):
            if locale == 'en-US' and experience == 'firefox-election':
                template = 'firefox/firstrun/firstrun-election.html'
            else:
                template = 'firefox/firstrun/firstrun-quantum.html'
        elif show_57_firstrun(version):
            if locale == 'en-US' and variation in ['a', 'b', 'c', 'd']:
                template = 'firefox/firstrun/firstrun-quantum-{}.html'.format(variation)
            else:
                template = 'firefox/firstrun/firstrun-quantum.html'
        else:
            template = 'firefox/firstrun/index.html'

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
            if show_57_dev_whatsnew(version):
                template = 'firefox/developer/whatsnew.html'
            else:
                template = 'firefox/dev-whatsnew.html'
        elif channel == 'nightly':
            template = 'firefox/nightly_whatsnew.html'
        elif locale == 'id':
            if switch('firefox_lite_whatsnew'):
                template = 'firefox/whatsnew/index-lite.id.html'
            else:
                template = 'firefox/whatsnew/index.id.html'
        elif locale == 'zh-TW':
            template = 'firefox/whatsnew/index.zh-TW.html'
        elif version.startswith('63.'):
            template = 'firefox/whatsnew/whatsnew-fx63.html'
        elif show_62_whatsnew(version, oldversion):
            template = 'firefox/whatsnew/whatsnew-fx62.html'
        elif show_61_whatsnew(version, oldversion):
            template = 'firefox/whatsnew/whatsnew-fx61.html'
        elif show_60_whatsnew(version, oldversion):
            template = 'firefox/whatsnew/whatsnew-fx60.html'
        elif show_59_whatsnew(version, oldversion):
            template = 'firefox/whatsnew/whatsnew-fxa.html'
        elif show_57_whatsnew(version, oldversion):
            # locale-specific templates don't seem to work for the default locale
            if locale == 'en-US':
                template = 'firefox/whatsnew/fx57/whatsnew-57.en-US.html'
            # locale-specific templates for de, en-GB, es-AR, es-CL, es-ES, es-MX,
            # fr, id, pl, pt-BR, ru, zh-CN, and zh-TW
            else:
                template = 'firefox/whatsnew/fx57/whatsnew-57.html'
        else:
            template = 'firefox/whatsnew/index.html'

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

    def get_template_names(self):
        variation = self.request.GET.get('variation', None)

        if variation in ['0', '1', '2']:
            template = 'firefox/tracking-protection-tour/variation-{}.html'.format(variation)
        else:
            template = 'firefox/tracking-protection-tour/index.html'

        return [template]


def download_thanks(request):
    experience = request.GET.get('xv', None)
    locale = l10n_utils.get_locale(request)
    variant = request.GET.get('v', None)
    show_newsletter = locale in ['en-US', 'en-GB', 'en-CA', 'en-ZA', 'es-ES', 'es-AR', 'es-CL', 'es-MX', 'pt-BR', 'fr', 'ru', 'id', 'de', 'pl']

    # ensure variant matches pre-defined value
    if variant not in ['x', 'y']:  # place expected ?v= values in this list
        variant = None

    if variant == 'x' and locale == 'en-US':
        show_newsletter = False  # Prevent showing the newsletter for FxA account experiment mozilla/bedrock#5974

    # `wait-face`, `reggiewatts` variations are currently localized for both en-US and de locales.
    if lang_file_is_active('firefox/new/wait-face', locale) and experience == 'waitface':
        template = 'firefox/new/wait-face/scene2.html'
    elif lang_file_is_active('firefox/new/reggiewatts', locale) and experience == 'reggiewatts':
        template = 'firefox/new/reggie-watts/scene2.html'
    elif locale == 'de':
        if experience == 'berlin':
            template = 'firefox/new/berlin/scene2.html'
        elif experience == 'aus-gruenden':
            template = 'firefox/new/berlin/scene2-aus-gruenden.html'
        elif experience == 'herz':
            template = 'firefox/new/berlin/scene2-herz.html'
        elif experience == 'geschwindigkeit':
            template = 'firefox/new/berlin/scene2-gesch.html'
        elif experience == 'privatsphare':
            template = 'firefox/new/berlin/scene2-privat.html'
        elif experience == 'auf-deiner-seite':
            template = 'firefox/new/berlin/scene2-auf-deiner-seite.html'
        else:
            template = 'firefox/new/scene2.html'
    elif locale == 'en-US':
        if experience in ['portland', 'forgood']:
            template = 'firefox/new/portland/scene2.html'
        elif experience in ['portland-fast', 'fast']:
            template = 'firefox/new/portland/scene2-fast.html'
        elif experience in ['portland-safe', 'safe']:
            template = 'firefox/new/portland/scene2-safe.html'
        elif experience == 'betterbrowser':
            template = 'firefox/new/better-browser/scene2.html'
        else:
            template = 'firefox/new/scene2.html'
    else:
        template = 'firefox/new/scene2.html'

    return l10n_utils.render(request, template, {'show_newsletter': show_newsletter})


def new(request):
    # Remove legacy query parameters (Bug 1236791)
    if request.GET.get('product', None) or request.GET.get('os', None):
        return HttpResponsePermanentRedirect(reverse('firefox.new'))

    scene = request.GET.get('scene', None)
    experience = request.GET.get('xv', None)
    variant = request.GET.get('v', None)
    locale = l10n_utils.get_locale(request)

    # ensure variant matches pre-defined value
    if variant not in ['a', '1', '2', 'x', 'y']:  # place expected ?v= values in this list
        variant = None

    if scene == '2':
        # send to new permanent scene2 URL (bug 1438302)
        thanks_url = reverse('firefox.download.thanks')
        query_string = request.META.get('QUERY_STRING', '')
        if query_string:
            thanks_url = '?'.join([thanks_url, force_text(query_string, errors='ignore')])
        return HttpResponsePermanentRedirect(thanks_url)
    # if no/incorrect scene specified, show scene 1
    else:
        if lang_file_is_active('firefox/new/wait-face', locale) and experience == 'waitface':
            template = 'firefox/new/wait-face/scene1.html'
        elif lang_file_is_active('firefox/new/reggiewatts', locale) and experience == 'reggiewatts':
            template = 'firefox/new/reggie-watts/scene1.html'
        elif locale == 'de':
            if experience == 'berlin':
                template = 'firefox/new/berlin/scene1.html'
            elif experience == 'aus-gruenden':
                template = 'firefox/new/berlin/scene1-aus-gruenden.html'
            elif experience == 'herz':
                template = 'firefox/new/berlin/scene1-herz.html'
            elif experience == 'geschwindigkeit':
                template = 'firefox/new/berlin/scene1-gesch.html'
            elif experience == 'privatsphare':
                template = 'firefox/new/berlin/scene1-privat.html'
            elif experience == 'auf-deiner-seite':
                template = 'firefox/new/berlin/scene1-auf-deiner-seite.html'
            else:
                template = 'firefox/new/scene1.html'
        elif switch('firefox-yandex') and locale == 'ru':
            template = 'firefox/new/yandex/scene1.html'
        elif locale == 'en-US':
            if variant == 'x':
                template = 'firefox/new/fx/scene1.html'
            elif experience in ['portland', 'forgood']:
                template = 'firefox/new/portland/scene1.html'
            elif experience in ['portland-fast', 'fast']:
                template = 'firefox/new/portland/scene1-fast.html'
            elif experience in ['portland-safe', 'safe']:
                template = 'firefox/new/portland/scene1-safe.html'
            elif experience == 'betterbrowser':
                template = 'firefox/new/better-browser/scene1.html'
            elif experience == 'safari':
                if variant == 'a':
                    template = 'firefox/new/scene1.html'
                elif variant == '2':
                    template = 'firefox/new/compare/scene1-safari-2.html'
                else:
                    template = 'firefox/new/compare/scene1-safari-1.html'
            elif experience == 'chrome':
                if variant == 'a':
                    template = 'firefox/new/scene1.html'
                elif variant == '2':
                    template = 'firefox/new/compare/scene1-chrome-2.html'
                else:
                    template = 'firefox/new/compare/scene1-chrome-1.html'
            elif experience == 'edge':
                if variant == 'a':
                    template = 'firefox/new/scene1.html'
                elif variant == '2':
                    template = 'firefox/new/compare/scene1-edge-2.html'
                else:
                    template = 'firefox/new/compare/scene1-edge-1.html'
            elif experience == 'opera':
                if variant == 'a':
                    template = 'firefox/new/scene1.html'
                elif variant == '2':
                    template = 'firefox/new/compare/scene1-opera-2.html'
                else:
                    template = 'firefox/new/compare/scene1-opera-1.html'
            else:
                template = 'firefox/new/scene1.html'
        else:
            template = 'firefox/new/scene1.html'

    # no harm done by passing 'v' to template, even when no experiment is running
    # (also makes tests easier to maintain by always sending a context)
    return l10n_utils.render(request, template, {'experience': experience, 'v': variant})


def ios_testflight(request):
    # no country field, so no need to send locale
    newsletter_form = NewsletterFooterForm('ios-beta-test-flight', '')

    return l10n_utils.render(request,
                             'firefox/testflight.html',
                             {'newsletter_form': newsletter_form})


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
    return l10n_utils.render(request, 'firefox/home.html')
