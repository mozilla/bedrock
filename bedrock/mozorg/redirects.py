# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.redirects.util import gone, redirect, ua_redirector


def to_uppercase(url):
    def decider(request, **kwargs):
        kwargs = {k: v.upper() for k, v in kwargs.items() if k != "locale"}
        return url.format(**kwargs)

    return decider


redirectpatterns = (
    # bug 874913, 681572
    redirect(r"^(products/)?download\.html", "firefox.new", query=""),
    # bug 845580
    redirect(r"^home/?$", "firefox.new"),
    # bug 948605
    redirect(r"^firefox/xp", "firefox.new"),
    # bug 875052
    redirect(r"^start/", ua_redirector("seamonkey", "http://www.seamonkey-project.org/start/", "firefox.new"), cache_timeout=0),
    # bug 856081 redirect /about/drivers https://wiki.mozilla.org/Firefox/Drivers
    redirect(r"^about/drivers(\.html|/)?$", "https://wiki.mozilla.org/Firefox/Drivers"),
    # community
    # bug 885797
    redirect(r"^community/(directory|wikis|blogs|websites)\.html$", "https://wiki.mozilla.org/Websites/Directory", locale_prefix=False),
    # bug 885856
    redirect(r"^projects/index\.(de|fr|hr|sq)\.html$", "/{}/firefox/", locale_prefix=False),
    # bug 856075
    redirect(
        r"^projects/technologies\.html$", "https://developer.mozilla.org/docs/Mozilla/Using_Mozilla_code_in_other_projects", locale_prefix=False
    ),
    # bug 787269
    redirect(
        r"^projects/security/components/signed-script(?:s|-example)\.html$",
        "https://developer.mozilla.org/docs/Bypassing_Security_Restrictions_and_Signing_Code",
    ),
    # bug 874526, 877698
    redirect(r"^projects/security/components/same-origin\.html$", "https://developer.mozilla.org/docs/Web/Security/Same-origin_policy"),
    redirect(r"^projects/security/components(?P<path>.*)$", "http://www-archive.mozilla.org/projects/security/components{path}"),
    # bug 876889
    redirect(r"^projects/testopia/?", "https://developer.mozilla.org/docs/Mozilla/Bugzilla/Testopia"),
    # bug 874525
    redirect(r"^projects/security/pki/(?P<match>[nj])ss", to_uppercase("https://developer.mozilla.org/docs/{match}SS")),
    # bug 866190
    redirect(r"^projects/security/pki/python-nss/?$", "https://developer.mozilla.org/docs/Python_binding_for_NSS"),
    # bug 1043035
    redirect(r"^projects/security/pki(?:/|/index\.html)?$", "https://developer.mozilla.org/docs/PKI"),
    redirect(r"^projects/security/pki/pkcs11", "https://developer.mozilla.org/docs/Mozilla/Projects/NSS#PKCS_.2311_information"),
    redirect(r"^projects/security/pki/psm", "https://developer.mozilla.org/docs/Mozilla/Projects/PSM"),
    redirect(r"^projects/security/pki/src", "https://developer.mozilla.org/docs/Mozilla/Projects/NSS/NSS_Sources_Building_Testing"),
    # bug 975476
    redirect(r"^projects/security/pki/python-nss/doc/api/current/html(?P<path>.*)$", "https://mozilla.github.io/python-nss-docs{path}"),
    # bug 780672
    redirect(r"^firefox/webhero", "firefox.new"),
    # bug 964107
    redirect(r"^firefox/video", "https://www.youtube.com/firefoxchannel"),
    # bug 948520
    redirect(r"^firefox/livebookmarks", "https://support.mozilla.org/kb/Live%20Bookmarks"),
    # bug 782333
    redirect(r"^firefox/backtoschool/?$", "https://addons.mozilla.org/firefox/collections/mozilla/back-to-school/"),
    redirect(r"^firefox/backtoschool/firstrun/?$", "firefox.firstrun"),
    # bug 824126, 837942
    redirect(r"^ports/qtmozilla(?:/|/index\.html)?$", "https://wiki.mozilla.org/Qt"),
    redirect(r"^ports/os2/?$", "https://wiki.mozilla.org/Ports/os2"),
    redirect(r"^ports(?P<path>.*)", "http://www-archive.mozilla.org/ports{path}"),
    redirect(r"^b2g", "https://support.mozilla.org/products/firefox-os"),
    # Bug 781914
    redirect(r"^contribute/areas\.html$", "mozorg.contribute"),
    redirect(r"^contribute/universityambassadors", "https://campus.mozilla.community/"),
    # Bug 1144949
    redirect(r"^contribute/page/?$", "https://wiki.mozilla.org/Webdev/GetInvolved/mozilla.org"),
    # Bug 763665, 1148127
    redirect(r"^projects/?$", "firefox.new"),
    # Bug 792185 Brand Toolkit -> Style Guide, Issue 8418
    redirect(r"^firefox/brand(/.*)?", "https://mozilla.design/firefox/"),
    # Bug 804810 Identity Guidelines -> Style Guide, Issue 8418
    redirect(r"^foundation/identity-guidelines(/.*)?", "https://mozilla.design/mozilla/"),
    # Bug 945474 - delete Marketplace marketing product page
    # and redirect
    redirect(r"^apps/?$", "https://marketplace.firefox.com/"),
    # Bug 800467 /apps/partners ->
    # marketplace.firefox.com/developers
    redirect(r"apps/partners/?$", "https://marketplace.firefox.com/developers/"),
    # Bug 815527 /m/privacy.html -> /privacy/firefox/
    redirect(r"^m/privacy\.html$", "privacy.notices.firefox"),
    # Bug 1109318 /privacy/you -> privacy/tips/
    # Bug 1238687 /privacy/tips -> teach/smarton/
    # Bug 1436740 /privacy/tips -> internet-health/privacy-security/
    # Issue 8375 /internet-health/ -> foundation.mozilla.org
    redirect(r"^privacy/you/?$", "https://foundation.mozilla.org/internet-health/"),
    redirect(r"^privacy/tips/?$", "https://foundation.mozilla.org/internet-health/"),
    # Bug 821047 /about/mission.html -> /mission/
    redirect(r"^about/mission\.html$", "/mission/"),
    # Bug 784411 /about/mission/ -> /mission/
    redirect(r"^about/mission/?$", "/mission/"),
    # Bug 800298 /webmaker/ -> wm.o and /webmaker/videos/ ->
    # wm.o/videos/
    redirect(r"webmaker/?$", "https://webmaker.org"),
    redirect(r"webmaker/videos/?$", "https://webmaker.org/videos/"),
    # Bug 822817 /telemetry/ ->
    # https://wiki.mozilla.org/Telemetry/FAQ
    redirect(r"telemetry/?$", "https://wiki.mozilla.org/Telemetry/FAQ"),
    # Bug 854561, Issue 7448
    redirect(r"^projects/mozilla-based(\.html|/)?", "https://developer.mozilla.org/docs/Archive/List_of_Mozilla-Based_Applications"),
    redirect(r"^about/mozilla-based/?$", "https://developer.mozilla.org/docs/Archive/List_of_Mozilla-Based_Applications"),
    # Bug 867773, 1238851 - Redirect the Persona URLs to MDN
    redirect(r"^persona(?:/(?:about|developer-faq))?/?$", "https://developer.mozilla.org/Persona"),
    # Bug 1380845 - Redirect persona privacy policy to archive.
    redirect(r"^persona/privacy-policy/?$", "/privacy/archive/persona/2017-07/"),
    redirect(r"^persona/terms-of-service/?$", "/privacy/archive/persona/2017-07/#terms-of-service"),
    # Bug 981176 - For now we'll hard-code a redirect to 1.3
    # In the future this should automatically go to the
    # latest version's notes
    redirect(r"^firefox/os/notes/?$", "/firefox/os/notes/1.3/"),
    # Bug 997577 - /legal/ -> /about/legal/
    redirect(r"^legal/fraud-report/?$", "/about/legal/fraud-report/"),
    redirect(r"^legal/eula/?$", "/about/legal/eula/"),
    redirect(r"^legal/eula/firefox-2/?$", "/about/legal/eula/firefox-2/"),
    redirect(r"^legal/eula/firefox-3/?$", "/about/legal/eula/firefox-3/"),
    # bug 1405436
    redirect(r"^legal/eula/firefox", "/about/legal/terms/firefox/"),
    # Bug 1209643
    redirect(r"^legal/bylaws_amendment_(?P<n>[12])(\.html|/)?", "/foundation/documents/bylaws-amendment-{n}/"),
    redirect(r"^legal/articles(\.html|/)?", "foundation.documents.articles-of-incorporation"),
    redirect(r"^legal/amendment(\.html|/)?", "foundation.documents.articles-of-incorporation-amendment"),
    redirect(r"^legal/bylaws(\.html|/)?", "foundation.documents.bylaws"),
    # bug 960689, 896474
    redirect(r"^about/legal\.html", "legal.index"),
    # Bug 1073269
    redirect(r"^dnt/?$", "https://support.mozilla.org/kb/how-do-i-turn-do-not-track-feature"),
    # bug 1205632
    redirect(r"^js/language(?:/|/index\.html)?$", "https://developer.mozilla.org/docs/Web/JavaScript/Language_Resources", locale_prefix=False),
    redirect(r"^js/language/js20(/.*)?$", "http://www.ecmascript-lang.org", locale_prefix=False),
    redirect(r"^js/language/es4(/.*)?$", "http://www.ecmascript-lang.org", locale_prefix=False),
    redirect(r"^js/language(?P<path>.*)$", "http://www-archive.mozilla.org/js/language{path}"),
    # bug 845988 - remove double slashes in URLs
    # have to specifically match a non-slash on either side of the slashes
    # to force it to match all repeating slashes in one go.
    redirect(r"^(.*[^/])//+([^/].*)$", "/{}/{}", locale_prefix=False),
    # bug 1237875
    redirect(r"^community/forums/?$", "mozorg.about.forums.forums"),
    # bug 927442
    redirect(r"^(firefox/)?community/?", "mozorg.contribute"),
    # bug 925551, issue 8374
    redirect(r"^plugincheck/more_info\.html$", "https://support.mozilla.org/kb/npapi-plugins/"),
    # issue 851727
    redirect(r"^projects/powered-by(\.html|/)?", "mozorg.home"),
    redirect(r"^about/powered-by/?", "mozorg.home"),
    # bug 957664
    redirect(r"^press/awards(?:/|\.html)?$", "https://blog.mozilla.org/press/awards/"),
    # bug 876810
    redirect(r"^hacking/commit-access-policy/?$", "mozorg.about.governance.policies.commit.access-policy"),
    redirect(r"^hacking/committer(/|/faq\.html)?$", "mozorg.about.governance.policies.commit"),
    redirect(r"^hacking/notification/?$", "mozorg.about.governance.policies.commit"),
    redirect(
        r"^hacking/committer/committers-agreement\.(?P<ext>odt|pdf|txt)$",
        "https://static.mozilla.com/foundation/documents/commit-access/committers-agreement.{ext}",
    ),
    redirect(r"^hacking/notification/acceptance-email\.txt$", "https://static.mozilla.com/foundation/documents/commit-access/acceptance-email.txt"),
    # bug 1165344
    redirect(r"^hacking/CVS-Contributor-Form\.(?:pdf|ps)$", "mozorg.about.governance.policies.commit"),
    redirect(r"^hacking/(?:form|getting-cvs-write-access)\.html$", "mozorg.about.governance.policies.commit"),
    redirect(r"^hacking/portable-cpp\.html$", "https://developer.mozilla.org/docs/Mozilla/C++_Portability_Guide"),
    redirect(r"^hacking/rules\.html$", "https://developer.mozilla.org/docs/mozilla-central"),
    redirect(r"^hacking/(?P<page>module-ownership|reviewers)\.html$", "/about/governance/policies/{page}/"),
    redirect(r"^hacking/regression-policy\.html$", "mozorg.about.governance.policies.regressions"),
    # Bug 1040970
    redirect(
        r"^mozillacareers$",
        "https://wiki.mozilla.org/People/mozillacareers",
        query={
            "utm_medium": "redirect",
            "utm_source": "mozillacareers-vanity",
        },
    ),
    # Bug 1090468
    redirect(r"^security/transition\.txt$", "/media/security/transition.txt"),
    # bug 957637
    redirect(r"^sopa/?", "https://blog.mozilla.org/blog/2012/01/19/firefox-users-engage-congress-sopa-strike-stats/"),
    # bug 924687, issue 10736
    redirect(r"^opportunities(?:/|/index\.html)?$", "careers.home"),
    # bug 818321
    redirect(r"^projects/security/tld-idn-policy-list\.html$", "https://wiki.mozilla.org/IDN_Display_Algorithm"),
    redirect(r"^projects/security/membership-policy\.html$", "/about/governance/policies/security-group/membership/"),
    redirect(r"^projects/security/secgrouplist\.html$", "/about/governance/policies/security-group/"),
    redirect(r"^projects/security/security-bugs-policy\.html$", "/about/governance/policies/security-group/bugs/"),
    # bug 818316, 1128579
    redirect(r"^projects/security/certs(?:/(?:index\.html)?)?$", "/about/governance/policies/security-group/certs/"),
    redirect(r"^projects/security/certs/included(?:/(?:index\.html)?)?$", "https://wiki.mozilla.org/CA:IncludedCAs"),
    redirect(r"^projects/security/certs/pending(?:/(?:index\.html)?)?$", "https://wiki.mozilla.org/CA:PendingCAs"),
    redirect(r"^projects/security/certs/policy(?:/(?:index\.html)?)?$", "/about/governance/policies/security-group/certs/policy/"),
    redirect(r"^projects/security/certs/policy/EnforcementPolicy\.html$", "/about/governance/policies/security-group/certs/policy/enforcement/"),
    redirect(r"^projects/security/certs/policy/MaintenancePolicy\.html$", "/about/governance/policies/security-group/certs/policy/maintenance/"),
    redirect(r"^projects/security/certs/policy/InclusionPolicy\.html$", "/about/governance/policies/security-group/certs/policy/inclusion/"),
    redirect(r"^about/governance/policies/security-group/certs/included(?:/(?:index\.html)?)?$", "https://wiki.mozilla.org/CA:IncludedCAs"),
    redirect(r"^about/governance/policies/security-group/certs/pending(?:/(?:index\.html)?)?$", "https://wiki.mozilla.org/CA:PendingCAs"),
    # bug 1068931
    redirect(r"^advocacy/?$", "https://advocacy.mozilla.org/"),
    # bug 887426
    redirect(r"^about/policies/?$", "/about/governance/policies/"),
    redirect(r"^about/policies/participation\.html$", "/about/governance/policies/participation/"),
    redirect(r"^about/policies/policies\.html$", "/about/governance/policies/"),
    # bug 882923
    redirect(r"^opt-out\.html$", "/privacy/websites/#user-choices"),
    # bug 878039
    redirect(r"^access/?$", "https://developer.mozilla.org/docs/Web/Accessibility"),
    redirect(r"^access/architecture\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_architecture"),
    redirect(r"^access/at-vendors\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_Assistive_Technology_Vendors"),
    redirect(r"^access/authors\.html$", "https://developer.mozilla.org/docs/Web/Accessibility/Information_for_Web_authors"),
    redirect(
        r"^access/core-developers\.html$",
        "https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_Information_for_Core_Gecko_Developer",
    ),
    redirect(
        r"^access/evaluators\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_Governments_and_Other_Organization"
    ),
    redirect(r"^access/event-flow\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Event_Process_Procedure"),
    redirect(
        r"^access/external-developers\.html$",
        "https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_External_Developers_Dealing_with_A#community",
    ),
    redirect(r"^access/features\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_Features_in_Firefox"),
    redirect(r"^access/highlevel\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/CSUN_Firefox_Materials"),
    redirect(
        r"^access/platform-apis\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_API_cross-reference#Accessible_Roles"
    ),
    redirect(r"^access/plugins-work\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Mozilla_Plugin_Accessibility"),
    redirect(r"^access/prefs-and-apis\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Embedding_API_for_Accessibility"),
    redirect(r"^access/resources\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Links_and_Resources"),
    redirect(r"^access/section508\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Mozilla_s_Section_508_Compliance"),
    redirect(r"^access/today\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Software_accessibility_today"),
    redirect(
        r"^access/toolkit-checklist\.html$",
        "https://developer.mozilla.org/docs/Mozilla/Accessibility/What_needs_to_be_done_when_building_new_toolkits",
    ),
    redirect(r"^access/ui-developers\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_information_for_UI_designers"),
    redirect(r"^access/users\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_users"),
    redirect(r"^access/w3c-uaag\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/UAAG_evaluation_report"),
    redirect(r"^access/w4a\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/W4A"),
    redirect(
        r"^access/windows/at-apis\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Gecko_info_for_Windows_accessibility_vendors"
    ),
    redirect(r"^access/windows/msaa-server\.html$", "https://developer.mozilla.org/docs/Web/Accessibility/Implementing_MSAA_server"),
    redirect(r"^access/windows/zoomtext\.html$", "https://developer.mozilla.org/docs/Mozilla/Accessibility/ZoomText"),
    redirect(r"^access/donate(\.html|/)?$", "https://foundation.mozilla.org/donate/"),
    # bug 1148187
    redirect(r"^access/(?P<page>.+)$", "http://website-archive.mozilla.org/www.mozilla.org/access/access/{page}"),
    # bug 987852
    redirect(r"^MPL/0\.95/(.*)$", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/0.95/{}", locale_prefix=False),
    redirect(r"^MPL/1\.0/(.*)$", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/1.0/{}", locale_prefix=False),
    redirect(r"^MPL/2\.0/process/(.*)$", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/2.0/process/{}", locale_prefix=False),
    redirect(r"^MPL/NPL/(.*)$", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/NPL/{}", locale_prefix=False),
    redirect(r"^MPL/boilerplate-1\.1/(.*)$", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/boilerplate-1.1/{}", locale_prefix=False),
    redirect(r"^MPL/missing\.html$", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/missing.html", locale_prefix=False),
    # Bug 1216953
    redirect(r"^MPL/MPL-1\.0\.html$", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/1.0/"),
    redirect(r"^MPL/MPL-1\.1\.html$", "/MPL/1.1/"),
    # Bug 987852 & 1201914
    redirect(r"^MPL/(?P<page>.+)\.html$", "/MPL/{page}/"),
    redirect(r"^MPL/2\.0/index\.txt$", "/media/MPL/2.0/index.txt", locale_prefix=False),
    # bug 724682
    redirect(r"^projects/mathml/demo/texvsmml\.html$", "https://developer.mozilla.org/docs/Mozilla_MathML_Project/MathML_Torture_Test"),
    redirect(r"^projects/mathml/fonts(?:/(?:index\.html)?)?$", "https://developer.mozilla.org/Mozilla_MathML_Project/Fonts"),
    redirect(r"^projects/mathml/screenshots(?:/(?:index\.html)?)?$", "https://developer.mozilla.org/Mozilla_MathML_Project/Screenshots"),
    redirect(r"^projects/mathml/authoring\.html$", "https://developer.mozilla.org/en/Mozilla_MathML_Project/Authoring"),
    redirect(r"^projects/mathml/update\.html$", "https://developer.mozilla.org/en/Mozilla_MathML_Project/Status"),
    redirect(r"^projects/mathml(/.*)?$", "https://developer.mozilla.org/en-US/docs/Mozilla/MathML_Project"),
    # bug 961010
    redirect(r"^mobile/credits/?", "/credits/"),
    # bug 897082
    redirect(r"^about/mozilla-spaces.*$", "/contact/spaces/"),
    redirect(r"^about/contact.*$", "/contact/spaces/"),
    redirect(r"^contribute/local/?$", "/contact/communities/"),
    redirect(r"^contribute/local/northamerica\.html$", "/contact/communities/north-america/"),
    redirect(r"^contribute/local/europe\.html$", "/contact/communities/europe/"),
    redirect(r"^contribute/local/latinamerica\.html$", "/contact/communities/latin-america/"),
    redirect(r"^contribute/local/africamideast\.html$", "/contact/communities/africa-middle-east/"),
    redirect(r"^contribute/local/asia\.html$", "/contact/communities/asia-south-pacific/"),
    redirect(r"^contribute/local/southpole\.html$", "/contact/communities/antarctica/"),
    # bug 1393622
    redirect(r"contact/spaces/(?:auckland|tokyo|taipei|london|mountain-view|vancouver|portland)/?$", "/contact/spaces/"),
    redirect("^contribute/buttons/", "https://affiliates.mozilla.org/"),
    # bug 875052
    redirect(r"^about/get-involved", "mozorg.contribute"),
    # bug 878926
    redirect(r"^firefoxflicks/?(?P<p>.*)$", "https://firefoxflicks.mozilla.org/{locale}{p}"),
    # bug 849426
    redirect(r"^about/history(\.html)?$", "/about/history/"),
    redirect(r"^about/bookmarks\.html$", "https://wiki.mozilla.org/Historical_Documents"),
    redirect(r"^about/timeline\.html$", "https://wiki.mozilla.org/Timeline"),
    # bug 1016400, issue 10736
    redirect(r"^about/careers\.html$", "careers.home"),
    # bug 861243 and bug 869489
    redirect(r"^about/manifesto\.html$", "/about/manifesto/"),
    redirect(r"^about/manifesto\.(.*)\.html$", "/{}/about/manifesto/", locale_prefix=False),
    # bug 856077
    redirect(r"^projects/toolkit/?$", "https://developer.mozilla.org/docs/Toolkit_API"),
    redirect(r"^rhino/download\.html$", "https://developer.mozilla.org/docs/Mozilla/Projects/Rhino/Download_Rhino"),
    redirect(r"^rhino/doc\.html$", "https://developer.mozilla.org/docs/Mozilla/Projects/Rhino/Documentation"),
    redirect(r"^rhino/shell\.html$", "https://developer.mozilla.org/docs/Mozilla/Projects/Rhino/Shell"),
    redirect(r"^rhino/?", "https://developer.mozilla.org/docs/Mozilla/Projects/Rhino"),
    # bug 846362
    redirect(r"^community/(index(\.(de|fr|hr|sq))?\.html)?$", "mozorg.contribute"),
    # bug 860532 - Reidrects for governance pages
    redirect(r"^about/governance\.html$", "/about/governance/"),
    redirect(r"^about/roles\.html$", "/about/governance/roles/"),
    redirect(r"^about/organizations\.html$", "/about/governance/organizations/"),
    # bug 876233
    redirect(r"^about/participate/?$", "mozorg.contribute"),
    # bug 790784
    # NB: The /foundation/privacy-policy.html redirect must appear before the
    # foundation redirects added with bug 724633. Otherwise, the address will first
    # be prefixed with a locale, and this redirect will not work.
    redirect(r"^(about/policies/|foundation/)?privacy-policy(/|\.html)?$", "/privacy/websites/"),
    redirect(r"^privacy-policy\.pdf$", "https://static.mozilla.com/moco/en-US/pdf/mozilla_privacypolicy.pdf"),
    # bug 724633 - Porting foundation pages
    # Add redirects for the pdfs that were under /foundation/documents/
    # that will now be served from static.mozilla.com/foundation/documents/
    # (The links within the foundation pages have been updated, but there are
    # probably many links to them from other pages and sites that need to keep
    # working.)
    redirect(r"^foundation/documents/(?P<pdf>[^/]+)\.pdf$", "https://static.mozilla.com/foundation/documents/{pdf}.pdf", re_flags="i"),
    redirect(r"^foundation/donate_form\.pdf$", "https://static.mozilla.com/foundation/documents/donate_form.pdf", re_flags="i"),
    # openwebfund/ and openwebfund/index.html redirect to another site.  Careful because
    # there are other pages under openwebfund that still need to be served from Bedrock.
    redirect(r"^foundation/openwebfund/(index\.html)?$", "https://foundation.mozilla.org/donate/", re_flags="i"),
    redirect(r"^foundation/donate\.html$", "https://foundation.mozilla.org/donate/", re_flags="i"),
    # FIXUPs for changing foo/bar.html to foo/bar/
    # Redirect foundation/foo.html to foundation/foo/, with a redirect for the nice search engines
    redirect(r"^foundation/(?P<page>about|careers|licensing|moco|mocosc)\.html$", "/foundation/{page}/", re_flags="i"),
    # Redirect foundation/anything/foo.html to foundation/anything/foo/,
    # with a redirect for the nice search engines
    redirect(r"^foundation/documents/(?P<page>index|mozilla-200.-financial-faq)\.html$", "/foundation/{page}/", re_flags="i"),
    redirect(
        r"^foundation/(?P<page>(?:annualreport|documents|feed-icon-guidelines|" r"licensing|openwebfund|trademarks)/.*)\.html$",
        "/foundation/{page}/",
        re_flags="i",
    ),
    # bug 442671
    redirect(r"^foundation/trademarks/l10n-policy/?$", "/foundation/trademarks/", re_flags="i"),
    # bug 1074354
    redirect(r"^legal/?$", "/about/legal/"),
    # bug 963816
    redirect(r"^legal/privacy/?$", "/privacy/"),
    redirect(r"^legal/privacy/firefox(?:/|\.html)?$", "/privacy/firefox/"),
    redirect(r"^legal/privacy/oct-2006", "/privacy/archive/firefox/2006-10/"),
    redirect(r"^legal/privacy/june-2008", "/privacy/archive/firefox/2008-06/"),
    redirect(r"^legal/privacy/jan-2009", "/privacy/archive/firefox/2009-01/"),
    redirect(r"^legal/privacy/sept-2009", "/privacy/archive/firefox/2009-09/"),
    redirect(r"^legal/privacy/jan-2010", "/privacy/archive/firefox/2010-01/"),
    redirect(r"^legal/privacy/dec-2010", "/privacy/archive/firefox/2010-12/"),
    redirect(r"^legal/privacy/june-2011", "/privacy/archive/firefox/2011-06/"),
    redirect(r"^legal/privacy/june-2012", "/privacy/archive/firefox/2012-06/"),
    redirect(r"^legal/privacy/sept-2012", "/privacy/archive/firefox/2012-09/"),
    redirect(r"^legal/privacy/dec-2012", "/privacy/archive/firefox/2012-12/"),
    redirect(r"^legal/privacy/firefox-third-party", "/privacy/archive/firefox/third-party/"),
    redirect(r"^legal/privacy/notices-firefox", "/legal/firefox/"),
    redirect(r"^privacy/policies/(?P<page>facebook|firefox-os|websites)/?$", "/privacy/{page}/"),
    # bug 1034859
    redirect(r"^about/buttons/(?P<file>.*)$", "/media/img/careers/buttons/{file}", prepend_locale=False),
    # bug 1003737
    redirect(r"^impressum/?$", "/about/legal/impressum/"),
    # Bug 682619
    redirect(r"^support/thunderbird(/.*)?$", "https://support.mozilla.org/products/thunderbird"),
    redirect(r"^support/firefox(/.*)?$", "https://support.mozilla.org/products/firefox"),
    # bug 1236910
    redirect(r"^support(/.*)?$", "https://support.mozilla.org/"),
    # Bug 1235853
    redirect(r"^facebookapps(/.*)?$", "firefox.new"),
    # Bug 1255882
    redirect(r"^firefox/about/?$", "mozorg.about.index"),
    # bug 453506, 1255882
    redirect(r"^editor/(?P<page>.*)$", "http://www-archive.mozilla.org/editor/{page}"),
    # Bug 453876, 840416
    redirect(r"^add-ons/kodak", "https://addons.mozilla.org/en-US/firefox/addon/4441"),
    # bug 1267736
    redirect(r"^about/patents/?$", "mozorg.about.policy.patents.index"),
    redirect(r"^about/patents/guide/?$", "mozorg.about.policy.patents.guide"),
    redirect(r"^about/patents/license/?$", "mozorg.about.policy.patents.license"),
    redirect(r"^about/patents/license/1\.0/?$", "mozorg.about.policy.patents.license-1.0"),
    redirect(r"^projects/marketing(/.*)?$", "https://wiki.mozilla.org/MarketingGuide"),
    # bug 1288647, 1722760
    redirect(r"^hacking/?$", "https://firefox-source-docs.mozilla.org/"),
    # Issue 10736
    redirect(r"^jobs/?$", "careers.home"),
    redirect(r"^join/?$", "careers.home"),
    # Bug 1262593
    redirect(r"^unix/remote\.html$", "http://www-archive.mozilla.org/unix/remote.html"),
    # Bug 1313023
    redirect(r"^story/?$", "https://foundation.mozilla.org/donate/"),
    # Bug 1317260
    redirect(
        r"^about/governance/policies/security-group/certs/policy/(?P<anchor>inclusion|maintenance|enforcement)/?",
        "/about/governance/policies/security-group/certs/policy/#{anchor}",
    ),
    # Bug 936362
    # only upper-case for XBL. /xbl is a namespace URL for the standard.
    redirect(r"^XBL/?$", "https://www.w3.org/TR/xbl/"),
    redirect(r"^RDF/?$", "https://www.w3.org/RDF/", re_flags="i"),
    # Bug 1332008, 1525853
    redirect(r"^protocol/?$", "https://protocol.mozilla.org"),
    # Bug 1322959 - vanity URL, Issue 8375
    redirect(r"^onlineprivacy/?$", "https://foundation.mozilla.org/internet-health/"),
    # Bug 1335569 - vanity URL, Issue 8375
    redirect(r"^digital-inclusion/?$", "https://foundation.mozilla.org/internet-health/"),
    # Bug 1344270 - vanity URL, Issue 8375
    redirect(r"^open-innovation/?$", "https://foundation.mozilla.org/internet-health/"),
    # Bug 1333146
    redirect(r"^internet-?health-?report/?$", "https://internethealthreport.org/"),
    # Bug 1335040
    redirect(r"^gigabit(/.*)?", "https://wiki.mozilla.org/Gigabit"),
    # Bug 1324504, issue 6994
    redirect(r"^/contribute/studentambassadors(/.*)?", "mozorg.contribute"),
    # Bug 1340600, Issue 7840 - vanity URL
    redirect(
        r"^css-?grid/?$",
        "https://developer.mozilla.org/docs/Learn/CSS/CSS_layout/Grids",
        query={
            "utm_source": "redirect",
            "utm_medium": "collateral",
            "utm_campaign": "css-grid",
        },
    ),
    # Bug 1361194, Issue 8375
    redirect(r"^internethealth/?$", "https://foundation.mozilla.org/internet-health/"),
    # Bug 1384370, Issue 7840
    redirect(r"^developers/?$", "https://developer.mozilla.com/"),
    # Bug 1438464
    redirect(r"^collusion/?$", "https://github.com/mozilla/lightbeam-we"),
    redirect(r"^lightbeam(/.*)?", "https://github.com/mozilla/lightbeam-we"),
    # Bug 1428150
    gone(r"^tabzilla/transbar\.jsonp$"),
    gone(r"^tabzilla/tabzilla\.js$"),
    gone(r"^tabzilla/media/js/tabzilla\.js$"),
    redirect(r"tabzilla/media/css/tabzilla\.css$", "https://mozorg.cdn.mozilla.net/media/css/tabzilla-min.css", locale_prefix=False),
    # Bug 1430887
    redirect(r"^firefox/geolocation/?$", "https://support.mozilla.org/kb/does-firefox-share-my-location-web-sites"),
    # Bug 1422080, 1013349, 1233015
    redirect(r"^about/partnerships/?$", "mozorg.contact.contact-landing"),
    redirect(r"^about/partnerships/contentservices(/.*)?$", "mozorg.contact.contact-landing"),
    redirect(r"^about/partnerships\.html", "mozorg.contact.contact-landing"),
    redirect(r"^about/partnerships/distribution/?$", "/foundation/trademarks/distribution-policy/"),
    # Bug 1436740, Issue 8375
    redirect(r"^teach/?$", "https://foundation.mozilla.org/internet-health/"),
    redirect(r"^teach/smarton/?$", "https://foundation.mozilla.org/internet-health/"),
    redirect(r"^teach/smarton/(?:tracking|security|surveillance)/?$", "https://foundation.mozilla.org/internet-health/"),
    # issue 6266
    redirect(r"^about/policy/leandata/?$", "mozorg.about.policy.lean-data.index"),
    # Issue 6756 - vanity URL, Issue 8375
    redirect(r"^decentralization/?$", "https://foundation.mozilla.org/internet-health/"),
    # issue 6971
    redirect(r"^gear/?$", "https://wiki.mozilla.org/SwagStore"),
    # issue 6994
    redirect(r"^contribute/signup/?$", "mozorg.contribute"),
    redirect(r"^/contribute/task(/.*)?", "mozorg.contribute"),
    redirect(r"^contribute/friends/?$", "mozorg.contribute"),
    redirect(r"^contribute/stories(/.*)?$", "mozorg.contribute"),
    # Issue 6461
    redirect(r"^contribute/events/?$", "https://community.mozilla.org/events/"),
    # issue 7435
    redirect(r"^about/history/details/?$", "mozorg.about.history"),
    # issue 7842
    redirect(r"^enterprise/?$", "firefox.enterprise.index"),
    # Issue 7970
    redirect(r"^moss/mission-partners-india/?$", "mozorg.moss.mission-partners"),
    # Issue 7840
    redirect(r"^developer/?$", "https://developer.mozilla.com/"),
    redirect(r"^developer/browsertest/?$", "https://developer.mozilla.org/docs/Learn/Tools_and_testing/Cross_browser_testing/Automated_testing"),
    redirect(r"^developer/css-grid/?$", "https://developer.mozilla.org/docs/Learn/CSS/CSS_layout/Grids"),
    # Issue 8418
    redirect(r"^styleguide/products/firefox(.+)", "https://mozilla.design/firefox/"),
    redirect(r"^styleguide/identity/firefox(.+)", "https://mozilla.design/firefox/"),
    redirect(r"^styleguide/identity/mozilla(.+)", "https://mozilla.design/mozilla/"),
    redirect(r"^styleguide(/.*)?", "https://mozilla.design/"),
    # Issue 8644, 8932, 15613
    redirect(r"^builders/?$", "https://builders.mozilla.org/"),
    # Issue 6824, 14364
    redirect(r"^technology/?$", "https://future.mozilla.org/"),
    # Issue 8668
    redirect(r"^contact/communities(/.*)?", "https://community.mozilla.org/groups/"),
    # Issue 8641
    redirect(r"^technology/what-is-a-browser/?$", "firefox.browsers.what-is-a-browser"),
    redirect(r"^technology/update-your-browser/?$", "firefox.browsers.update-browser"),
    redirect(r"^technology/incognito-browser/?$", "firefox.browsers.incognito-browser"),
    redirect(r"^technology/browser-history/?$", "firefox.browsers.browser-history"),
    # Issue 8536, 11891
    redirect(r"^etc/firefox/retention(/.*)?", "firefox.new"),
    redirect(r"^firefox/retention/thank-you/?", "firefox.new"),
    # Issue 8374
    redirect(r"^plugincheck/?$", "https://support.mozilla.org/kb/npapi-plugins/"),
    # Vanity URL for EKR's blog
    redirect(r"^ekr/?$", "https://blog.mozilla.org/blog/author/ekrmozilla-com/"),
    # Issue 8375
    redirect(r"^internet-health(/.*)?", "https://foundation.mozilla.org/internet-health/"),
    # Issue 8949
    redirect(r"^donate/?$", "https://foundation.mozilla.org/donate/"),
    redirect(r"^about/governance/policies/security/plugin-whitelist-policy/?$", "https://wiki.mozilla.org/Plugins/Firefox_Whitelist"),
    redirect(r"^about/governance/policies/security-group/tld-idn/?$", "https://wiki.mozilla.org/IDN_Display_Algorithm"),
    # Issue 9560
    redirect(
        r"^openletter/?$",
        "https://foundation.mozilla.org/en/campaigns/sign-letter-AICOA/",
        query={
            "utm_campaign": "2022antitrust",
            "utm_content": "shortlink",
            "utm_medium": "print",
            "utm_source": "washingtonpost",
        },
    ),
    # Bug 1673476
    redirect(r"^/about/governance/policies/security-group/certs/?$", "https://wiki.mozilla.org/CA"),
    # Issue 9254
    redirect(r"^grants(/.*)?$", "mozorg.moss.index"),
    # Issue 9984
    redirect(r"^/about/legal/fraud-report/?$", "/about/legal/defend-mozilla-trademarks/"),
    # Issue 11204
    redirect(r"^(truecolou?rs|turningred)/?$", "firefox.new"),
    # Issue 11991
    redirect(r"^transparency/?$", "mozorg.about.policy.transparency.index"),
    # Issue 14231
    redirect(r"^santa-?locator/?$", "mozorg.home"),
    redirect(r"^landing/firefox/fx100/?$", "firefox.new"),
    redirect(r"^accounts/?$", "mozorg.account"),
    # Issue 13211
    redirect(r"^/en/$", "/en-US/", permanent=True),
    # Issue 13554
    redirect(r"^about/leadership/senior-leadership/$", "/about/leadership/#senior"),
    redirect(r"^about/leadership/mozilla-foundation/$", "/about/leadership/#foundation"),
    redirect(r"^about/leadership/reps-council/$", "/about/leadership/#reps"),
    redirect(r"^about/leadership/boards-of-directors/$", "/about/leadership/#boards"),
    # Issue 13672
    redirect(r"/VendorDPA/?$", "https://assets.mozilla.net/pdf/VendorDPA.pdf", re_flags="i"),
    # Issue 14221
    redirect(r"^firefox/products/?$", "/products/"),
    # Issue 14252
    redirect(r"^stories/?$", "https://blog.mozilla.org/category/products/firefox/"),
    # Issue 14245
    redirect(r"^contact/spaces/berlin/?$", "/contact/spaces/"),
    redirect(r"^contact/spaces/beijing/?$", "/contact/spaces/"),
    redirect(r"^contact/spaces/san-francisco/?$", "/contact/spaces/"),
    redirect(r"^contact/spaces/toronto/?$", "/contact/spaces/"),
    redirect(r"^contact/spaces/paris/?$", "/contact/spaces/"),
    # Issue 14255
    redirect(r"^rise25/?$", "/rise25/nominate/"),
    # Issue 14351
    redirect(r"^research/?$", "https://foundation.mozilla.org/research/"),
    redirect(r"^research/cc/?$", "https://foundation.mozilla.org/research/library/?topics=187"),
    # redirects that don't need a lang code prefix
    redirect(r"^diversity/?$", "mozorg.diversity.2022.index", locale_prefix=False),
    redirect(r"^webvision/?$", "mozorg.about.webvision.summary", locale_prefix=True, prepend_locale=False),
    # issue 14944
    redirect(r"^nothing-?personal/?$", "firefox.nothing-personal.index"),
    # Issue 15008
    redirect(r"^try-picture-in-picture/?$", "firefox.features.picture-in-picture"),
)
