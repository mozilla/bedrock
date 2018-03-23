# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import print_function, unicode_literals

from django.core.urlresolvers import NoReverseMatch

from django_medusa.renderers import StaticSiteRenderer

from bedrock.security.models import SecurityAdvisory


KNOWN_VULNS = [
    '/en-US/security/known-vulnerabilities/firefox/',
    '/en-US/security/known-vulnerabilities/firefox-esr/',
    '/en-US/security/known-vulnerabilities/firefox-os/',
    '/en-US/security/known-vulnerabilities/thunderbird/',
    '/en-US/security/known-vulnerabilities/thunderbird-esr/',
    '/en-US/security/known-vulnerabilities/seamonkey/',
    '/en-US/security/known-vulnerabilities/firefox-3.6/',
    '/en-US/security/known-vulnerabilities/firefox-3.5/',
    '/en-US/security/known-vulnerabilities/firefox-3.0/',
    '/en-US/security/known-vulnerabilities/firefox-2.0/',
    '/en-US/security/known-vulnerabilities/firefox-1.5/',
    '/en-US/security/known-vulnerabilities/firefox-1.0/',
    '/en-US/security/known-vulnerabilities/thunderbird-3.1/',
    '/en-US/security/known-vulnerabilities/thunderbird-3.0/',
    '/en-US/security/known-vulnerabilities/thunderbird-2.0/',
    '/en-US/security/known-vulnerabilities/thunderbird-1.5/',
    '/en-US/security/known-vulnerabilities/thunderbird-1.0/',
    '/en-US/security/known-vulnerabilities/seamonkey-2.0/',
    '/en-US/security/known-vulnerabilities/seamonkey-1.1/',
    '/en-US/security/known-vulnerabilities/seamonkey-1.0/',
    '/en-US/security/known-vulnerabilities/mozilla-suite/',
]


class SecurityAdvisoriesRenderer(StaticSiteRenderer):
    def get_paths(self):
        paths = []
        for advisory in SecurityAdvisory.objects.all():
            try:
                paths.append('/en-US' + advisory.get_absolute_url())
            except NoReverseMatch:
                pass

        return paths + KNOWN_VULNS


renderers = [SecurityAdvisoriesRenderer]
