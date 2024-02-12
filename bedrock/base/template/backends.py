# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.template import TemplateDoesNotExist
from django.template.backends.django import DjangoTemplates


class SelectiveWagtailTemplateUsage(DjangoTemplates):
    """We're using the django_jinja package, which does not appear
    to sit well alongside the standard DjangoTemplate backend.

    However, Wagtail needs that DjangoTemplate backend to be available
    in order to work.

    So, this custom backend uses Django Templating ONLY for templates
    in the wagtailadmin package, which doesn't appear to be configurable
    via exposed settings
    """

    app_dirname = "wagtail"

    def __init__(self, params):
        self.CUSTOM_ALLOWED_DIRS = params.pop("CUSTOM_ALLOWED_DIRS", [])
        super().__init__(params)

    def get_template(self, template_name):
        must_skip_backend = True

        if isinstance(template_name, str):  # some tests pass in an in-memory Jinja2 template instance, which needs to be skipped anyway
            for dirname in self.CUSTOM_ALLOWED_DIRS:
                if self.app_dirname and f"{dirname}/" in template_name:
                    must_skip_backend = False

        if must_skip_backend:
            raise TemplateDoesNotExist(f"template_name {template_name} was not in {self.app_dirname} so skipping this Engine")

        return super().get_template(template_name)
