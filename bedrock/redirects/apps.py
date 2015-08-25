from django.apps import AppConfig, apps
from django.utils.module_loading import import_string

from .util import register


class RedirectsConfig(AppConfig):
    name = 'bedrock.redirects'
    label = 'redirects'

    def ready(self):
        for app in apps.get_app_configs():
            try:
                patterns = import_string(app.name + '.redirects.redirectpatterns')
            except ImportError:
                continue

            register(patterns)
