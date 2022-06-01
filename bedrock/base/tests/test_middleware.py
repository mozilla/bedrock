# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test import RequestFactory, TestCase
from django.test.utils import override_settings

from bedrock.base.middleware import LocaleURLMiddleware


@override_settings(DEV=True)
class TestLocaleURLMiddleware(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.middleware = LocaleURLMiddleware()

    @override_settings(DEV_LANGUAGES=("de", "fr"))
    def test_matching_locale(self):
        locale = "fr"
        path = "/the/dude/"
        full_path = f"/{locale}{path}"
        req = self.rf.get(full_path)
        self.middleware.process_request(req)
        self.assertEqual(req.path_info, path)
        self.assertEqual(req.locale, "fr")

    @override_settings(DEV_LANGUAGES=("de", "fr"))
    def test_non_matching_locale(self):
        locale = "zh"
        path = "/the/dude/"
        full_path = f"/{locale}{path}"
        req = self.rf.get(full_path)
        self.middleware.process_request(req)
        self.assertEqual(req.path_info, full_path)
        self.assertEqual(req.locale, "")

    @override_settings(DEV_LANGUAGES=("zh-CN", "zh-TW"))
    def test_matching_main_language_to_sub_language(self):
        locale = "zh"
        path = "/the/dude/"
        full_path = f"/{locale}{path}"
        req = self.rf.get(full_path)
        self.middleware.process_request(req)
        self.assertEqual(req.path_info, path)
        self.assertEqual(req.locale, "zh-CN")

    @override_settings(DEV_LANGUAGES=("es-ES", "fr"))
    def test_matching_canonical(self):
        locale = "es"
        path = "/the/dude/"
        full_path = f"/{locale}{path}"
        req = self.rf.get(full_path)
        self.middleware.process_request(req)
        self.assertEqual(req.path_info, path)
        self.assertEqual(req.locale, "es-ES")
