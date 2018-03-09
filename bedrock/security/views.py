# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import re

from django.core.urlresolvers import NoReverseMatch
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, RedirectView

from bedrock.base.urlresolvers import reverse
from product_details import product_details
from product_details.version_compare import Version
from lib.l10n_utils import LangFilesMixin

from bedrock.mozorg.decorators import cache_control_expires
from bedrock.security.models import HallOfFamer, Product, SecurityAdvisory


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


class HallOfFameView(LangFilesMixin, ListView):
    template_names = {
        'client': 'security/bug-bounty/hall-of-fame.html',
        'web': 'security/bug-bounty/web-hall-of-fame.html',
    }
    context_object_name = 'hofers'
    allow_empty = False
    program = None

    def get_template_names(self):
        return [self.template_names[self.program]]

    def get_queryset(self):
        return HallOfFamer.objects.filter(program=self.program)


class AdvisoriesView(LangFilesMixin, ListView):
    template_name = 'security/advisories.html'
    queryset = SecurityAdvisory.objects.only('id', 'impact', 'title', 'announced')
    context_object_name = 'advisories'


class AdvisoryView(LangFilesMixin, DetailView):
    model = SecurityAdvisory
    template_name = 'security/advisory.html'
    context_object_name = 'advisory'


class ProductView(LangFilesMixin, ListView):
    template_name = 'security/product-advisories.html'
    context_object_name = 'product_versions'
    allow_empty = False
    minimum_versions = {
        'firefox': Version('4.0'),
        'thunderbird': Version('6.0'),
        'seamonkey': Version('2.3'),
    }

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


class ProductVersionView(LangFilesMixin, ListView):
    template_name = 'security/product-advisories.html'
    context_object_name = 'product_versions'
    allow_empty = False

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
    permanent = True

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
        url_component = kwargs['filename'].replace(' ', '')
        try:
            return reverse(**self.get_redirect_args(url_component))
        except NoReverseMatch:
            return None

    def get_redirect_args(self, url_component):
        if url_component == 'suite17':
            return dict(viewname='security.product-advisories',
                        kwargs={'slug': 'mozilla-suite'})

        match = self.prod_ver_re.match(url_component)
        if match:
            product, version = match.groups()
            version = '{0}.{1}'.format(*version)
            return dict(viewname='security.product-version-advisories',
                        kwargs={'product': product, 'version': version})

        if url_component.endswith('ESR'):
            return dict(viewname='security.product-advisories',
                        kwargs={'slug': url_component[:-3] + '-esr'})

        return dict(viewname='security.product-advisories', kwargs={'slug': url_component})
