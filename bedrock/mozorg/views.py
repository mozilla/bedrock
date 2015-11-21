# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import re
from cgi import escape

from django.conf import settings
from django.contrib.staticfiles.finders import find as find_static
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import last_modified, require_safe
from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect, render as django_render

import basket
from bedrock.base.helpers import static
import requests
from lib import l10n_utils
from commonware.decorators import xframe_allow
from bedrock.base.urlresolvers import reverse
from lib.l10n_utils.dotlang import _, lang_file_is_active, lang_file_has_tag

from bedrock.mozorg import email_contribute
from bedrock.mozorg.credits import CreditsFile
from bedrock.mozorg.decorators import cache_control_expires
from bedrock.mozorg.forms import (ContributeForm, ContributeTasksForm,
                                  ContributeStudentAmbassadorForm,
                                  WebToLeadForm, ContributeSignupForm,
                                  ContentServicesForm)
from bedrock.mozorg.forums import ForumsFile
from bedrock.mozorg.models import ContributorActivity, TwitterCache
from bedrock.mozorg.util import hide_contrib_form, HttpResponseJSON
from bedrock.newsletter.forms import NewsletterFooterForm


credits_file = CreditsFile('credits')
forums_file = ForumsFile('forums')


def csrf_failure(request, reason=''):
    template_vars = {'reason': reason}
    return l10n_utils.render(request, 'mozorg/csrf-failure.html', template_vars,
                             status=403)


@xframe_allow
def hacks_newsletter(request):
    return l10n_utils.render(request,
                             'mozorg/newsletter/hacks.mozilla.org.html')


@cache_page(60 * 60 * 24 * 7)  # one week
def mozid_data_view(request, source_name):
    try:
        qs = ContributorActivity.objects.group_by_date_and_source(source_name)
    except ContributorActivity.DoesNotExist:
        # not a valid source_name
        raise Http404

    data = [{'wkcommencing': activity['date'].isoformat(),
             'totalactive': activity['total__sum'],
             'new': activity['new__sum']} for activity in qs]

    return HttpResponseJSON(data, cors=True)


class ContributeSignup(l10n_utils.LangFilesMixin, FormView):
    template_name = 'mozorg/contribute/signup.html'
    form_class = ContributeSignupForm
    category = None

    def get_context_data(self, **kwargs):
        cxt = super(ContributeSignup, self).get_context_data(**kwargs)
        cxt['category_info'] = {
            'coding': _('More about coding'),
            'testing': _('More about testing'),
            'writing': _('More about writing'),
            'teaching': _('More about teaching'),
            'helping': _('More about helping'),
            'translating': _('More about translating'),
            'activism': _('More about activism'),
            'dontknow': _('More about how you can contribute'),
        }
        return cxt

    def get_form_kwargs(self):
        kwargs = super(ContributeSignup, self).get_form_kwargs()
        kwargs['locale'] = l10n_utils.get_locale(self.request)
        return kwargs

    def get_success_url(self):
        category = self.category or 'dontknow'
        return reverse('mozorg.contribute.thankyou') + '?c=' + category

    def get_basket_data(self, form):
        data = form.cleaned_data
        self.category = data['category']
        basket_data = {
            'email': data['email'],
            'name': data['name'],
            'country': data['country'],
            'message': data['message'],
            'format': data['format'],
            'lang': form.locale,
        }
        if data.get('newsletter', False):
            basket_data['subscribe'] = 'Y'

        if 'area_' + self.category in data:
            interest_id = data['area_' + self.category]
        else:
            interest_id = self.category
        basket_data['interest_id'] = interest_id
        basket_data['source_url'] = self.request.build_absolute_uri()
        return basket_data

    def form_valid(self, form):
        try:
            basket.request('post', 'get-involved', self.get_basket_data(form))
        except basket.BasketException as e:
            if e.code == basket.errors.BASKET_INVALID_EMAIL:
                msg = _(u'Whoops! Be sure to enter a valid email address.')
                field = 'email'
            else:
                msg = _(u'We apologize, but an error occurred in our system. '
                        u'Please try again later.')
                field = '__all__'
            form.errors[field] = form.error_class([msg])
            return self.form_invalid(form)

        return super(ContributeSignup, self).form_valid(form)


class ContributeSignupOldForm(l10n_utils.LangFilesMixin, FormView):
    template_name = 'mozorg/contribute/signup.html'
    form_class = ContributeForm

    def get_context_data(self, **kwargs):
        kwargs['is_old_form'] = True
        return super(ContributeSignupOldForm, self).get_context_data(**kwargs)

    def form_valid(self, form):
        honeypot = form.cleaned_data.get('office_fax')
        if not honeypot:
            email_contribute.handle_form(self.request, form)

        return super(ContributeSignupOldForm, self).form_valid(form)

    def get_success_url(self):
        return reverse('mozorg.contribute.thankyou')


class ContributeTasks(l10n_utils.LangFilesMixin, TemplateView):
    template_name = 'mozorg/contribute/contribute-tasks.html'
    variation_re = re.compile('^[1-4]$')

    def get_context_data(self, **kwargs):
        cxt = super(ContributeTasks, self).get_context_data(**kwargs)
        variation = self.request.GET.get('variation', '4')
        if self.variation_re.match(variation):
            cxt['variation'] = variation
        return cxt


class ContributeTasksSurvey(l10n_utils.LangFilesMixin, FormView):
    template_name = 'mozorg/contribute/contribute-tasks-survey.html'
    task_re = re.compile('^[1-7]$')
    form_class = ContributeTasksForm

    def get_context_data(self, **kwargs):
        cxt = super(ContributeTasksSurvey, self).get_context_data(**kwargs)
        task = self.request.GET.get('task', '')
        if self.task_re.match(task):
            cxt['task'] = task
        return cxt

    def get_form_kwargs(self):
        kwargs = super(ContributeTasksSurvey, self).get_form_kwargs()
        kwargs['locale'] = l10n_utils.get_locale(self.request)
        return kwargs

    def get_success_url(self):
        return reverse('mozorg.contribute.tasksthankyou')

    def get_basket_data(self, form):
        data = form.cleaned_data
        return {
            'email': data['email'],
            'name': data['name'],
            'country': data['country'],
            'interest_id': 'dontknow',
            'lang': form.locale,
            'source_url': self.request.build_absolute_uri(),
        }

    def form_valid(self, form):
        try:
            basket.request('post', 'get-involved', self.get_basket_data(form))
        except basket.BasketException as e:
            if e.code == basket.errors.BASKET_INVALID_EMAIL:
                msg = _(u'Whoops! Be sure to enter a valid email address.')
                field = 'email'
            else:
                msg = _(u'We apologize, but an error occurred in our system. '
                        u'Please try again later.')
                field = '__all__'
            form.errors[field] = form.error_class([msg])
            return self.form_invalid(form)

        return super(ContributeTasksSurvey, self).form_valid(form)


class ContributeTasksThankyou(l10n_utils.LangFilesMixin, TemplateView):
    template_name = 'mozorg/contribute/contribute-tasks-thankyou.html'


class ContributeSignupThankyou(l10n_utils.LangFilesMixin, TemplateView):
    template_name = 'mozorg/contribute/thankyou.html'
    category_re = re.compile('^\w{5,20}$')

    def get_context_data(self, **kwargs):
        cxt = super(ContributeSignupThankyou, self).get_context_data(**kwargs)
        category = self.request.GET.get('c', '')
        match = self.category_re.match(category)
        if match:
            cxt['category'] = category
        return cxt


class ContributeIndex(l10n_utils.LangFilesMixin, TemplateView):
    template_name = 'mozorg/contribute/index.html'


def contribute_signup(request):
    use_new_form = lang_file_has_tag('mozorg/contribute/index',
                                     l10n_utils.get_locale(request),
                                     '2015_signup_form')
    view_class = ContributeSignup if use_new_form else ContributeSignupOldForm
    return view_class.as_view()(request)


@csrf_exempt
def contribute(request, template, return_to_form):
    newsletter_form = NewsletterFooterForm('about-mozilla', l10n_utils.get_locale(request))

    contribute_success = False

    form = ContributeForm(request.POST or None, auto_id=u'id_contribute-%s')
    if form.is_valid():
        data = form.cleaned_data.copy()

        honeypot = data.pop('office_fax')

        if not honeypot:
            contribute_success = email_contribute.handle_form(request, form)
            if contribute_success:
                # If form was submitted successfully, return a new, empty
                # one.
                form = ContributeForm()
        else:
            # send back a clean form if honeypot was filled in
            form = ContributeForm()

    return l10n_utils.render(request,
                             template,
                             {'form': form,
                              'newsletter_form': newsletter_form,
                              'contribute_success': contribute_success,
                              'return_to_form': return_to_form,
                              'hide_form': hide_contrib_form(request.locale)})


def contribute_index(request):
    if lang_file_is_active('mozorg/contribute/index',
                           l10n_utils.get_locale(request)):
        return ContributeIndex.as_view()(request)
    else:
        return contribute(request, 'mozorg/contribute/contribute-old.html', False)


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

            honeypot = data.pop('office_fax')

            if honeypot:
                msg = 'ok'
                stat = 200
            else:
                # rename custom Salesforce fields to their real GUID name
                data['00NU0000002pDJr'] = data.pop('interest')
                data['00NU00000053D4G'] = data.pop('interested_countries')
                data['00NU00000053D4L'] = data.pop('interested_languages')
                data['00NU00000053D4a'] = data.pop('campaign_type')
                data['oid'] = '00DU0000000IrgO'
                data['lead_source'] = form_kwargs.get('lead_source',
                                                      'www.mozilla.org/about/partnerships/')
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
            form_errors = {fn: [escape(msg) for msg in msgs] for fn, msgs
                           in form.errors.iteritems()}

            return HttpResponseJSON({'msg': msg, 'errors': form_errors}, status=stat)
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


def process_content_services_form(request, template, success_url_name, template_vars=None, form_kwargs=None):
    template_vars = template_vars or {}
    form_kwargs = form_kwargs or {}

    if request.method == 'POST':
        form = ContentServicesForm(data=request.POST, **form_kwargs)

        msg = 'Form invalid'
        stat = 400
        success = False

        if form.is_valid():
            data = form.cleaned_data.copy()

            honeypot = data.pop('office_fax')

            if honeypot:
                # don't let on there was a problem
                msg = 'ok'
                stat = 200
            else:
                # rename custom Salesforce fields to their real GUID name
                data['00NU00000053D4G'] = data.pop('interested_countries')
                data['00NU00000053D4L'] = data.pop('interested_languages')
                data['00NU00000053D4a'] = data.pop('campaign_type')
                data['00NU0000004ELEK'] = data.pop('mobile')
                data['oid'] = '00DU0000000IrgO'

                if data['country'] != 'us':
                    data['state'] = data.pop('province')

                data['lead_source'] = form_kwargs.get(
                    'lead_source',
                    'www.mozilla.org/about/partnerships/contentservices/')
                # As we're doing the Salesforce POST in the background here,
                # `retURL` is never visited/seen by the user. I believe it
                # is required by Salesforce though, so it should hang around
                # as a placeholder (with a valid URL, just in case).
                data['retURL'] = ('http://www.mozilla.org/en-US/'
                                  'about/partnerships/'
                                  'contentservices/start?success=1')

                r = requests.post('https://www.salesforce.com/servlet/'
                                  'servlet.WebToLead?encoding=UTF-8', data)
                msg = requests.status_codes._codes.get(r.status_code, ['error'])[0]
                stat = r.status_code

                success = True

        if request.is_ajax():
            # ensure no unescaped values sent back.
            form_errors = {fn: [escape(msg) for msg in msgs] for fn, msgs
                           in form.errors.iteritems()}
            return HttpResponseJSON({'msg': msg, 'errors': form_errors}, status=stat)
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
        form = ContentServicesForm(auto_id='%s', **form_kwargs)

        template_vars.update(csrf(request))
        template_vars['form'] = form
        template_vars['form_success'] = True if ('success' in request.GET) else False

        return l10n_utils.render(request, template, template_vars)


@csrf_protect
def content_services_start(request):
    return process_content_services_form(request,
                                         'mozorg/contentservices/start.html',
                                         'mozorg.contentservices.start')


def plugincheck(request, template='mozorg/plugincheck.html'):
    """
    Renders the plugncheck template.
    """
    return l10n_utils.render(request, template)


@xframe_allow
def contribute_studentambassadors_landing(request):
    tweets = TwitterCache.objects.get_tweets_for('mozstudents')
    return l10n_utils.render(request,
                             'mozorg/contribute/studentambassadors/landing.html',
                             {'tweets': tweets})


@csrf_protect
def contribute_studentambassadors_join(request):
    form = ContributeStudentAmbassadorForm(request.POST or None)
    if form.is_valid():
        try:
            form.save()
        except basket.BasketException:
            msg = form.error_class(
                [_('We apologize, but an error occurred in our system. '
                   'Please try again later.')])
            form.errors['__all__'] = msg
        else:
            return redirect('mozorg.contribute.studentambassadors.thanks')
    return l10n_utils.render(
        request,
        'mozorg/contribute/studentambassadors/join.html', {'form': form}
    )


def holiday_calendars(request, template='mozorg/projects/holiday-calendars.html'):
    """Generate the table of holiday calendars from JSON."""
    calendars = []
    json_file = find_static('caldata/calendars.json')
    with open(json_file) as calendar_data:
        calendars = json.load(calendar_data)

    letters = set()
    for calendar in calendars:
        letters.add(calendar['country'][:1])

    data = {
        'calendars': sorted(calendars, key=lambda k: k['country']),
        'letters': sorted(letters),
        'CALDATA_URL': static('caldata/')
    }

    return l10n_utils.render(request, template, data)


@cache_control_expires(2)
@last_modified(credits_file.last_modified_callback)
@require_safe
def credits_view(request):
    """Display the names of our contributors."""
    ctx = {'credits': credits_file}
    # not translated
    return django_render(request, 'mozorg/credits.html', ctx)


@cache_control_expires(2)
@last_modified(forums_file.last_modified_callback)
@require_safe
def forums_view(request):
    """Display our mailing lists and newsgroups."""
    ctx = {'forums': forums_file}
    return l10n_utils.render(request, 'mozorg/about/forums/forums.html', ctx)


class Robots(TemplateView):
    template_name = 'mozorg/robots.txt'
    content_type = 'text/plain'

    def get_context_data(self, **kwargs):
        hostname = self.request.get_host()
        return {'disallow_all': not hostname == 'www.mozilla.org'}


def home_tweets(locale):
    account = settings.HOMEPAGE_TWITTER_ACCOUNTS.get(locale)
    if account:
        return TwitterCache.objects.get_tweets_for(account)
    return []


def home(request):
    locale = l10n_utils.get_locale(request)
    return l10n_utils.render(
        request, 'mozorg/home/home.html', {
            'has_contribute': lang_file_is_active('mozorg/contribute'),
            'tweets': home_tweets(locale),
            'mobilizer_link': settings.MOBILIZER_LOCALE_LINK.get(
                locale, settings.MOBILIZER_LOCALE_LINK['en-US'])})
