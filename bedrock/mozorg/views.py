# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django.conf import settings
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic.base import TemplateView
from django.shortcuts import redirect

import basket
import requests
from lib import l10n_utils
from commonware.decorators import xframe_allow
from funfactory.urlresolvers import reverse
from lib.l10n_utils.dotlang import _, lang_file_is_active

from bedrock.firefox import version_re
from bedrock.firefox.utils import is_current_or_newer
from bedrock.mozorg import email_contribute
from bedrock.mozorg.forms import (ContributeForm,
                                  ContributeUniversityAmbassadorForm,
                                  WebToLeadForm)
from bedrock.mozorg.util import hide_contrib_form
from bedrock.mozorg.util import HttpResponseJSON
from bedrock.newsletter.forms import NewsletterFooterForm


def csrf_failure(request, reason=''):
    template_vars = {'reason': reason}
    return l10n_utils.render(request, 'mozorg/csrf-failure.html', template_vars,
                             status=403)


@xframe_allow
def hacks_newsletter(request):
    return l10n_utils.render(request,
                             'mozorg/newsletter/hacks.mozilla.org.html')


@csrf_exempt
def contribute(request, template, return_to_form):
    newsletter_id = 'about-mozilla'
    has_contribute_form = (request.method == 'POST' and
                           'contribute-form' in request.POST)

    has_newsletter_form = (request.method == 'POST' and
                           'newsletter-form' in request.POST)

    locale = getattr(request, 'locale', 'en-US')

    contribute_success = False
    newsletter_success = False

    # This is ugly, but we need to handle two forms. I would love if
    # these forms could post to separate pages and get redirected
    # back, but we're forced to keep the error/success workflow on the
    # same page. Please change this.
    if has_contribute_form:
        form = ContributeForm(request.POST)
        contribute_success = email_contribute.handle_form(request, form)
        if contribute_success:
            # If form was submitted successfully, return a new, empty
            # one.
            form = ContributeForm()
    else:
        form = ContributeForm()

    if has_newsletter_form:
        newsletter_form = NewsletterFooterForm(newsletter_id, locale,
                                               request.POST,
                                               prefix='newsletter')
        if newsletter_form.is_valid():
            data = newsletter_form.cleaned_data

            try:
                basket.subscribe(data['email'],
                                 newsletter_id,
                                 format=data['fmt'],
                                 country=data['country'])
                newsletter_success = True
            except basket.BasketException:
                msg = newsletter_form.error_class(
                    [_('We apologize, but an error occurred in our system. '
                       'Please try again later.')]
                )
                newsletter_form.errors['__all__'] = msg
    else:
        newsletter_form = NewsletterFooterForm(newsletter_id, locale, prefix='newsletter')

    return l10n_utils.render(request,
                             template,
                             {'form': form,
                              'contribute_success': contribute_success,
                              'newsletter_form': newsletter_form,
                              'newsletter_success': newsletter_success,
                              'return_to_form': return_to_form,
                              'hide_form': hide_contrib_form(request.locale),
                              'has_moz15': locale in settings.LOCALES_WITH_MOZ15})


@xframe_allow
@csrf_exempt
def contribute_embed(request, template, return_to_form):
    """The same as contribute but allows frame embedding."""
    return contribute(request, template, return_to_form)


def process_partnership_form(request, template, success_url_name, template_vars=None, form_kwargs=None):
    template_vars = template_vars or {}
    form_kwargs = form_kwargs or {}

    if request.method == 'POST':
        form = WebToLeadForm(data=request.POST, **form_kwargs)

        msg = 'Form invalid'
        stat = 400
        success = False

        if form.is_valid():
            data = form.cleaned_data.copy()

            honeypot = data.pop('superpriority')

            if honeypot:
                msg = 'Visitor invalid'
                stat = 400
            else:
                interest = data.pop('interest')
                data['00NU0000002pDJr'] = interest
                data['oid'] = '00DU0000000IrgO'
                # As we're doing the Salesforce POST in the background here,
                # `retURL` is never visited/seen by the user. I believe it
                # is required by Salesforce though, so it should hang around
                # as a placeholder (with a valid URL, just in case).
                data['retURL'] = ('http://www.mozilla.org/en-US/about/'
                                  'partnerships?success=1')

                r = requests.post('https://www.salesforce.com/servlet/'
                                  'servlet.WebToLead?encoding=UTF-8', data)
                msg = requests.status_codes._codes.get(r.status_code, ['error'])[0]
                stat = r.status_code

                success = True

        if request.is_ajax():
            return HttpResponseJSON({'msg': msg, 'errors': form.errors}, status=stat)
        # non-AJAX POST
        else:
            # if form is not valid, render template to retain form data/error messages
            if not success:
                template_vars.update(csrf(request))
                template_vars['form'] = form
                template_vars['form_success'] = success

                return l10n_utils.render(request, template, template_vars)
            # if form is valid, redirect to avoid refresh double post possibility
            else:
                return HttpResponseRedirect("%s?success" % (reverse(success_url_name)))
    # no form POST - build form, add CSRF, & render template
    else:
        # without auto_id set, all id's get prefixed with 'id_'
        form = WebToLeadForm(auto_id='%s', **form_kwargs)

        template_vars.update(csrf(request))
        template_vars['form'] = form
        template_vars['form_success'] = True if ('success' in request.GET) else False

        return l10n_utils.render(request, template, template_vars)


@csrf_protect
def partnerships(request):
    return process_partnership_form(request, 'mozorg/partnerships.html', 'mozorg.partnerships')


def plugincheck(request, template='mozorg/plugincheck.html'):
    """
    Determine whether the current UA is the latest Firefox,
    passes the result to the template and renders the
    specified template.
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    user_version = "0"
    ua_regexp = r"Firefox/(%s)" % version_re
    match = re.search(ua_regexp, user_agent)
    if match:
        user_version = match.group(1)

    data = {
        'is_latest': is_current_or_newer(user_version)
    }

    return l10n_utils.render(request, template, data)


@csrf_exempt
def contribute_university_ambassadors(request):
    form = ContributeUniversityAmbassadorForm(request.POST or None)
    if form.is_valid():
        try:
            form.save()
        except basket.BasketException:
            msg = form.error_class(
                [_('We apologize, but an error occurred in our system. '
                   'Please try again later.')])
            form.errors['__all__'] = msg
        else:
            return redirect('mozorg.contribute_university_ambassadors_thanks')
    return l10n_utils.render(
        request,
        'mozorg/contribute_university_ambassadors.html', {'form': form}
    )


class Robots(TemplateView):
    template_name = 'mozorg/robots.txt'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'text/plain'
        return super(Robots, self).render_to_response(
            context, **response_kwargs)

    def get_context_data(self, **kwargs):
        SITE_URL = getattr(settings, 'SITE_URL', '')
        return {'disallow_all': not SITE_URL.endswith('://www.mozilla.org')}


class HomeTestView(TemplateView):
    """Home page view that will use a different template for a QS."""
    template_name = 'mozorg/home.html'

    def post(self, request, *args, **kwargs):
        # required for newsletter form post that is handled in newsletter/helpers.py
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(HomeTestView, self).get_context_data(**kwargs)
        ctx['has_contribute'] = lang_file_is_active('mozorg/contribute')
        locale = l10n_utils.get_locale(self.request)
        locale = locale if locale in settings.MOBILIZER_LOCALE_LINK else 'en-US'
        ctx['mobilizer_link'] = settings.MOBILIZER_LOCALE_LINK[locale]

        ctx['show_search'] = self.request.GET.get('s', 0)

        return ctx

    def render_to_response(self, context, **response_kwargs):
        return l10n_utils.render(self.request,
                                 self.get_template_names(),
                                 context,
                                 **response_kwargs)
