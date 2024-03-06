# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import django.conf.locale
from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy


class BaseAppConfig(AppConfig):
    name = "bedrock.base"
    label = "base"

    def _generate_extra_lang_info(self):
        update_dict = dict()
        for lang_code, lang_name in settings.LANGUAGES:
            if len(lang_code) > 2:
                update_dict[lang_code] = {
                    "code": lang_code,
                    "name": lang_name,
                    "name_local": lang_name,
                    "name_translated": gettext_lazy(lang_name),
                    "bidi": lang_code in settings.LANGUAGES_BIDI,
                }

        return update_dict

    def ready(self):
        # Patch Django's LANG_INFO with the three-letter countries we support
        django.conf.locale.LANG_INFO.update(**self._generate_extra_lang_info())
