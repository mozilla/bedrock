from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from ... import clients


class Command(BaseCommand):
    # TODO: args, help, docstrings

    def rna_client(self, legacy_api=False):
        if legacy_api:
            return clients.LegacyRNAModelClient()
        else:
            return clients.RNAModelClient()

    def model_params(self, models, legacy_api=False):
        params = dict((m, {}) for m in models)
        if not legacy_api:
            for m in models:
                try:
                    latest = m.objects.latest('modified')
                except ObjectDoesNotExist:
                    pass
                else:
                    params[m]['modified_after'] = latest.modified.isoformat()
        return params

    def handle(self, *args, **options):
        legacy_api = settings.RNA.get('LEGACY_API', False)
        rc = self.rna_client(legacy_api)
        model_params = self.model_params(rc.model_map.values(), legacy_api)
        for url_name, model_class in rc.model_map.items():
            params = model_params[model_class]
            rc.model_client(url_name).model(save=True, params=params)
