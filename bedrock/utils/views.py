from builtins import object
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from bedrock.utils import expand_locale_groups
from lib.l10n_utils import LangFilesMixin, get_locale


class VariationMixin(object):
    template_name_variations = None
    template_context_variations = None
    variation_locales = None

    @cached_property
    def _all_variation_locales(self):
        return expand_locale_groups(self.variation_locales)

    def _locale_allowed(self):
        if self.variation_locales is None:
            return True

        return get_locale(self.request) in self._all_variation_locales

    def get_template_names(self):
        names = super(VariationMixin, self).get_template_names()
        if self.template_name_variations and self._locale_allowed():
            variation = self.request.GET.get('v')
            if variation in self.template_name_variations:
                name, ext = self.template_name.rsplit('.', 1)
                names = ['{0}-{1}.{2}'.format(name, variation, ext)]

        return names

    def get_context_data(self, **kwargs):
        cxt = super(VariationMixin, self).get_context_data(**kwargs)
        if self.template_context_variations:
            # do this outside of locale check so that template always has
            # the 'variation' variable if a variation is set
            cxt['variation'] = ''
            if self._locale_allowed():
                variation = self.request.GET.get('v')
                if variation in self.template_context_variations:
                    cxt['variation'] = variation

        return cxt


class VariationTemplateView(VariationMixin, LangFilesMixin, TemplateView):
    pass
