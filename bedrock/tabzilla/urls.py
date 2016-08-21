# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.conf.urls import url

from pipeline.collector import default_collector
from pipeline.packager import Packager

from bedrock.base.templatetags.helpers import static
from bedrock.redirects.util import redirect

import views


def tabzilla_css_redirect(r):
    packer = Packager()
    tabzilla_package = packer.package_for('css', 'tabzilla')
    if not settings.DEBUG:
        file_path = tabzilla_package.output_filename
    else:
        default_collector.collect()
        paths = packer.compile(tabzilla_package.paths)
        file_path = paths[0]

    return static(file_path)


urlpatterns = (
    url(r'^tabzilla\.js$', views.tabzilla_js, name='tabzilla'),
    url(r'^transbar\.jsonp$', views.transbar_jsonp, name='transbar'),

    redirect(r'media/js/tabzilla\.js$', 'tabzilla', locale_prefix=False),
    redirect(r'media/css/tabzilla\.css$', tabzilla_css_redirect, locale_prefix=False),
)
