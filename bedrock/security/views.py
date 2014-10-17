# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import re

from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.http import last_modified
from django.views.generic import DetailView, ListView, RedirectView

from funfactory.urlresolvers import reverse
from product_details import product_details
from product_details.version_compare import Version

from bedrock.mozorg.decorators import cache_control_expires
from bedrock.security.models import Product, SecurityAdvisory


def product_is_obsolete(prod_name, version):
    """
    Return true if the product major version is not latest.

    :param prod_name: e.g. "firefox"
    :param version: e.g. "33.0.2"
    :return: boolean
    """
    if prod_name == 'seamonkey':
        # latest right now is 2.30. Should be good enough for a while.
        return Version(version) < Version('2.30')

    major_vers = int(version.split('.')[0])

    if prod_name == 'firefox':
        # we've got info in product-details
        latest_version = product_details.firefox_versions['LATEST_FIREFOX_VERSION']
        latest_major_vers = int(latest_version.split('.')[0])
        return major_vers < latest_major_vers

    if prod_name == 'firefox-esr':
        # we've got info in product-details
        latest_version = product_details.firefox_versions['FIREFOX_ESR']
        latest_major_vers = int(latest_version.split('.')[0])
        return major_vers < latest_major_vers

    if prod_name == 'thunderbird':
        # we've got info in product-details
        latest_version = product_details.thunderbird_versions['LATEST_THUNDERBIRD_VERSION']
        latest_major_vers = int(latest_version.split('.')[0])
        return major_vers < latest_major_vers

    # everything else is obsolete
    return True


def latest_queryset(request, kwargs):
    """
    Return a queryset for use as a way to find last-modified date.
    :param request: the http request object
    :param kwargs: the URL param args for the request
    :return: QuerySet
    """
    urlname = request.resolver_match.url_name.split('.')[1]
    if urlname == 'advisories':
        return SecurityAdvisory.objects.all()

    if urlname == 'advisory':
        pk = kwargs.get('pk')
        return SecurityAdvisory.objects.filter(pk=pk)

    if urlname == 'product-advisories':
        slug = kwargs.get('slug')
        # doesn't take minimum versions into account.
        # don't think that's really a problem as they shouldn't change.
        return SecurityAdvisory.objects.filter(fixed_in__product_slug=slug)

    if urlname == 'product-version-advisories':
        slug = u'{product}-{version}'.format(**kwargs)
        qfilter = Q(fixed_in__slug__startswith=slug + '.')
        dots = slug.count('.')
        if dots < 2:
            # add exact match if not point release
            if slug.endswith('.0'):
                # stip trailing .0 as products are stored without them
                slug = slug[:-2]
            qfilter |= Q(fixed_in__slug__exact=slug)
        return SecurityAdvisory.objects.filter(qfilter)


def latest_advisory(request, *args, **kwargs):
    """
    Callback function for use with last_modified decorator.
    :params: request, *args, **kwargs same as sent to view
    :return: function
    """
    queryset = latest_queryset(request, kwargs)
    try:
        latest = queryset.only('last_modified').latest()
    except SecurityAdvisory.DoesNotExist:
        return None

    return latest.last_modified


class AdvisoriesView(ListView):
    template_name = 'security/advisories.html'
    queryset = SecurityAdvisory.objects.only('id', 'impact', 'title', 'announced')
    context_object_name = 'advisories'

    @method_decorator(cache_control_expires(0.5))
    @method_decorator(last_modified(latest_advisory))
    def dispatch(self, request, *args, **kwargs):
        return super(AdvisoriesView, self).dispatch(request, *args, **kwargs)


class AdvisoryView(DetailView):
    model = SecurityAdvisory
    template_name = 'security/advisory.html'
    context_object_name = 'advisory'

    @method_decorator(cache_control_expires(0.5))
    @method_decorator(last_modified(latest_advisory))
    def dispatch(self, request, *args, **kwargs):
        return super(AdvisoryView, self).dispatch(request, *args, **kwargs)


class ProductView(ListView):
    template_name = 'security/product-advisories.html'
    context_object_name = 'product_versions'
    allow_empty = False
    minimum_versions = {
        'firefox': Version('4.0'),
        'thunderbird': Version('6.0'),
        'seamonkey': Version('2.3'),
    }

    @method_decorator(cache_control_expires(0.5))
    @method_decorator(last_modified(latest_advisory))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        product_slug = self.kwargs.get('slug')
        versions = Product.objects.filter(product_slug=product_slug)
        min_version = self.minimum_versions.get(product_slug)
        if min_version:
            versions = [vers for vers in versions if vers.version >= min_version]
        return sorted(versions, reverse=True)

    def get_context_data(self, **kwargs):
        cxt = super(ProductView, self).get_context_data(**kwargs)
        cxt['product_name'] = cxt['product_versions'][0].product
        return cxt


class ProductVersionView(ListView):
    template_name = 'security/product-advisories.html'
    context_object_name = 'product_versions'
    allow_empty = False

    @method_decorator(cache_control_expires(0.5))
    @method_decorator(last_modified(latest_advisory))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductVersionView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        slug = u'{product}-{version}'.format(**self.kwargs)
        qfilter = Q(slug__startswith=slug + '.')
        dots = slug.count('.')
        if dots < 2:
            # add exact match if not point release
            if slug.endswith('.0'):
                # stip trailing .0 as products are stored without them
                slug = slug[:-2]
            qfilter |= Q(slug__exact=slug)
        versions = Product.objects.filter(qfilter)
        return sorted(versions, reverse=True)

    def get_context_data(self, **kwargs):
        cxt = super(ProductVersionView, self).get_context_data(**kwargs)
        prod_name, version = self.kwargs['product'], self.kwargs['version']
        cxt['is_obsolete'] = product_is_obsolete(prod_name, version)
        cxt['product_name'] = '{0} {1}'.format(cxt['product_versions'][0].product, version)
        cxt['product_slug'] = prod_name
        return cxt


class CachedRedirectView(RedirectView):
    @method_decorator(cache_control_expires(24 * 30))  # 30 days
    def dispatch(self, request, *args, **kwargs):
        return super(CachedRedirectView, self).dispatch(request, *args, **kwargs)


class OldAdvisoriesView(CachedRedirectView):
    def get_redirect_url(self, **kwargs):
        return reverse('security.advisory', kwargs=kwargs)


class OldAdvisoriesListView(CachedRedirectView):
    def get_redirect_url(self, **kwargs):
        return reverse('security.advisories')


class KVRedirectsView(CachedRedirectView):
    prod_ver_re = re.compile('(\w+)(\d{2})$')

    def get_redirect_url(self, *args, **kwargs):
        url_component = kwargs['filename']
        if url_component == 'suite17':
            return reverse('security.product-advisories', kwargs={'slug': 'mozilla-suite'})

        match = self.prod_ver_re.match(url_component)
        if match:
            product, version = match.groups()
            version = '{0}.{1}'.format(*version)
            return reverse('security.product-version-advisories', kwargs={'product': product,
                                                                          'version': version})

        if url_component.endswith('ESR'):
            return reverse('security.product-advisories',
                           kwargs={'slug': url_component[:-3] + '-esr'})

        return reverse('security.product-advisories', kwargs={'slug': url_component})
