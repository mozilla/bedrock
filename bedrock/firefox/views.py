# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django.http import (Http404, HttpResponseRedirect,
                         HttpResponsePermanentRedirect)
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView

import basket
from bedrock.base.urlresolvers import reverse
from commonware.response.decorators import xframe_allow
from lib import l10n_utils
from product_details.version_compare import Version

from bedrock.firefox.firefox_details import firefox_desktop, firefox_android
from bedrock.firefox.forms import SendToDeviceWidgetForm
from bedrock.mozorg.util import HttpResponseJSON
from bedrock.newsletter.forms import NewsletterFooterForm
from bedrock.releasenotes import version_re


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
            'all': 'download-firefox-mobile',
        }
    }
}


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


def fx_home_redirect(request):
    return HttpResponseRedirect(reverse('firefox.new'))


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
    if platform == 'android' and channel in ['alpha', 'nightly', 'esr']:
        raise Http404

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


def show_40_firstrun(version):
    try:
        version = Version(version)
    except ValueError:
        return False

    return version >= Version('40.0')


class LatestFxView(TemplateView):

    """
    Base class to be extended by views that require visitor to be
    using latest version of Firefox. Classes extending this class must
    implement either `get_template_names` function or provide
    `template_name` class attribute. Control where to redirect non
    Firefox users by setting the `non_fx_redirect` attribute to
    a url name.
    """
    non_fx_redirect = 'firefox.new'

    @cache_control(max_age=0)
    def dispatch(self, *args, **kwargs):
        return super(LatestFxView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # required for newsletter form post that is handled in
        # newsletter/templatetags/helpers.py
        return self.get(request, *args, **kwargs)

    def redirect_to(self):
        """
        Redirect visitors based on their user-agent.

        - Up-to-date Firefox users pass through.
        - Other Firefox users go to the new page.
        - Non Firefox users go to the configured page.
        """
        query = self.request.META.get('QUERY_STRING')
        query = '?' + query if query else ''

        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        if 'Firefox' not in user_agent:
            return reverse(self.non_fx_redirect) + query
            # TODO : Where to redirect bug 757206

        return None

    def render_to_response(self, context, **response_kwargs):
        redirect_url = self.redirect_to()

        if redirect_url is not None:
            return HttpResponsePermanentRedirect(redirect_url)
        else:
            return l10n_utils.render(self.request,
                                     self.get_template_names(),
                                     context,
                                     **response_kwargs)


class FirstrunView(LatestFxView):

    def get_context_data(self, **kwargs):
        ctx = super(FirstrunView, self).get_context_data(**kwargs)

        # add version to context for use in templates
        ctx['version'] = self.kwargs.get('version') or ''

        return ctx

    def get_template_names(self):
        funnelcake = self.request.GET.get('f', '')
        locale = l10n_utils.get_locale(self.request)
        version = self.kwargs.get('version') or ''

        if detect_channel(version) == 'alpha':
            template = 'firefox/dev-firstrun.html'
        elif show_40_firstrun(version):
            if locale == 'en-US' and funnelcake == '90':
                # ravioli/katie couric promo
                template = 'firefox/firstrun/ravioli.html'
            else:
                template = 'firefox/firstrun/firstrun-horizon.html'
        elif show_38_0_5_firstrun(version):
            template = 'firefox/australis/fx38_0_5/firstrun.html'
        else:
            template = 'firefox/australis/firstrun.html'

        # return a list to conform with original intention
        return [template]


class FirstrunLearnMoreView(LatestFxView):

    def get_context_data(self, **kwargs):
        ctx = super(FirstrunLearnMoreView, self).get_context_data(**kwargs)

        # add funnelcake version to context for use in templates
        ctx['f'] = self.request.GET.get('f', '')

        return ctx

    def get_template_names(self):
        locale = l10n_utils.get_locale(self.request)
        funnelcake = self.request.GET.get('f', '')

        if locale == 'en-US' and funnelcake in ['64', '65']:
            template = 'firefox/firstrun/learnmore/yahoo-search.html'
        else:
            template = 'firefox/firstrun/learnmore/learnmore.html'

        return [template]


class WhatsnewView(LatestFxView):

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
        # zh-TW on 49.0 gets a special template
        elif locale == 'zh-TW' and show_49_0_whatsnew(version):
            template = 'firefox/whatsnew-zh-TW-49.html'
        elif show_42_whatsnew(version):
            template = 'firefox/whatsnew_42/whatsnew.html'
        else:
            template = 'firefox/australis/whatsnew.html'

        # return a list to conform with original intention
        return [template]


class FeedbackView(TemplateView):

    donate_url = ('https://donate.mozilla.org/'
       '?ref=EOYFR2015&utm_campaign=EOYFR2015'
       '&utm_source=Heartbeat_survey&utm_medium=referral'
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


class Win10Welcome(l10n_utils.LangFilesMixin, TemplateView):

    def get_template_names(self):
        # check for variant in querystring for multi-variant testing.
        v = self.request.GET.get('v', '')
        template = 'firefox/win10-welcome.html'

        # ensure variant is one of 4 accepted values and locale is en-US only.
        # now on round 3 of testing, hence "-3" in template name
        if (v in map(str, range(1, 11)) and self.request.locale == 'en-US'):
            template = 'firefox/win10_variants/variant-3-' + v + '.html'

        return [template]


class TrackingProtectionTourView(l10n_utils.LangFilesMixin, TemplateView):
    template_name = 'firefox/tracking-protection-tour.html'


@xframe_allow
def new(request):
    # Remove legacy query parameters (Bug 1236791)
    if request.GET.get('product', None) or request.GET.get('os', None):
        return HttpResponsePermanentRedirect(reverse('firefox.new'))

    scene = request.GET.get('scene', None)

    if scene == '2':
        template = 'firefox/new/scene2.html'
    # if no/incorrect scene specified, show scene 1
    else:
        template = 'firefox/new/scene1.html'

        # en-US tests
        locale = l10n_utils.get_locale(request)
        version = request.GET.get('v', None)

        # note version 'a' is omitted here as it's a double control group
        if locale == 'en-US' and version in ['b', 'c']:
            template = 'firefox/new/variant/scene1-v{0}.html'.format(version)

    return l10n_utils.render(request, template)


def sync(request):
    locale = l10n_utils.get_locale(request)
    version = request.GET.get('v', None)

    if (locale != 'en-US' or version not in ['2', '3']):
        version = None

    return l10n_utils.render(request, 'firefox/sync.html', {'version': version})


def ios_testflight(request):
    # no country field, so no need to send locale
    newsletter_form = NewsletterFooterForm('ios-beta-test-flight', '')

    return l10n_utils.render(request,
                             'firefox/testflight.html',
                             {'newsletter_form': newsletter_form})
