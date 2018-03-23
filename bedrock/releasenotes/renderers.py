# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import print_function, unicode_literals

from django.core.urlresolvers import NoReverseMatch

from django_medusa.renderers import StaticSiteRenderer

from bedrock.releasenotes.models import ProductRelease


class ReleaseNotesRenderer(StaticSiteRenderer):
    def get_paths(self):
        paths = []
        for release in ProductRelease.objects.all():
            try:
                rel_path = '/en-US' + release.get_absolute_url()
            except NoReverseMatch:
                pass

            req_path = rel_path.replace('/releasenotes/', '/system-requirements/')
            paths.append(rel_path)
            paths.append(req_path)

        return paths


renderers = [ReleaseNotesRenderer]
