# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import requests

from .base import flatten, url_test

UA_ANDROID = {"User-Agent": "Mozilla/5.0 (Android 6.0.1; Mobile; rv:51.0) Gecko/51.0 Firefox/51.0"}
UA_IOS = {"User-Agent": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8F190"}

URLS = flatten(
    (
        # bug 832348 **/index.html -> **/
        url_test("/any/random/url/with/index.html", "/any/random/url/with/"),
        # bug 774675 + also see Issue 13211 for why /en/ isn't included here any more
        url_test("/es/", "/es-ES/", status_code=requests.codes.found),
        url_test("/pt/", "/pt-BR/", status_code=requests.codes.found),
        # bug 795970 - lowercase to uppercase, e.g. en-us to en-US
        url_test("/en-us/about/", "/en-US/about/", status_code=requests.codes.found),
        url_test("/es-es/about/", "/es-ES/about/", status_code=requests.codes.found),
        url_test("/pt-br/about/", "/pt-BR/about/", status_code=requests.codes.found),
        # bug 880182
        url_test("/ja-JP-mac/", "/ja/", status_code=requests.codes.found),
        # bug 795970 - lowercase to uppercase, e.g. en-us to en-US
        url_test("/en-us/", "/en-US/", status_code=requests.codes.found),
        url_test("/pt-br/", "/pt-BR/", status_code=requests.codes.found),
        # bug 845988 - remove double slashes in URLs
        url_test("/en-US/firefox//all/", "/en-US/firefox/all/"),
        url_test("/pt-BR/////thunderbird/", "/pt-BR/thunderbird/"),
        # bug 874913
        url_test("/en-US/{,products/}download.html{,?stuff=whatnot}", "/en-US/firefox/new/"),
        url_test("/{,products/}download.html{,?stuff=whatnot}", "/firefox/new/"),
        # bug 845580
        url_test("/en-US/home/", "/en-US/firefox/new/"),
        # bug 948605
        url_test("/en-US/firefox/xp-any-random-thing", "/en-US/firefox/new/"),
        url_test("/en-US/products/firefox/start/", "http://start.mozilla.org"),
        url_test(
            "/start/the-sm-one",
            "http://www.seamonkey-project.org/start/",
            req_headers={"User-Agent": "mozilla seamonkey"},
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test("/start/any-random-thing", "/firefox/new/", resp_headers={"Cache-Control": "max-age=0"}),
        # bug 856081 redirect /about/drivers https://wiki.mozilla.org/Firefox/Drivers
        url_test("/about/drivers{/,.html}", "https://wiki.mozilla.org/Firefox/Drivers"),
        # community
        # bug 885797
        url_test("/community/{directory,wikis,blogs,websites}.html", "https://wiki.mozilla.org/Websites/Directory"),
        # bug 885856
        url_test("/projects/index.{de,fr,hr,sq}.html", "/{de,fr,hr,sq}/firefox/"),
        # bug 856075
        url_test("/projects/technologies.html", "https://developer.mozilla.org/docs/Mozilla/Using_Mozilla_code_in_other_projects"),
        # bug 787269
        url_test(
            "/projects/security/components/signed-script{s,-example}.html",
            "https://developer.mozilla.org/docs/Bypassing_Security_Restrictions_and_Signing_Code",
        ),
        # bug 874526, 877698
        url_test("/projects/security/components/any-random-thing", "http://www-archive.mozilla.org/projects/security/components/any-random-thing"),
        # bug 876889
        url_test("/projects/testopia/", "https://developer.mozilla.org/docs/Mozilla/Bugzilla/Testopia"),
        # bug 874525
        url_test("/projects/security/pki/{n,j}ss/random-thing", "https://developer.mozilla.org/docs/{N,J}SS"),
        # bug 866190
        url_test("/projects/security/pki/python-nss/", "https://developer.mozilla.org/docs/Python_binding_for_NSS"),
        # bug 1043035
        url_test("/projects/security/pki/{,index.html}", "https://developer.mozilla.org/docs/PKI"),
        url_test("/projects/security/pki/pkcs11-random-thing", "https://developer.mozilla.org/docs/Mozilla/Projects/NSS#PKCS_.2311_information"),
        url_test("/projects/security/pki/psm-random-thing", "https://developer.mozilla.org/docs/Mozilla/Projects/PSM"),
        url_test("/projects/security/pki/src-random-thing", "https://developer.mozilla.org/docs/Mozilla/Projects/NSS/NSS_Sources_Building_Testing"),
        # bug 975476
        url_test("/projects/security/pki/python-nss/doc/api/current/html/random/stuff/", "https://mozilla.github.io/python-nss-docs/random/stuff/"),
        # bug 780672
        url_test("/firefox/webhero/random/stuff/", "/firefox/new/"),
        # bug 964107
        url_test("/firefox/video/random/stuff/", "https://www.youtube.com/firefoxchannel"),
        # bug 948520
        url_test("/firefox/livebookmarks/random/stuff/", "https://support.mozilla.org/kb/Live%20Bookmarks"),
        # bug 782333
        url_test("/firefox/backtoschool/", "https://addons.mozilla.org/firefox/collections/mozilla/back-to-school/"),
        url_test("/firefox/backtoschool/firstrun/", "/firefox/firstrun/"),
        # bug 824126, 837942
        url_test("/ports/qtmozilla/{,index.html}", "https://wiki.mozilla.org/Qt"),
        url_test("/ports/os2/", "https://wiki.mozilla.org/Ports/os2"),
        url_test("/ports/other-things/", "http://www-archive.mozilla.org/ports/other-things/"),
        # bug 1205632
        url_test("/js/language/", "https://developer.mozilla.org/docs/Web/JavaScript/Language_Resources"),
        url_test("/js/language/js20/", "http://www.ecmascript-lang.org"),
        url_test("/js/language/es4/", "http://www.ecmascript-lang.org"),
        url_test("/js/language/E262-3-errata.html", "http://www-archive.mozilla.org/js/language/E262-3-errata.html"),
        # bug 927442
        url_test("{/firefox,}/community/", "/contribute/"),
        # bug 925551, issue 8374
        url_test("/plugincheck/more_info.html", "https://support.mozilla.org/kb/npapi-plugins/"),
        # bug 854561, Issue 7448
        url_test("/projects/mozilla-based{.html,/}", "https://developer.mozilla.org/docs/Archive/List_of_Mozilla-Based_Applications"),
        url_test("/about/mozilla-based/", "https://developer.mozilla.org/docs/Archive/List_of_Mozilla-Based_Applications"),
        # bug 957664
        url_test("/press/awards{/,.html}", "https://blog.mozilla.org/press/awards/"),
        # issue 8096
        url_test("/firefox/beta/all/", "/firefox/all/desktop-beta/"),
        url_test("/firefox/developer/all/", "/firefox/all/desktop-developer/"),
        url_test("/firefox/aurora/all/", "/firefox/all/desktop-developer/"),
        url_test("/firefox/nightly/all/", "/firefox/all/desktop-nightly/"),
        url_test("/firefox/organizations/all/", "/firefox/all/desktop-esr/"),
        url_test("/firefox/android/all/", "/firefox/all/android-release/"),
        url_test("/firefox/android/beta/all/", "/firefox/all/android-beta/"),
        url_test("/firefox/android/nightly/all/", "/firefox/all/android-nightly/"),
        url_test("/projects/firefox/3.6.10/whatsnew/bunny-lebowski/", "/firefox/3.6.10/whatsnew/bunny-lebowski/"),
        url_test("/projects/firefox/4.0/firstrun/", "/firefox/4.0/firstrun/"),
        url_test("/projects/firefox/4.0a2/firstrun/stuff", "/firefox/nightly/firstrun/stuff"),
        # bug 1275483
        url_test("/firefox/nightly/whatsnew/", "/firefox/nightly/firstrun/"),
        # bug 1299947, 1314603, 1328409
        url_test(
            "/{beta,aurora,nightly}/",
            "/firefox/channel/android/#{beta,aurora,nightly}",
            req_headers=UA_ANDROID,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/{beta,aurora,nightly}/", "/firefox/channel/ios/#{beta,aurora,nightly}", req_headers=UA_IOS, resp_headers={"Cache-Control": "max-age=0"}
        ),
        url_test("/{beta,aurora,nightly}/", "/firefox/channel/desktop/#{beta,aurora,nightly}", resp_headers={"Cache-Control": "max-age=0"}),
        url_test(
            "/firefox/{beta,aurora,nightly}/",
            "/firefox/channel/android/#{beta,aurora,nightly}",
            req_headers=UA_ANDROID,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/firefox/{beta,aurora,nightly}/",
            "/firefox/channel/ios/#{beta,aurora,nightly}",
            req_headers=UA_IOS,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test("/firefox/{beta,aurora,nightly}/", "/firefox/channel/desktop/#{beta,aurora,nightly}", resp_headers={"Cache-Control": "max-age=0"}),
        url_test("/mobile/{beta,aurora,nightly}/", "/firefox/channel/android/#{beta,aurora,nightly}"),
        # bug 1299947, 1326383
        url_test("/firefox/channel/", "/firefox/channel/android/", req_headers=UA_ANDROID, resp_headers={"Cache-Control": "max-age=0"}),
        url_test("/firefox/channel/", "/firefox/channel/ios/", req_headers=UA_IOS, resp_headers={"Cache-Control": "max-age=0"}),
        url_test("/firefox/channel/", "/firefox/channel/desktop/", resp_headers={"Cache-Control": "max-age=0"}),
        url_test("/firefox/unsupported-systems.html", "/firefox/unsupported-systems/"),
        url_test("/download/", "/firefox/new/"),
        # Bug 1409554
        url_test("/{firefox,mobile}/download/", "/firefox/new/"),
        # also deals with anything after download/
        url_test("/firefox/download/stuff/", "/firefox/new/"),
        # Issue #6045
        url_test("/firefox/download", "/firefox/new/"),
        url_test("/firefox/firefox.exe", "/"),
        # should be case insensitive
        url_test("/pt-BR/FireFox/Firefox.EXE", "/pt-BR/"),
        # bug 821006
        url_test("/firefox/all.html", "/firefox/all/"),
        # bug 727561
        url_test("/firefox/search{,.html}", "/firefox/new/"),
        # bug 860865, 1101220, issue 8096
        url_test("/firefox/all-{beta,rc}{/,.html}", "/firefox/all/desktop-beta/"),
        url_test("/firefox/all-aurora{/,.html}", "/firefox/all/desktop-developer/"),
        url_test("/firefox/aurora/{notes,system-requirements}/", "/firefox/developer/{notes,system-requirements}/"),
        url_test("/firefox/organizations/all.html", "/firefox/all/desktop-esr/"),
        # bug 729329
        url_test("/mobile/sync/is/da/best/", "/firefox/features/sync/"),
        # bug 882845
        url_test("/firefox/toolkit/download-to-your-devices/because-i-say-so/", "/firefox/new/"),
        # bug 1014823
        url_test("/pt-BR/{products/,}firefox/releases/whatsnew/", "/pt-BR/firefox/whatsnew/"),
        # bug 929775
        url_test(
            "/firefox/update/and/stuff/",
            "/firefox/new/",
            query={
                "utm_source": "firefox-browser",
                "utm_medium": "firefox-browser",
                "utm_campaign": "firefox-update-redirect",
            },
        ),
        # bug 868182
        url_test("/firefox/mobile/faq/?os=firefox-os", "https://support.mozilla.org/products/firefox-os"),
        # Bug 986174
        url_test("/{m,{firefox/,}mobile}/features/", "/firefox/browsers/mobile/"),
        url_test("/{m,{firefox/,}mobile}/faq/", "https://support.mozilla.org/products/mobile"),
        # bug 885799, 952429
        url_test("/projects/calendar/holidays.html", "https://www.thunderbird.net/calendar/holidays/"),
        url_test("/projects/calendar/random/stuff/", "https://www.thunderbird.net/calendar/"),
        # bug 1388914
        url_test("/thunderbird{,/}", "https://www.thunderbird.net/"),
        url_test("/thunderbird/channel/", "https://www.thunderbird.net/channel/"),
        url_test("/thunderbird/features/", "https://www.thunderbird.net/features/"),
        url_test("/thunderbird/52.6.0/releasenotes/", "https://www.thunderbird.net/thunderbird/52.6.0/releasenotes/"),
        url_test("/thunderbird/52.6.0/system-requirements/", "https://www.thunderbird.net/thunderbird/52.6.0/system-requirements/"),
        # bug 1211007
        url_test("/thunderbird/download", "https://www.thunderbird.net/"),
        # bug 1124038
        url_test("/thunderbird/organizations/{all-esr.html,faq/}", "https://www.thunderbird.net/organizations/"),
        # bug 1123399, 1150649
        url_test("/thunderbird/all.htm", "https://www.thunderbird.net/thunderbird/all/"),
        url_test("/thunderbird/all-beta.html", "https://www.thunderbird.net/thunderbird/beta/all/"),
        url_test("/thunderbird/early_releases/downloads/", "https://www.thunderbird.net/thunderbird/beta/all/"),
        url_test("/thunderbird/early_releases/", "https://www.thunderbird.net/thunderbird/beta/all/"),
        # bug 1081917, 1029829, 1029838
        url_test(
            "/thunderbird/releases/0.9.html",
            "http://website-archive.mozilla.org/www.mozilla.org/thunderbird_releasenotes/en-US/thunderbird/releases/0.9.html",
        ),
        # should catch everything 1.* to 29.*
        url_test(
            "/thunderbird/{1,5,15,29}.0beta/{releasenotes,system-requirements}/",
            "http://website-archive.mozilla.org/www.mozilla.org/thunderbird_releasenotes"
            "/en-US/thunderbird/{1,5,15,29}.0beta/{releasenotes,system-requirements}/",
        ),
        # bug 1124042
        url_test("/thunderbird/features/email_providers.html", "https://www.thunderbird.net/email-providers/"),
        # bug 1133266
        url_test("/thunderbird/legal/privacy/", "/privacy/thunderbird/"),
        url_test("/thunderbird/about/privacy-policy/", "/privacy/archive/thunderbird/2010-06/"),
        # bug 1196578
        url_test("/thunderbird/about/legal/eula/", "/about/legal/eula/"),
        url_test("/thunderbird/about/legal/eula/thunderbird2.html", "/about/legal/eula/thunderbird-2/"),
        url_test("/thunderbird/about/legal/eula/thunderbird.html", "/about/legal/eula/thunderbird-1.5/"),
        # bug 1204579
        url_test("/thunderbird/2.0.0.0/eula/", "/about/legal/eula/thunderbird-2/"),
        url_test("/thunderbird/about/legal/", "/about/legal/terms/mozilla/"),
        url_test("/thunderbird/download/", "https://www.thunderbird.net/"),
        url_test("/thunderbird/about/", "https://wiki.mozilla.org/Thunderbird"),
        url_test("/thunderbird/about/mission/", "https://wiki.mozilla.org/Thunderbird"),
        url_test("/thunderbird/about/{careers,contact,get-involved}/", "https://wiki.mozilla.org/Thunderbird#Contributing"),
        url_test("/thunderbird/community/", "https://wiki.mozilla.org/Thunderbird#Contributing"),
        url_test("/thunderbird/3.1{a,b,rc}{1,2}/", "http://website-archive.mozilla.org/www.mozilla.org/thunderbird/thunderbird/3.1{a,b,rc}{1,2}/"),
        url_test("/thunderbird/{6,7,8,9}.0beta/", "http://website-archive.mozilla.org/www.mozilla.org/thunderbird/thunderbird/{6,7,8,9}.0beta/"),
        url_test(
            "/thunderbird/about/{board,press,staff}/",
            "http://website-archive.mozilla.org/www.mozilla.org/thunderbird/thunderbird/about/{board,press,staff}/",
        ),
        # bug 1295332
        url_test("/hello/", "https://support.mozilla.org/kb/hello-status"),
        url_test("/firefox/hello/start", "https://support.mozilla.org/kb/hello-status"),
        url_test("/firefox/{46.0,46.0.1,46.0a1,46.0a2}/hello/start", "https://support.mozilla.org/kb/hello-status"),
        # Bug 1110927
        url_test("/firefox/start/central.html", "/firefox/new/"),
        url_test("/firefox/sync/firstrun.html", "/firefox/features/sync/"),
        # bug 876810
        url_test("/hacking/commit-access-policy/", "/about/governance/policies/commit/access-policy/"),
        url_test("/hacking/committer/{,faq.html}", "/about/governance/policies/commit/"),
        url_test("/hacking/notification/", "/about/governance/policies/commit/"),
        url_test(
            "/hacking/committer/committers-agreement.{odt,pdf,txt}",
            "https://static.mozilla.com/foundation/documents/commit-access/committers-agreement.{odt,pdf,txt}",
        ),
        url_test("/hacking/notification/acceptance-email.txt", "https://static.mozilla.com/foundation/documents/commit-access/acceptance-email.txt"),
        # bug 1165344
        url_test("/hacking/CVS-Contributor-Form.{pdf,ps}", "/about/governance/policies/commit/"),
        url_test("/hacking/{form,getting-cvs-write-access}.html", "/about/governance/policies/commit/"),
        url_test("/hacking/portable-cpp.html", "https://developer.mozilla.org/docs/Mozilla/C++_Portability_Guide"),
        url_test("/hacking/rules.html", "https://developer.mozilla.org/docs/mozilla-central"),
        url_test("/hacking/{module-ownership,reviewers}.html", "/about/governance/policies/{module-ownership,reviewers}/"),
        url_test("/hacking/regression-policy.html", "/about/governance/policies/regressions/"),
        # Bug 1040970
        url_test(
            "/mozillacareers",
            "https://wiki.mozilla.org/People/mozillacareers",
            query={
                "utm_medium": "redirect",
                "utm_source": "mozillacareers-vanity",
            },
        ),
        # Bug 987852 & 1201914
        url_test("/MPL/Revision-FAQ.html", "/MPL/Revision-FAQ/"),
        url_test("/MPL/2.0/index.txt", "/media/MPL/2.0/index.txt"),
        # Bug 1090468
        url_test("/security/transition.txt", "/media/security/transition.txt"),
        # Bug 920212
        url_test("/firefox/fx/", "/firefox/new/"),
        # Bug 979531, 1003727, 979664, 979654, 979660, 1150713
        url_test("/firefox/customize/", "https://support.mozilla.org/kb/customize-firefox-controls-buttons-and-toolbars"),
        url_test("/firefox/{performance,happy,speed,memory}/", "/firefox/features/fast/"),
        url_test("/firefox/security/", "/firefox/features/private/"),
        url_test("/firefox/technology/", "https://developer.mozilla.org/docs/Tools"),
        url_test("/firefox/sms/{,sent}", "/firefox/new/"),
        # Previously Bug 979527 / Github #10004 "Getting Started" Page
        url_test("{/products,}/firefox/central{/,.html}", "/firefox/new/"),
        # bug 868169
        url_test(
            "/mobile/android-download.html?dude=abiding",
            "https://play.google.com/store/apps/details",
            query={"id": "org.mozilla.firefox", "dude": "abiding"},
        ),
        url_test(
            "/mobile/android-download-beta.html?walter=raging",
            "https://play.google.com/store/apps/details",
            query={"id": "org.mozilla.firefox_beta", "walter": "raging"},
        ),
        # bug 877198
        url_test("/press/news.html", "https://blog.mozilla.org/press/"),
        url_test(
            "/press/mozilla-2003-10-15.html",
            "https://blog.mozilla.org/press/2003/10/mozilla-foundation-launches-new-web-browser-and-end-user-services/",
        ),
        url_test(
            "/press/mozilla-2004-02-09.html",
            "https://blog.mozilla.org/press/2004/02/new-round-of-releases-extends-mozilla-project%C2%92s-standards-based-open-source-offerings/",
        ),
        url_test("/press/mozilla-2004-02-17.html", "https://blog.mozilla.org/press/2004/02/mozilla-gains-stronghold-in-europe/"),
        url_test(
            "/press/mozilla-2004-02-26.html", "https://blog.mozilla.org/press/2004/02/mozilla-foundation-rallies-supporters-to-take-back-the-web/"
        ),
        url_test("/press/mozilla-2004-05-03.html", "https://blog.mozilla.org/press/2004/05/mozilla-foundation-releases-thunderbird-0-6/"),
        url_test("/press/mozilla-2004-06-15.html", "https://blog.mozilla.org/press/2004/06/mozilla-reloads-firefox/"),
        url_test("/press/mozilla-2004-06-16.html", "https://blog.mozilla.org/press/2004/06/mozilla-foundation-releases-thunderbird-0-7/"),
        url_test(
            "/press/mozilla-2004-06-30.html", "https://blog.mozilla.org/press/2004/06/mozilla-foundation-announces-more-open-scriptable-plugins/"
        ),
        url_test(
            "/press/mozilla-2004-08-02.html", "https://blog.mozilla.org/press/2004/08/mozilla-foundation-announces-security-bug-bounty-program/"
        ),
        url_test("/press/mozilla-2004-08-10.html", "https://blog.mozilla.org/press/2004/08/mozilla-foundation-announces-xforms-development-project/"),
        url_test("/press/mozilla-2004-08-18.html", "https://blog.mozilla.org/press/2004/08/mozilla-affiliate-in-japan-kicks-off/"),
        url_test(
            "/press/mozilla-2004-09-14-01.html",
            "https://blog.mozilla.org/press/2004/09/mozilla-foundation-announces-first-payments-of-security"
            "-bug-bounty-program-further-strengthens-browser-security/",
        ),
        url_test("/press/mozilla-2004-09-14-02.html", "https://blog.mozilla.org/press/2004/09/firefox-preview-release-and-thunderbird-0-8-released/"),
        url_test(
            "/press/mozilla-2004-09-20.html",
            "https://blog.mozilla.org/press/2004/09/mozilla-firefox-preview-release-hits-one-million-downloads-in-first-four-days-of-availability/",
        ),
        url_test("/press/mozilla-2004-10-01-02.html", "https://blog.mozilla.org/press/2004/10/important-security-update-for-firefox-available/"),
        url_test(
            "/press/mozilla-2004-11-09.html",
            "https://blog.mozilla.org/press/2004/11/mozilla-foundation-releases-the-highly-anticipated-mozilla-firefox-1-0-web-browser/",
        ),
        url_test(
            "/press/mozilla-2004-11-22.html", "https://blog.mozilla.org/press/2004/11/important-update-to-german-language-version-of-firefox-1-0/"
        ),
        url_test(
            "/press/mozilla-2004-12-15.html",
            "https://blog.mozilla.org/press/2004/12/mozilla-foundation-places-two-page-advocacy-ad-in-the-new-york-times/",
        ),
        url_test("/press/mozilla-2004-12-7.html", "https://blog.mozilla.org/press/2004/12/mozilla-thunderbird-1-0-email-client-has-landed/"),
        url_test(
            "/press/mozilla-2005-01-07.html",
            "https://blog.mozilla.org/press/2005/01/mozilla-firefox-and-thunderbird-to-support-new-open-standard-platform-for-usb-drives/",
        ),
        url_test(
            "/press/mozilla-2005-02-02.html",
            "https://blog.mozilla.org/press/2005/02/mozilla-foundation-announces-beta-release-of-xforms-1-0-recommendation/",
        ),
        url_test(
            "/press/mozilla-2005-02-16.html",
            "https://blog.mozilla.org/press/2005/01/mozilla-firefox-and-thunderbird-to-support-new-open-standard-platform-for-usb-drives/",
        ),
        url_test("/press/mozilla-2005-02-24.html", "https://blog.mozilla.org/press/2005/02/mozilla-foundation-announces-update-to-firefox/"),
        url_test("/press/mozilla-2005-03-04.html", "https://blog.mozilla.org/press/2005/03/mozilla-foundation-expands-with-launch-of-mozilla-china/"),
        url_test("/press/mozilla-2005-03-23.html", "https://blog.mozilla.org/press/2005/03/mozilla-foundation-releases-security-update-to-firefox/"),
        url_test("/press/mozilla-2005-03-28.html", "https://blog.mozilla.org/press/2005/03/mozilla-foundation-awards-bug-bounties/"),
        url_test(
            "/press/mozilla-2005-05-13.html",
            "https://blog.mozilla.org/press/2005/05/mozilla-foundation-co-hosts-europes-leading-xml-and-web-developer-conference/",
        ),
        url_test(
            "/press/mozilla-2005-07-28.html",
            "https://blog.mozilla.org/press/2005/07/mozilla-headlines-two-key-open-source-development-conferences-in-august/",
        ),
        url_test(
            "/press/mozilla-2005-08-03.html",
            "https://blog.mozilla.org/press/2005/08/mozilla-foundation-forms-new-organization-to-further-the-creation-of-free"
            "-open-source-internet-software-including-the-award-winning-mozilla-firefox-browser/",
        ),
        url_test(
            "/press/mozilla-2005-10-03.html", "https://blog.mozilla.org/press/2005/10/mozilla-launches-beta-of-comprehensive-online-developer-center/"
        ),
        url_test("/press/mozilla-2005-10-19.html", "https://blog.mozilla.org/press/2005/10/firefox-surpasses-100-million-downloads/"),
        url_test(
            "/press/mozilla-2005-11-29.html",
            "https://blog.mozilla.org/press/2005/11/mozilla-introduces-firefox-1-5-and-ups-the-ante-in-web-browsing/",
        ),
        url_test("/press/mozilla-2005-11-3.html", "https://blog.mozilla.org/press/2005/11/mozilla-kicks-off-extend-firefox-competition/"),
        url_test("/press/mozilla-2005-11-30.html", "https://blog.mozilla.org/press/2005/11/firefox-1-5-adds-answers-com-for-quick-reference/"),
        url_test("/press/mozilla-2005-12-2.html", "https://blog.mozilla.org/press/2005/12/mozilla-launches-firefox-flicks-campaign/"),
        url_test("/press/mozilla-2005-12-22.html", "https://blog.mozilla.org/press/2005/12/mozilla-launches-firefox-flicks-ad-contest/"),
        url_test("/press/mozilla-2006-01-12.html", "https://blog.mozilla.org/press/2006/01/mozilla-releases-thunderbird-1-5-email-client/"),
        url_test("/press/mozilla-2006-01-24.html", "https://blog.mozilla.org/press/2006/01/firefox-1-5-adoption-rising-as-browser-garners-acclaim/"),
        url_test("/press/mozilla-2006-01-25.html", "https://blog.mozilla.org/press/2006/01/indie-film-all-stars-foin-firefox-flicks-crew/"),
        url_test(
            "/press/mozilla-2006-02-03.html",
            "https://blog.mozilla.org/press/2006/02/mozilla-releases-preview-of-application-framework-for"
            "-development-of-cross-platform-internet-client-applications/",
        ),
        url_test("/press/mozilla-2006-03-02.html", "https://blog.mozilla.org/press/2006/03/mozilla-announces-winners-of-extend-firefox-competition/"),
        url_test(
            "/press/mozilla-2006-04-12.html",
            "https://blog.mozilla.org/press/2006/04/mozilla-showcases-first-round-of-community-produced-firefox-flicks-videos/",
        ),
        url_test(
            "/press/mozilla-2006-04-18.html",
            "https://blog.mozilla.org/press/2006/04/mozilla-receives-over-280-community-produced-videos-for-firefox-flicks/",
        ),
        url_test("/press/mozilla-2006-04-27.html", "https://blog.mozilla.org/press/2006/04/firefox-flicks-video-contest-winners-announced/"),
        url_test(
            "/press/mozilla-2006-06-14.html", "https://blog.mozilla.org/press/2006/06/mozilla-feeds-soccer-fans-passion-with-new-firefox-add-on/"
        ),
        url_test(
            "/press/mozilla-2006-10-11.html",
            "https://blog.mozilla.org/press/2006/10/qualcomm-launches-project-in-collaboration-with-mozilla"
            "-foundation-to-develop-open-source-version-of-eudora-email-program/",
        ),
        url_test("/press/mozilla-2006-10-24-02.html", "https://blog.mozilla.org/press/2006/10/firefox-moving-the-internet-forward/"),
        url_test(
            "/press/mozilla-2006-10-24.html",
            "https://blog.mozilla.org/press/2006/10/mozilla-releases-major-update-to-firefox-and-raises-the-bar-for-online-experience/",
        ),
        url_test(
            "/press/mozilla-2006-11-07.html",
            "https://blog.mozilla.org/press/2006/11/adobe-and-mozilla-foundation-to-open-source-flash-player-scripting-engine/",
        ),
        url_test(
            "/press/mozilla-2006-12-04.html",
            "https://blog.mozilla.org/press/2006/12/the-world-economic-forum-announces-technology-pioneers-2007-mozilla-selected/",
        ),
        url_test("/press/mozilla-2006-12-11.html", "https://blog.mozilla.org/press/2006/12/mozilla-firefox-headed-for-primetime/"),
        url_test(
            "/press/mozilla-2007-02-07.html",
            "https://blog.mozilla.org/press/2007/02/kodak-and-mozilla-join-forces-to-make-sharing-photos-even-easier/",
        ),
        url_test("/press/mozilla-2007-03-27.html", "https://blog.mozilla.org/press/2007/03/mozilla-launches-new-firefox-add-ons-web-site/"),
        url_test(
            "/press/mozilla-2007-03-28.html",
            "https://blog.mozilla.org/press/2007/03/mozilla-and-ebay-working-together-to-make-the-auction-experience"
            "-easier-for-firefox-users-in-france-germany-and-the-uk/",
        ),
        url_test("/press/mozilla-2007-04-19.html", "https://blog.mozilla.org/press/2007/04/mozilla-thunderbird-2-soars-to-new-heights/"),
        url_test(
            "/press/mozilla-2007-05-16.html",
            "https://blog.mozilla.org/press/2007/05/united-nations-agency-awards-mozilla-world-information-society-award/",
        ),
        url_test(
            "/press/mozilla-2007-07-04.html", "https://blog.mozilla.org/press/2007/07/mozilla-and-ebay-launch-firefox-companion-for-ebay-users/"
        ),
        url_test("/press/mozilla-2007-08-10.html", "https://blog.mozilla.org/press/2007/08/mozilla-to-host-24-hour-worldwide-community-event/"),
        url_test(
            "/press/mozilla-2007-08-28.html",
            "https://blog.mozilla.org/press/2007/08/mozilla-welcomes-students-back-to-school-with-firefox-campus-edition/",
        ),
        url_test(
            "/press/mozilla-2007-09-17-faq.html",
            "https://blog.mozilla.org/press/2007/09/mozilla-launches-internet-mail-and-communications-initiative/",
        ),
        url_test(
            "/press/mozilla-2007-09-17.html", "https://blog.mozilla.org/press/2007/09/mozilla-launches-internet-mail-and-communications-initiative/"
        ),
        url_test(
            "/press/mozilla-2008-01-07-faq.html", "https://blog.mozilla.org/press/2008/01/mozilla-appoints-john-lilly-as-chief-executive-officer/"
        ),
        url_test("/press/mozilla-2008-01-07.html", "https://blog.mozilla.org/press/2008/01/mozilla-appoints-john-lilly-as-chief-executive-officer/"),
        url_test("/press/mozilla-2008-02-19-faq.html", "https://blog.mozilla.org/press/2008/02/mozilla-messaging-starts-up-operations/"),
        url_test("/press/mozilla-2008-02-19.html", "https://blog.mozilla.org/press/2008/02/mozilla-messaging-starts-up-operations/"),
        url_test(
            "/press/mozilla-2008-05-28.html",
            "https://blog.mozilla.org/press/2008/05/mozilla-aims-to-set-guinness-world-record-on-firefox-3-download-day/",
        ),
        url_test(
            "/press/mozilla-2008-06-17-faq.html",
            "https://blog.mozilla.org/press/2008/06/mozilla-releases-firefox-3-and-redefines-the-web-experience/",
        ),
        url_test(
            "/press/mozilla-2008-06-17.html", "https://blog.mozilla.org/press/2008/06/mozilla-releases-firefox-3-and-redefines-the-web-experience/"
        ),
        url_test(
            "/press/mozilla-2008-07-02.html",
            "https://blog.mozilla.org/press/2008/07/mozilla-sets-new-guinness-world-record-with-firefox-3-downloads/",
        ),
        url_test(
            "/press/mozilla-2008-11-18.html",
            "https://blog.mozilla.org/press/2008/11/mozilla-launches-fashion-your-firefox-and-makes-it-easy-to-customize-the-browsing-experience/",
        ),
        url_test(
            "/press/mozilla-2008-12-03.html",
            "https://blog.mozilla.org/press/2008/12/mozilla-and-zazzle-announce-strategic-relationship-for-apparel-on-demand/",
        ),
        url_test(
            "/press/mozilla-2009-03-31.html",
            "https://blog.mozilla.org/press/2009/03/%C2%AD%C2%ADmozilla-adds-style-and-star-power-to-firefox-with-new-personas/",
        ),
        url_test("/press/mozilla-2009-06-30-faq.html", "https://blog.mozilla.org/press/2009/06/mozilla-advances-the-web-with-firefox-3-5/"),
        url_test("/press/mozilla-2009-06-30.html", "https://blog.mozilla.org/press/2009/06/mozilla-advances-the-web-with-firefox-3-5/"),
        url_test(
            "/press/mozilla-foundation.html",
            "https://blog.mozilla.org/press/2003/07/mozilla-org-announces-launch-of-the-mozilla-foundation-to-lead-open-source-browser-efforts/",
        ),
        url_test("/press/mozilla1.0.html", "https://blog.mozilla.org/press/2002/06/mozilla-org-launches-mozilla-1-0/"),
        url_test(
            "/press/open-source-security.html",
            "https://blog.mozilla.org/press/2000/01/open-source-development-of-security-products-possible"
            "-worldwide-enhancing-security-and-privacy-for-e-commerce-and-communication/",
        ),
        # Bug 608370, 957664
        url_test("/press/kit{.html,s/}", "https://blog.mozilla.org/press/kits/"),
        # bug 957637
        url_test("/sopa/", "https://blog.mozilla.org/blog/2012/01/19/firefox-users-engage-congress-sopa-strike-stats/"),
        # bug 675031
        url_test(
            "/projects/fennec/is/a/pretty/fox.html",
            "http://website-archive.mozilla.org/www.mozilla.org/fennec_releasenotes/projects/fennec/is/a/pretty/fox.html",
        ),
        # bug 924687, issue 10736
        url_test("/opportunities{,/,/index.html}", "/careers/"),
        # bug 884933
        url_test("/{m,{firefox/,}mobile}/platforms/", "https://support.mozilla.org/kb/will-firefox-work-my-mobile-device"),
        url_test("/m/", "/firefox/new/"),
        # bug 876581
        url_test("/firefox/phishing-protection/", "https://support.mozilla.org/kb/how-does-phishing-and-malware-protection-work"),
        # bug 1006079
        url_test("/mobile/home/{,index.html}", "https://blog.mozilla.org/services/2012/08/31/retiring-firefox-home/"),
        # bug 949562
        url_test(
            "/mobile/home/1.0/releasenotes/{,index.html}",
            "http://website-archive.mozilla.org/www.mozilla.org/firefox_home/mobile/home/1.0/releasenotes/",
        ),
        url_test(
            "/mobile/home/1.0.2/releasenotes/{,index.html}",
            "http://website-archive.mozilla.org/www.mozilla.org/firefox_home/mobile/home/1.0.2/releasenotes/",
        ),
        url_test("/mobile/home/faq/{,index.html}", "http://website-archive.mozilla.org/www.mozilla.org/firefox_home/mobile/home/faq/"),
        # bug 960064
        url_test("/firefox/vpat-1.5.html", "http://website-archive.mozilla.org/www.mozilla.org/firefox_vpat/firefox-vpat-1.5.html"),
        url_test("/firefox/vpat.html", "http://website-archive.mozilla.org/www.mozilla.org/firefox_vpat/firefox-vpat-3.html"),
        # bug 1068931
        url_test("/advocacy/", "https://advocacy.mozilla.org/"),
        # bug 887426
        url_test("/about/policies/", "/about/governance/policies/"),
        url_test("/about/policies/participation.html", "/about/governance/policies/participation/"),
        url_test("/about/policies/policies.html", "/about/governance/policies/"),
        # bug 882923
        url_test("/opt-out.html", "/privacy/websites/#user-choices"),
        # bug 818321
        url_test("/projects/security/tld-idn-policy-list.html", "https://wiki.mozilla.org/IDN_Display_Algorithm"),
        url_test("/projects/security/membership-policy.html", "/about/governance/policies/security-group/membership/"),
        url_test("/projects/security/secgrouplist.html", "/about/governance/policies/security-group/"),
        url_test("/projects/security/security-bugs-policy.html", "/about/governance/policies/security-group/bugs/"),
        # bug 818316, 1128579
        url_test("/projects/security/certs/", "/about/governance/policies/security-group/certs/"),
        url_test("/projects/security/certs/included/", "https://wiki.mozilla.org/CA:IncludedCAs"),
        url_test("/projects/security/certs/pending/", "https://wiki.mozilla.org/CA:PendingCAs"),
        url_test("/about/governance/policies/security-group/certs/included/", "https://wiki.mozilla.org/CA:IncludedCAs"),
        url_test("/about/governance/policies/security-group/certs/pending/", "https://wiki.mozilla.org/CA:PendingCAs"),
        url_test("/projects/security/certs/policy/", "/about/governance/policies/security-group/certs/policy/"),
        url_test("/projects/security/certs/policy/EnforcementPolicy.html", "/about/governance/policies/security-group/certs/policy/enforcement/"),
        url_test("/projects/security/certs/policy/MaintenancePolicy.html", "/about/governance/policies/security-group/certs/policy/maintenance/"),
        url_test("/projects/security/certs/policy/InclusionPolicy.html", "/about/governance/policies/security-group/certs/policy/inclusion/"),
        # bug 926629
        url_test("/newsletter/about_mobile/", "/newsletter/"),
        url_test("/newsletter/about_mozilla/", "/contribute/"),
        url_test("/newsletter/new/", "/newsletter/"),
        # bug 1238458
        # issue 14141
        url_test("/firefox/browsers/mobile/compare", "/firefox/browsers/mobile/"),
        url_test("/newsletter/ios/", "/firefox/browsers/mobile/ios/"),
        # bug 818323
        url_test("/projects/security/known-vulnerabilities.html", "/security/known-vulnerabilities/"),
        url_test("/projects/security/older-vulnerabilities.html", "/security/known-vulnerabilities/older-vulnerabilities/"),
        # bug 1017564
        url_test("/mobile/RANDOM-STUFF/system-requirements/", "https://support.mozilla.org/kb/will-firefox-work-my-mobile-device"),
        # bug 1041712, 1069335, 1069902
        url_test(
            "/{firefox,mobile}/{2,19,27}.0{a2,beta,.2}/{release,aurora}notes/{,stuff}",
            "http://website-archive.mozilla.org/www.mozilla.org/firefox_releasenotes/en-US"
            "/{firefox,mobile}/{2,19,27}.0{a2,beta,.2}/{release,aurora}notes/{,stuff}",
        ),
        # bug 1090468
        url_test(
            "/security/{older-alerts,security-announcement,phishing-test{,-results}}.html",
            "http://website-archive.mozilla.org/www.mozilla.org/security/security/{older-alerts,security-announcement,phishing-test{,-results}}.html",
        ),
        url_test(
            "/security/iSECPartners_Phishing.pdf", "http://website-archive.mozilla.org/www.mozilla.org/security/security/iSECPartners_Phishing.pdf"
        ),
        # bug 878039
        url_test("/access/", "https://developer.mozilla.org/docs/Web/Accessibility"),
        url_test("/access/architecture.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_architecture"),
        url_test("/access/at-vendors.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_Assistive_Technology_Vendors"),
        url_test("/access/authors.html", "https://developer.mozilla.org/docs/Web/Accessibility/Information_for_Web_authors"),
        url_test(
            "/access/core-developers.html",
            "https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_Information_for_Core_Gecko_Developer",
        ),
        url_test(
            "/access/evaluators.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_Governments_and_Other_Organization"
        ),
        url_test("/access/event-flow.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Event_Process_Procedure"),
        url_test(
            "/access/external-developers.html",
            "https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_External_Developers_Dealing_with_A#community",
        ),
        url_test("/access/features.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_Features_in_Firefox"),
        url_test("/access/highlevel.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/CSUN_Firefox_Materials"),
        url_test(
            "/access/platform-apis.html",
            "https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_API_cross-reference#Accessible_Roles",
        ),
        url_test("/access/plugins-work.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Mozilla_Plugin_Accessibility"),
        url_test("/access/prefs-and-apis.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Embedding_API_for_Accessibility"),
        url_test("/access/resources.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Links_and_Resources"),
        url_test("/access/section508.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Mozilla_s_Section_508_Compliance"),
        url_test("/access/today.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Software_accessibility_today"),
        url_test(
            "/access/toolkit-checklist.html",
            "https://developer.mozilla.org/docs/Mozilla/Accessibility/What_needs_to_be_done_when_building_new_toolkits",
        ),
        url_test("/access/ui-developers.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_information_for_UI_designers"),
        url_test("/access/users.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_users"),
        url_test("/access/w3c-uaag.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/UAAG_evaluation_report"),
        url_test("/access/w4a.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/W4A"),
        url_test(
            "/access/windows/at-apis.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/Gecko_info_for_Windows_accessibility_vendors"
        ),
        url_test("/access/windows/msaa-server.html", "https://developer.mozilla.org/docs/Web/Accessibility/Implementing_MSAA_server"),
        url_test("/access/windows/zoomtext.html", "https://developer.mozilla.org/docs/Mozilla/Accessibility/ZoomText"),
        # bug 1148187
        url_test("/access/unix.html", "http://website-archive.mozilla.org/www.mozilla.org/access/access/unix.html"),
        # bug 1216953
        url_test("/MPL/MPL-1.0.html", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/1.0/"),
        url_test("/MPL/MPL-1.1.html", "/MPL/1.1/"),
        # bug 987852
        url_test("/MPL/0.95/stuff.html", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/0.95/stuff.html"),
        url_test("/MPL/1.0/stuff.html", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/1.0/stuff.html"),
        url_test("/MPL/2.0/process/stuff.html", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/2.0/process/stuff.html"),
        url_test("/MPL/NPL/stuff.html", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/NPL/stuff.html"),
        url_test("/MPL/boilerplate-1.1/stuff.html", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/boilerplate-1.1/stuff.html"),
        url_test("/MPL/missing.html", "http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/missing.html"),
        # bug 858315
        url_test("/projects/devpreview/firstrun/", "/firefox/firstrun/"),
        url_test(
            "/projects/devpreview/stuff.html",
            "http://website-archive.mozilla.org/www.mozilla.org/devpreview_releasenotes/projects/devpreview/stuff.html",
        ),
        # bug 947890, 1069902
        url_test(
            "/firefox/releases/{0.9.1,1.5.0.1}.html",
            "http://website-archive.mozilla.org/www.mozilla.org/firefox_releasenotes/en-US/firefox/releases/{0.9.1,1.5.0.1}.html",
        ),
        url_test(
            "/{firefox,mobile}/{2,9,18,25}.0/releasenotes/",
            "http://website-archive.mozilla.org/www.mozilla.org/firefox_releasenotes/en-US/{firefox,mobile}/{2,9,18,25}.0/releasenotes/",
        ),
        # bug 988746, 989423, 994186, 1153351
        url_test("/mobile/{23,28,29}.0/releasenotes/", "/firefox/android/{23,28,29}.0/releasenotes/"),
        url_test("/mobile/{3,4}2.0beta/{aurora,release}notes/", "/firefox/android/{3,4}2.0beta/{aurora,release}notes/"),
        # bug 724682
        url_test("/projects/mathml/demo/texvsmml.html", "https://developer.mozilla.org/docs/Mozilla_MathML_Project/MathML_Torture_Test"),
        url_test("/projects/mathml/{,demo/}", "https://developer.mozilla.org/en-US/docs/Mozilla/MathML_Project"),
        url_test("/projects/mathml/fonts/", "https://developer.mozilla.org/Mozilla_MathML_Project/Fonts"),
        url_test("/projects/mathml/screenshots/", "https://developer.mozilla.org/Mozilla_MathML_Project/Screenshots"),
        # bug 961010
        url_test("/mobile/credits/credits-people-list.html", "/credits/"),
        url_test("/fennec/", "/firefox/new/"),
        # issue 8749
        url_test("/mobile/", "/firefox/browsers/mobile/"),
        # bug 876668
        url_test("/mobile/customize/", "/firefox/browsers/mobile/"),
        # bug 736934, 860865, 1101220, 1153351
        url_test("/mobile/{{beta,aurora}/,}notes/", "/firefox/android/{{beta,aurora}/,}notes/"),
        url_test("/firefox/{{beta,aurora,organizations}/,}system-requirements.html", "/firefox/{{beta,aurora,organizations}/,}system-requirements/"),
        # bug 897082
        url_test("/about/mozilla-spaces/stuff.html", "/contact/spaces/"),
        url_test("/about/contact/stuff.html", "/contact/spaces/"),
        url_test("/contribute/local/", "/contact/communities/"),
        url_test("/contribute/local/northamerica.html", "/contact/communities/north-america/"),
        url_test("/contribute/local/europe.html", "/contact/communities/europe/"),
        url_test("/contribute/local/latinamerica.html", "/contact/communities/latin-america/"),
        url_test("/contribute/local/africamideast.html", "/contact/communities/africa-middle-east/"),
        url_test("/contribute/local/asia.html", "/contact/communities/asia-south-pacific/"),
        url_test("/contribute/local/southpole.html", "/contact/communities/antarctica/"),
        # bug 1393622
        url_test("/contact/spaces/{auckland,tokyo}/", "/contact/spaces/"),
        # bug 875052
        url_test("/about/get-involved/whanot/", "/contribute/"),
        # bug 1155870
        url_test("/firefox/os/{releases,notes}/", "https://developer.mozilla.org/Firefox_OS/Releases"),
        url_test("/firefox/os/{release,}notes/2.0/", "https://developer.mozilla.org/Firefox_OS/Releases/2.0"),
        # bug 878871
        url_test("/firefoxos/is.great/", "/firefox/os/"),
        # bug 831810 & 1142583, 1329931
        url_test("/{mwc,MWC}/", "https://support.mozilla.org/products/firefox-os"),
        # bug 878926
        url_test("/{de/,}firefoxflicks/{,stuff}", "https://firefoxflicks.mozilla.org/{de/,}{,stuff}"),
        # bug 849426
        url_test("/about/history.html", "/about/history/"),
        url_test("/about/bookmarks.html", "https://wiki.mozilla.org/Historical_Documents"),
        url_test("/about/timeline.html", "https://wiki.mozilla.org/Timeline"),
        # bug 1016400, issue 10736
        url_test("/about/careers.html", "/careers/"),
        # bug 861243 and bug 869489
        url_test("/about/manifesto.html", "/about/manifesto/"),
        url_test("/about/manifesto.{de,pt-BR}.html", "/{de,pt-BR}/about/manifesto/"),
        # bug 856077
        url_test("/projects/toolkit/", "https://developer.mozilla.org/docs/Toolkit_API"),
        # bug 877165
        url_test("/firefox/connect/random/stuff", "/"),
        # bug 657049, 1238851
        url_test("/firefox/accountmanager/", "https://developer.mozilla.org/Persona"),
        url_test("/persona{/{about,developer-faq}/,}", "https://developer.mozilla.org/Persona"),
        # bug 1209720
        url_test("/thunderbird/releasenotes/thunderbird/notes/"),
        url_test("/rhino/download.html", "https://developer.mozilla.org/docs/Mozilla/Projects/Rhino/Download_Rhino"),
        url_test("/rhino/doc.html", "https://developer.mozilla.org/docs/Mozilla/Projects/Rhino/Documentation"),
        url_test("/rhino/shell.html", "https://developer.mozilla.org/docs/Mozilla/Projects/Rhino/Shell"),
        url_test("/rhino/{,random/stuff}", "https://developer.mozilla.org/docs/Mozilla/Projects/Rhino"),
        # Bug 730488 deprecate /firefox/all-older.html
        url_test("/firefox/all-older.html", "/firefox/new/"),
        # Bug 1209643
        url_test("/legal/bylaws_amendment_1.html", "/foundation/documents/bylaws-amendment-1/"),
        url_test("/legal/bylaws_amendment_2.html", "/foundation/documents/bylaws-amendment-2/"),
        url_test("/legal/articles.html", "/foundation/documents/articles-of-incorporation/"),
        url_test("/legal/amendment.html", "/foundation/documents/articles-of-incorporation/amendment/"),
        url_test("/legal/bylaws.html", "/foundation/documents/bylaws/"),
        # bug 1211907
        url_test("/firefox/independent", "/firefox/new/"),
        url_test("/firefox/personal", "/firefox/new/"),
        # bug 960689, 896474
        url_test("/about/legal.html", "/about/legal/"),
        # bug 1243240
        url_test("/about/legal/report-abuse/", "/about/legal/report-infringement/"),
        # bug 846362
        url_test("/community/{index{.{de,fr},}.html,}", "/contribute/"),
        # bug 1003703, 1009630
        url_test(
            "/firefox/42.0/firstrun/eu/",
            "/firefox/42.0/firstrun/",
            query={
                "utm_source": "direct",
                "utm_medium": "none",
                "utm_campaign": "redirect",
                "utm_content": "eu-firstrun-redirect",
            },
        ),
        # bug 845983
        url_test("/metrofirefox/random/stuff/", "/firefox/random/stuff/"),
        # bug 860532 - Reidrects for governance pages
        url_test("/about/governance.html", "/about/governance/"),
        url_test("/about/roles.html", "/about/governance/roles/"),
        url_test("/about/organizations.html", "/about/governance/organizations/"),
        # bug 876233
        url_test("/about/participate/", "/contribute/"),
        # bug 790784
        url_test("/{about/policies/,foundation/,}privacy-policy{/,.html,}", "/privacy/websites/"),
        url_test("/privacy-policy.pdf", "https://static.mozilla.com/moco/en-US/pdf/mozilla_privacypolicy.pdf"),
        # bug 1074354
        url_test("/legal/", "/about/legal/"),
        # bug 963816
        url_test("/legal/privacy/", "/privacy/"),
        url_test("/legal/privacy/firefox{/,.html}", "/privacy/firefox/"),
        url_test("/legal/privacy/oct-2006", "/privacy/archive/firefox/2006-10/"),
        url_test("/legal/privacy/june-2008", "/privacy/archive/firefox/2008-06/"),
        url_test("/legal/privacy/jan-2009", "/privacy/archive/firefox/2009-01/"),
        url_test("/legal/privacy/sept-2009", "/privacy/archive/firefox/2009-09/"),
        url_test("/legal/privacy/jan-2010", "/privacy/archive/firefox/2010-01/"),
        url_test("/legal/privacy/dec-2010", "/privacy/archive/firefox/2010-12/"),
        url_test("/legal/privacy/june-2011", "/privacy/archive/firefox/2011-06/"),
        url_test("/legal/privacy/june-2012", "/privacy/archive/firefox/2012-06/"),
        url_test("/legal/privacy/sept-2012", "/privacy/archive/firefox/2012-09/"),
        url_test("/legal/privacy/dec-2012", "/privacy/archive/firefox/2012-12/"),
        url_test("/legal/privacy/firefox-third-party", "/privacy/archive/firefox/third-party/"),
        url_test("/legal/privacy/notices-firefox", "/legal/firefox/"),
        url_test("/privacy/policies/{facebook,firefox-os,websites}/", "/privacy/{facebook,firefox-os,websites}/"),
        # https://github.com/mozilla/bedrock/issues/5745
        url_test("/privacy/firefox-cliqz", "/privacy/archive/firefox-cliqz/2018-06/"),
        # mozilla/bedrock/#11610
        url_test("/privacy/firefox-os/", "/privacy/archive/firefox-os/2022-05/"),
        # bug 1034859
        url_test("/en-US/about/buttons/dude.jpg", "/media/img/careers/buttons/dude.jpg"),
        # bug 1003737
        url_test("/de/impressum/", "/de/about/legal/impressum/", follow_redirects=True),
        # bug 1248393
        url_test("/de/about/legal/impressum/", status_code=requests.codes.ok),
        url_test("/{en-US,fr,ja}/about/legal/impressum/", "/de/about/legal/impressum/", status_code=requests.codes.found),
        # bug 960543
        url_test("/firefox/{2,3}.0/eula/random/stuff/", "/legal/eula/firefox-{2,3}/"),
        # bug 724633 - Porting foundation pages
        # Add redirects for the pdfs that were under /foundation/documents/
        # that will now be served from static.mozilla.com/foundation/documents/
        # (The links within the foundation pages have been updated, but there are
        # probably many links to them from other pages and sites that need to keep
        # working.)
        url_test("/foundation/documents/random-stuff.pdf", "https://static.mozilla.com/foundation/documents/random-stuff.pdf"),
        url_test("/foundation/donate_form.pdf", "https://static.mozilla.com/foundation/documents/donate_form.pdf"),
        # openwebfund/ and openwebfund/index.html redirect to another site.  Careful because
        # there are other pages under openwebfund that still need to be served from Bedrock.
        url_test("/foundation/openwebfund/", "https://foundation.mozilla.org/donate/"),
        url_test("/foundation/donate.html", "https://foundation.mozilla.org/donate/"),
        # FIXUPs for changing foo/bar.html to foo/bar/
        # Redirect foundation/foo.html to foundation/foo/, with a redirect for the nice search engines
        url_test("/foundation/{about,careers,licensing,moco,mocosc}.html", "/foundation/{about,careers,licensing,moco,mocosc}/"),
        # Redirect foundation/anything/foo.html to foundation/anything/foo/,
        # with a redirect for the nice search engines
        url_test(
            "/foundation/{annualreport,documents,feed-icon-guidelines,licensing,openwebfund,trademarks}/random-stuff.html",
            "/foundation/{annualreport,documents,feed-icon-guidelines,licensing,openwebfund,trademarks}/random-stuff/",
        ),
        url_test("/foundation/documents/{index,mozilla-2002-financial-faq}.html", "/foundation/{index,mozilla-2002-financial-faq}/"),
        # bug 442671
        url_test("/foundation/trademarks/l10n-policy/", "/foundation/trademarks/"),
        # Bug 1186373
        url_test(
            "/firefox/hello/npssurvey/", "https://www.surveygizmo.com/s3/2227372/Firefox-Hello-Product-Survey", status_code=requests.codes.found
        ),
        # Bug 1221739
        url_test("/firefox/hello/feedbacksurvey/", "https://www.surveygizmo.com/s3/2319863/d2b7dc4b5687", status_code=requests.codes.found),
        # bug 1236791 - DISABLED for Issue 16355 because the grounds for needing the redirect is no longer valid
        # https://bugzilla.mozilla.org/show_bug.cgi?id=1236791 is 9 years old at the point of this change and looks
        # no longer relevant, so disabling this test is OK.
        # url_test(
        #     "/en-US/firefox/new/?product=firefox-{3.6.8,13.0.1}{&os={osx〈=en-US,win},}",
        #     "https://www.firefox.com?redirect_source=mozilla-org",  # Issue 16355
        #     status_code=301,  # Issue 16355
        # ),
        # bug 1235853
        url_test("/facebookapps/{,downloadtab/}", "/firefox/new/"),
        # bug 1238248
        url_test("/firefox/push/", "https://support.mozilla.org/kb/push-notifications-firefox"),
        # bug 1237875
        url_test("/community/forums/", "/about/forums/"),
        # bug 1238687, 1436740, issue 8375
        url_test("/privacy/you/", "https://foundation.mozilla.org/internet-health/"),
        url_test("/privacy/tips/", "https://foundation.mozilla.org/internet-health/"),
        # bug 1239960, 1329931
        url_test("/firefox/partners/", "https://support.mozilla.org/products/firefox-os"),
        url_test("/b2g/", "https://support.mozilla.org/products/firefox-os"),
        # from mcom-tests
        url_test("/products/", "/en-US/products/", status_code=requests.codes.found),
        url_test("/mobile/37.0{,beta,a2}/releasenotes", "/firefox/android/37.0{,beta,a2}/releasenotes/"),
        url_test("/projects/firefox/3.6.13/whatsnew/", "/firefox/3.6.13/whatsnew/"),
        url_test("/apps/", "https://marketplace.firefox.com/"),
        url_test("/dnt/", "https://support.mozilla.org/kb/how-do-i-turn-do-not-track-feature"),
        url_test("/metrofirefox/", "/firefox/"),
        url_test("/firefox/brand/", "https://mozilla.design/firefox/"),
        # Bug 804810
        url_test("/foundation/identity-guidelines/{,index.html}", "https://mozilla.design/mozilla/"),
        # Bug 1243060
        url_test("/firefox/tiles/", "https://support.mozilla.org/kb/about-tiles-new-tab"),
        # Bug 1252332
        url_test("/sync/", "/firefox/features/sync/"),
        url_test("/projects/bonecho/", "/firefox/channel/desktop/"),
        url_test("/projects/bonsai/", "https://wiki.mozilla.org/Bonsai"),
        url_test("/projects/camino/{,homepage.html}", "http://caminobrowser.org/"),
        url_test("/projects/cck/", "https://wiki.mozilla.org/CCK"),
        url_test("/projects/chimera/", "http://caminobrowser.org/"),
        url_test("/projects/deerpark/", "/firefox/channel/desktop/"),
        url_test("/projects/granparadiso/", "/firefox/channel/desktop/"),
        url_test("/projects/inspector/", "https://developer.mozilla.org/docs/Tools/Add-ons/DOM_Inspector"),
        url_test("/projects/javaconnect/", "http://developer.mozilla.org/en/JavaXPCOM"),
        url_test("/projects/marketing/", "https://wiki.mozilla.org/MarketingGuide"),
        url_test("/projects/minefield/", "/firefox/channel/desktop/"),
        url_test("/projects/minimo/", "https://wiki.mozilla.org/Mobile"),
        url_test("/projects/namoroka/", "/firefox/channel/desktop/"),
        url_test("/projects/nspr/", "https://developer.mozilla.org/docs/NSPR"),
        url_test("/projects/netlib/", "https://developer.mozilla.org/docs/Mozilla/Projects/Necko"),
        url_test("/projects/plugins/", "https://developer.mozilla.org/Add-ons/Plugins"),
        url_test("/projects/rt-messaging/", "http://chatzilla.hacksrus.com/"),
        url_test("/projects/rt-messaging/chatzilla/", "http://chatzilla.hacksrus.com/"),
        url_test("/projects/shiretoko/", "/firefox/channel/desktop/"),
        url_test("/projects/string/", "https://developer.mozilla.org/en/XPCOM_string_guide"),
        url_test("/projects/tech-evangelism/", "https://wiki.mozilla.org/Evangelism"),
        url_test("/projects/venkman/", "https://developer.mozilla.org/docs/Archive/Mozilla/Venkman"),
        url_test("/projects/webservices/examples/babelfish-wsdl/", "https://developer.mozilla.org/docs/SOAP_in_Gecko-based_Browsers"),
        url_test("/projects/xbl/", "https://www.w3.org/TR/xbl/"),
        url_test("/projects/xforms/", "https://wiki.mozilla.org/XForms"),
        url_test("/projects/xpcom/", "https://developer.mozilla.org/docs/Mozilla/Tech/XPCOM"),
        url_test("/projects/xpinstall/", "https://developer.mozilla.org/docs/Archive/Mozilla/XPInstall"),
        url_test("/projects/xslt/", "https://developer.mozilla.org/docs/Web/XSLT"),
        url_test("/projects/xul/", "https://wiki.mozilla.org/XUL"),
        url_test("/quality/", "http://quality.mozilla.org/"),
        url_test("/quality/help/", "http://quality.mozilla.org/get-involved"),
        # Bug 654614 /blocklist -> addons.m.o/blocked, Issue 14221
        url_test("/blocklist/", "https://addons.mozilla.org/blocked/"),
        url_test("/products/firefox/{,stuff/}", "/products/"),
        # Bug 784411
        url_test("/about/mission/", "/mission/"),
        # Bug 1260423
        url_test("/firefox/choose", "/firefox/new/"),
        url_test("/firefox/{,46.0/,46.0.1/,47.0/,47.0.1/}secondrun", "/firefox/browsers/mobile/"),
        # bug 1288647, 1722760
        url_test("/hacking", "https://firefox-source-docs.mozilla.org/"),
        # issue 10736
        url_test("/jobs", "/careers/"),
        url_test("/join", "/careers/"),
        # Bug 1293539
        url_test("/firefox/{48.0,48.0.1,49.0a1,49.0a2}/tour", "https://support.mozilla.org/kb/get-started-firefox-overview-main-features"),
        url_test("/firefox/tour", "https://support.mozilla.org/kb/get-started-firefox-overview-main-features"),
        # Bug 1262593
        url_test("/unix/remote.html", "http://www-archive.mozilla.org/unix/remote.html"),
        # Bug 1313023
        url_test("/story", "https://foundation.mozilla.org/donate/"),
        # Bug 1277196
        url_test(
            "/firefox/firstrun/learnmore",
            "/firefox/features/?utm_campaign=redirect&utm_medium=firefox-browser&utm_source=firefox-browser&utm_content=learnmore-tab",
        ),
        url_test(
            "/firefox/{49.0,49.0.1,50.0a1,51.0a2}/firstrun/learnmore",
            "/firefox/features/?utm_campaign=redirect&utm_medium=firefox-browser&utm_source=firefox-browser&utm_content=learnmore-tab",
        ),
        url_test(
            "/firefox/windows-10/welcome",
            "https://support.mozilla.org/kb/how-change-your-default-browser-windows-10?utm_campaign=redirect"
            "&utm_medium=firefox-browser&utm_source=firefox-browser&utm_content=windows10-welcome-tab",
        ),
        # bug 1319207
        url_test("/de/privacy/firefox-focus/", "/de/privacy/firefox-klar/"),
        url_test("/fr/privacy/firefox-klar/", "/fr/privacy/firefox-focus/"),
        url_test("/es-ES/privacy/firefox-klar/", "/es-ES/privacy/firefox-focus/"),
        # Bug 1317260
        url_test(
            "/about/governance/policies/security-group/certs/policy/{inclusion,maintenance,enforcement}/",
            "/about/governance/policies/security-group/certs/policy/#{inclusion,maintenance,enforcement}",
        ),
        # Bug 936362
        # only upper-case for XBL. /xbl is a namespace URL for the standard.
        url_test("/XBL", "https://www.w3.org/TR/xbl/"),
        url_test("/xbl", status_code=200),
        url_test("/RDF", "https://www.w3.org/RDF/"),
        url_test("/rdf", "https://www.w3.org/RDF/"),
        # Bug 1332008, 1525853
        url_test("{/en-US,}/protocol/", "https://protocol.mozilla.org"),
        # Bug 1322959, issue 8375
        url_test("/onlineprivacy", "https://foundation.mozilla.org/internet-health/"),
        # Bug 1335569, issue 8375
        url_test("/digital-inclusion", "https://foundation.mozilla.org/internet-health/"),
        # Bug 1333146
        url_test("/internet-health-report", "https://internethealthreport.org/"),
        url_test("/internethealthreport/", "https://internethealthreport.org/"),
        # Bug 1335569, issue 8375
        url_test("/open-innovation", "https://foundation.mozilla.org/internet-health/"),
        # Bug 1335040
        url_test("/gigabit/{,apply/}", "https://wiki.mozilla.org/Gigabit"),
        # Bug 1329931
        url_test("/firefox/os/{,devices/}", "https://support.mozilla.org/products/firefox-os"),
        # Bug 1324504
        url_test("/contribute/studentambassadors/{,join/,thanks/}", "/contribute/"),
        # Bug 1340600, Issue 7840
        url_test(
            "/css-grid",
            "https://developer.mozilla.org/docs/Learn/CSS/CSS_layout/Grids",
            query={
                "utm_source": "redirect",
                "utm_medium": "collateral",
                "utm_campaign": "css-grid",
            },
        ),
        # Bug 1361194, issue 8375
        url_test("/internethealth", "https://foundation.mozilla.org/internet-health/"),
        # Bug 1384370
        url_test("/developers", "https://developer.mozilla.com/"),
        # Bug 1369732
        url_test("/en-US/Firefox", "https://www.firefox.com/en-US/"),
        url_test("/Firefox", "https://www.firefox.com/"),
        # Bug 1380845
        url_test("/persona/privacy-policy/", "/privacy/archive/persona/2017-07/"),
        url_test("/persona/terms-of-service/", "/privacy/archive/persona/2017-07/#terms-of-service"),
        # Bug 1386112
        url_test("/firefox/android/faq/", "https://support.mozilla.org/products/mobile"),
        # bug 1392796
        url_test("/firefox/desktop/fast/", "/firefox/features/fast/"),
        url_test("/firefox/desktop/trust/", "/firefox/features/private/"),
        url_test("/firefox/desktop/tips/", "/firefox/features/tips/"),
        url_test("/firefox/desktop/customize/", "https://support.mozilla.org/kb/customize-firefox-controls-buttons-and-toolbars"),
        url_test("/firefox/private-browsing/", "/firefox/features/private-browsing/"),
        # bug 1405436
        url_test("/legal/eula/firefox.html", "/about/legal/terms/firefox/"),
        url_test("/firefox/organic/", "/firefox/"),
        url_test("/firefox/landing/better/", "/firefox/"),
        url_test("/firefox/{new/,}addons/", "https://addons.mozilla.org"),
        url_test("/firefox/tips/", "/firefox/features/tips/"),
        url_test("/firefox/new/en", "/firefox/new/"),
        # These are a wordpress artifact and result in a Left to Right Mark unicode control character
        # https://en.wikipedia.org/wiki/Left-to-right_mark
        url_test("/firefox/%E2%80%8E", "/firefox/"),
        url_test("/firefox/new/%E2%80%8E", "/firefox/new/"),
        url_test("/firefox/38.0.3/releasenotes/", "/firefox/38.0.5/releasenotes/"),
        url_test("/firefox/)", "/firefox/"),
        url_test("/firefox/{new,developer}/)", "/firefox/{new,developer}/"),
        url_test("/firefox/default.htm", "/firefox/"),
        url_test("/firefox/fx/dude", "/firefox/new/"),
        url_test("/firefox/android/45.0", "/firefox/android/45.0/releasenotes/"),
        url_test("/firefox/stats/", "/firefox/"),
        # bug 1416706
        url_test("/firefox/desktop/", "/firefox/new/"),
        # issue 9502
        url_test("/firefox/quantum/", "/firefox/browsers/quantum/"),
        # bug 1421584, issue 7491
        url_test("/firefox/organizations/faq/", "/firefox/enterprise/"),
        # bug 1425865
        url_test("/firefox/fire-tv/", "https://support.mozilla.org/products/firefox-fire-tv/", status_code=302),
        # bug 1421584
        url_test("/firefox/interest-dashboard/", "https://support.mozilla.org/kb/firefox-add-technology-modernizing"),
        # bug 1419244
        url_test("/firefox/mobile-download/{,desktop/}", "/firefox/browsers/mobile/"),
        # Bug 1438464
        url_test("/collusion/", "https://github.com/mozilla/lightbeam-we"),
        url_test("/lightbeam/{,about/}?", "https://github.com/mozilla/lightbeam-we"),
        # Bug 1428150
        url_test("/tabzilla/media/css/tabzilla.css", "https://mozorg.cdn.mozilla.net/media/css/tabzilla-min.css"),
        # bug 960651, 1436973
        url_test("/{firefox,mobile}/{5.0,5.0.1,4.0beta,latest}/details/{,index.html,from-3.6.html}", "/firefox/unsupported-systems/"),
        url_test("/firefox/unsupported/{,warning/,details/,EOL/,mac/,win/}", "/firefox/unsupported-systems/"),
        # Bug 1428783
        url_test("/firefox/dnt/", "https://support.mozilla.org/kb/how-do-i-turn-do-not-track-feature"),
        # Bug 1430887
        url_test("/firefox/geolocation/", "https://support.mozilla.org/kb/does-firefox-share-my-location-web-sites"),
        # bug 1422080, 1013349, 1233015
        url_test("/about/partnerships.html", "/contact/"),
        url_test("/about/partnerships/{,contentservices/}", "/contact/"),
        # Bug 1436740, issue 8375
        url_test("/teach/{,smarton/}", "https://foundation.mozilla.org/internet-health/"),
        url_test("/teach/smarton/{tracking,security,surveillance}/", "https://foundation.mozilla.org/internet-health/"),
        # Issue #5949
        url_test("/foundation/trademarks/", "/foundation/trademarks/policy/"),
        url_test("/foundation/trademarks/faq/", "/foundation/trademarks/policy/"),
        url_test("/foundation/documents/domain-name-license.pdf", "/foundation/trademarks/policy/"),
        url_test("/about/partnerships/distribution/", "/foundation/trademarks/distribution-policy/"),
        url_test("/foundation/trademarks/poweredby/faq/", "/foundation/trademarks/policy/"),
        url_test("/foundation/trademarks/l10n-website-policy/", "/foundation/trademarks/policy/"),
        # Issue 6209
        url_test("/pocket/", "https://getpocket.com/"),
        # issue 16358
        url_test("/firefox/pocket/", "https://getpocket.com/"),
        # Issue 6476
        url_test("/foundation/", "https://foundation.mozilla.org/"),
        url_test("/foundation/about/", "https://foundation.mozilla.org/about/"),
        url_test("/foundation/documents/", "https://foundation.mozilla.org/about/public-records/"),
        url_test("/foundation/issues/", "https://foundation.mozilla.org/initiatives/"),
        url_test("/foundation/leadership-network/", "https://foundation.mozilla.org/"),
        url_test("/foundation/advocacy/", "https://foundation.mozilla.org/"),
        # Issue 6979
        url_test("/firefoxfightsforyou/", "/firefox/new/"),
        # Issue 6994
        url_test("/contribute/signup/", "/contribute/"),
        url_test("/contribute/task/{,devtools-challenger/, firefox-mobile/}", "/contribute/"),
        url_test("/contribute/friends/", "/contribute/"),
        # Issue 7287
        url_test("/accounts/", "/account/"),
        # Issue 14230
        url_test("/firefox/accounts/", "/account/"),
        url_test("/firefox/account/", "/account/"),
        # Issue 7435
        url_test("/about/history/details/", "/about/history/"),
        # Issue 7436
        url_test("/firefox/feedback/", "https://support.mozilla.org/questions/new/desktop"),
        # Issue 7491
        url_test("/firefox/organizations/", "/firefox/enterprise/"),
        # Issue 7670
        url_test("/firefox/fights-for-you/", "/firefox/new/"),
        # Issue 7842
        url_test("/enterprise/", "/firefox/enterprise/"),
        # Issue 7970
        url_test("/moss/mission-partners-india/", "/moss/mission-partners/"),
        # Issue 7983, 14248
        url_test("/privacy/products/", "/privacy/"),
        # Issue #8206
        url_test("/firefox/{69.0/,69.0.1/,69.0a2/,69.0.1a1/,}tracking-protection/start/", "https://support.mozilla.org/kb/tracking-protection"),
        url_test("/firefox/{69.0/,69.0.1/,69.0a2/,69.0.1a1/,}content-blocking/start/", "https://support.mozilla.org/kb/content-blocking"),
        # Issue 7840
        url_test("/developer/", "https://developer.mozilla.com/"),
        url_test("/developer/browsertest/", "https://developer.mozilla.org/docs/Learn/Tools_and_testing/Cross_browser_testing/Automated_testing"),
        url_test("/developer/css-grid/", "https://developer.mozilla.org/docs/Learn/CSS/CSS_layout/Grids"),
        # Issue 6461
        url_test("/contribute/events/", "https://community.mozilla.org/events/"),
        # issue 8596
        url_test("/firefox/xr/", "https://support.mozilla.org/kb/webxr-permission-info-page"),
        # bug 1404926, Issue 8418
        url_test("/styleguide/identity/firefox-family/{,overview/}", "https://mozilla.design/firefox/"),
        url_test("/styleguide/identity/firefox/branding/", "https://mozilla.design/firefox/"),
        url_test("/styleguide/identity/firefox/channels/", "https://mozilla.design/firefox/"),
        url_test("/styleguide/identity/firefox/color/", "https://mozilla.design/firefox/"),
        # Bug 1255785, Issue 8418
        url_test("/styleguide/identity/mozilla/logo-prototype/", "https://mozilla.design/mozilla/"),
        # Bug 1268847, Issue 8418
        url_test("/styleguide/websites/sandstone/buttons/", "https://mozilla.design/"),
        url_test("/styleguide/websites/sandstone/forms/", "https://mozilla.design/"),
        url_test("/styleguide/websites/sandstone/tabzilla/", "https://mozilla.design/"),
        # Bug 1365076, Issue 8418
        url_test("/styleguide/identity/mozilla/branding/", "https://mozilla.design/mozilla/"),
        url_test("/styleguide/identity/mozilla/color/", "https://mozilla.design/mozilla/"),
        # Bug 1329931, Issue 8418
        url_test("/styleguide/products/firefox-os/{,subpages/}", "https://mozilla.design/firefox/"),
        # Bug 1329931 & 1342043, Issue 8418
        url_test("/styleguide/identity/firefoxos/{,subpages/}", "https://mozilla.design/firefox/"),
        # Bug 1433749, Issue 8418
        url_test("/styleguide/identity/firefox/branding/", "https://mozilla.design/firefox/"),
        url_test("/styleguide/websites/sandstone/buttons/", "https://mozilla.design/"),
        # Issue 8418
        url_test("/styleguide/", "https://mozilla.design/"),
        # Issue 8644, 8932, 15613
        url_test("/builders{,/}", "https://builders.mozilla.org/"),
        # Issue 6824, 14364
        url_test("/technology/", "https://future.mozilla.org/"),
        # Issue 8419
        url_test("/firefox/this-browser-comes-highly-recommended/", "/firefox/developer/"),
        # Issue 8420
        url_test("/firefox/dedicated-profiles/", "https://support.mozilla.org/kb/dedicated-profiles-firefox-installation"),
        # Issue 8668
        url_test("/contact/communities/{,north-america/,canada/}", "https://community.mozilla.org/groups/"),
        # Issue 8641
        url_test("/technology/what-is-a-browser/", "/firefox/browsers/what-is-a-browser/"),
        url_test("/technology/update-your-browser/", "/firefox/browsers/update-your-browser/"),
        url_test("/technology/incognito-browser/", "/firefox/browsers/incognito-browser/"),
        url_test("/technology/browser-history/", "/firefox/browsers/browser-history/"),
        url_test("/firefox/windows-64-bit/", "/firefox/browsers/windows-64-bit/"),
        url_test("/firefox/best-browser/", "/firefox/browsers/best-browser/"),
        # Issue 8536, 11891
        url_test("/etc/firefox/retention/{thank-you-a/,thank-you-b/,thank-you-referral/}", "/firefox/new/"),
        url_test("/firefox/retention/thank-you/", "/firefox/new/"),
        # Issue 8374
        url_test("/plugincheck/", "https://support.mozilla.org/kb/npapi-plugins/"),
        url_test("/ekr/", "https://blog.mozilla.org/blog/author/ekrmozilla-com/"),
        # Issue 6994
        url_test("/contribute/stories/", "/contribute/"),
        url_test("/contribute/stories/faye/", "/contribute/"),
        url_test("/contribute/stories/michael/", "/contribute/"),
        url_test("/contribute/stories/ruben/", "/contribute/"),
        url_test("/contribute/stories/shreyas/", "/contribute/"),
        # Issue 8375
        url_test("/internet-health/{,privacy-security/}", "https://foundation.mozilla.org/internet-health/"),
        # Issue 8949
        url_test("/donate/", "https://foundation.mozilla.org/donate/"),
        url_test("/about/governance/policies/security/plugin-whitelist-policy/", "https://wiki.mozilla.org/Plugins/Firefox_Whitelist"),
        url_test("/about/governance/policies/security-group/tld-idn/", "https://wiki.mozilla.org/IDN_Display_Algorithm"),
        # Unfck campaign, issue 11613
        url_test("/firefox/{unfck,unfuck,love,liebe,rendonslenetplusnet}/", "/firefox/new/"),
        url_test("/{unfck,unfuck,love,liebe,rendonslenetplusnet}/", "/firefox/new/"),
        # issue 9148
        url_test("/firefox/campaign/", "/firefox/new/"),
        # Issue 9560
        url_test(
            "/openletter/",
            "https://foundation.mozilla.org/en/campaigns/sign-letter-AICOA/",
            query={
                "utm_campaign": "2022antitrust",
                "utm_content": "shortlink",
                "utm_medium": "print",
                "utm_source": "washingtonpost",
            },
        ),
        # Bug 1673476
        url_test("/about/governance/policies/security-group/certs/", "https://wiki.mozilla.org/CA"),
        # Issue 9788
        url_test("/firefox/enterprise/signup/{,thanks/}", "/firefox/enterprise/"),
        # Issue 9254
        url_test("/grants/{,reports/gnome-haeger-report,jambu.html}/", "/moss/"),
        # Issue 10292
        url_test("/firefox/90.0/whatsnew/africa/", "/firefox/90.0/whatsnew/"),
        url_test("/firefox/90.0/whatsnew/africa/", "/firefox/90.0/whatsnew/"),
        url_test("/firefox/90.0/whatsnew/india/", "/firefox/90.0/whatsnew/"),
        url_test("/firefox/92.0/whatsnew/france/", "/firefox/92.0/whatsnew/"),
        url_test("/firefox/92.0/whatsnew/en/", "/firefox/92.0/whatsnew/"),
        url_test("/firefox/whatsnew/africa/", "/firefox/whatsnew/"),
        url_test("/firefox/whatsnew/india/", "/firefox/whatsnew/"),
        url_test("/firefox/whatsnew/france/", "/firefox/whatsnew/"),
        url_test("/firefox/whatsnew/en/", "/firefox/whatsnew/"),
        # Issue 10590
        url_test("/firefox/whatsnew/all/", "/firefox/whatsnew/"),
        url_test("/firefox/whatsnew/china/", "/firefox/whatsnew/"),
        url_test("/firefox/93.0/whatsnew/all/", "/firefox/93.0/whatsnew/"),
        url_test("/firefox/93.0a2/whatsnew/all/", "/firefox/93.0a2/whatsnew/"),
        url_test("/firefox/93.0/whatsnew/china/", "/firefox/93.0/whatsnew/"),
        url_test("/firefox/93.0a1/whatsnew/china/", "/firefox/93.0a1/whatsnew/"),
        # Issue 10335
        url_test("/vpn/", "/products/vpn/"),
        # issue 10703
        url_test("/firefox/lockwise/", "https://support.mozilla.org/kb/end-of-support-firefox-lockwise"),
        # issue 12107
        url_test("/firefox/families/", "/firefox/family/"),
        # issue 10879
        url_test("/exp/", "/"),
        # issue 11092, issue 12156
        url_test("/about/legal/terms/{mozilla-vpn,vpn,firefox-relay}/", "/about/legal/terms/subscription-services/"),
        # issue 12156
        url_test("/privacy/{mozilla-vpn,firefox-relay}/", "/privacy/subscription-services/"),
        # Issue 11204
        url_test("/{truecolors,truecolours,turningred}/", "/firefox/new/"),
        url_test(
            "/{truecolors,truecolours,turningred}/?utm_source=dude",
            "/firefox/new/",
            query={
                "utm_source": "dude",
            },
        ),
        # Issue 11991
        url_test("/transparency/", "/about/policy/transparency/"),
        # Issue 12376
        url_test("/newsletter/country/success/", "/newsletter/updated/"),
        url_test("/careers/internships/", "/careers/", status_code=requests.codes.found),
        # Issue 12563
        url_test("/exp/firefox/", "/firefox/new/"),
        url_test("/exp/firefox/new/", "/firefox/new/"),
        url_test("/exp/firefox/accounts/", "/account/"),
        url_test("/exp/opt-out/", "https://www.convert.com/opt-out/"),
        # issue 12935
        url_test("/privacy/facebook/", "/privacy/archive/facebook/2023-04/"),
        # Issue 11875 - Adding VPN download pages
        url_test("/vpn/download/", "/products/vpn/download/"),
        url_test("/vpn/download/windows/", "/products/vpn/download/windows/thanks/"),
        url_test("/vpn/download/mac/", "/products/vpn/download/mac/thanks/"),
        # Issue 13272
        url_test("/about/legal/terms/firefox-private-network/", "/privacy/archive/firefox-private-network/tos-2023-06/"),
        url_test("/privacy/firefox-private-network/", "/privacy/archive/firefox-private-network/notice-2023-06/"),
        url_test("/privacy/betterweb/", "/privacy/archive/firefox-betterweb/2023-06/"),
        url_test("/privacy/firefox-fire-tv/", "/privacy/archive/firefox-fire-tv/2023-06/"),
        url_test("/privacy/firefox-reality/", "/privacy/archive/firefox-reality/notice-2023-06/"),
        url_test("/about/legal/terms/firefox-reality/", "/privacy/archive/firefox-reality/tos-2023-06/"),
        # Issue 13672
        url_test("/VendorDPA/", "https://assets.mozilla.net/pdf/VendorDPA.pdf"),
        url_test("/vendordpa/", "https://assets.mozilla.net/pdf/VendorDPA.pdf"),
        # Issue 13732
        url_test("/firefox/welcome/3/", "/account/"),
        url_test("/firefox/mobile/get-app/", "/firefox/browsers/mobile/get-app/"),
        url_test("/contact/spaces/paris/", "/contact/spaces/"),
        # Issue 14245
        url_test("/contact/spaces/berlin/", "/contact/spaces/"),
        url_test("/contact/spaces/beijing/", "/contact/spaces/"),
        url_test("/contact/spaces/san-francisco/", "/contact/spaces/"),
        url_test("/contact/spaces/toronto/", "/contact/spaces/"),
        # Issue 13924
        url_test("/foundation/annualreport/2022/", "https://stateof.mozilla.org/"),
        # Issue 14186
        url_test("/privacy/firefox-monitor/", "/privacy/subscription-services/"),
        # Issue 14172
        url_test(
            "/firefox/browsers/mobile/app/?product=firefox",
            "https://play.google.com/store/apps/details?id=org.mozilla.firefox",
            req_headers=UA_ANDROID,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/firefox/browsers/mobile/app/?product=firefox",
            "https://apps.apple.com/app/apple-store/id989804926",
            req_headers=UA_IOS,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/firefox/browsers/mobile/app/?product=firefox&campaign=firefox-whatsnew",
            "https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dwww.mozilla.org%26utm_medium%3Dreferral%26utm_campaign%3Dfirefox-whatsnew",
            req_headers=UA_ANDROID,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/firefox/browsers/mobile/app/?product=firefox&campaign=firefox-whatsnew",
            "https://apps.apple.com/app/apple-store/id989804926?pt=373246&ct=firefox-whatsnew&mt=8",
            req_headers=UA_IOS,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/firefox/browsers/mobile/app/?product=focus&campaign=firefox-browsers-mobile-focus",
            "https://play.google.com/store/apps/details?id=org.mozilla.focus&referrer=utm_source%3Dwww.mozilla.org%26utm_medium%3Dreferral%26utm_campaign%3Dfirefox-browsers-mobile-focus",
            req_headers=UA_ANDROID,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/firefox/browsers/mobile/app/?product=focus&campaign=firefox-browsers-mobile-focus",
            "https://apps.apple.com/app/apple-store/id1055677337?pt=373246&ct=firefox-browsers-mobile-focus&mt=8",
            req_headers=UA_IOS,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/firefox/browsers/mobile/app/?product=klar&campaign=firefox-browsers-mobile-focus",
            "https://play.google.com/store/apps/details?id=org.mozilla.klar&referrer=utm_source%3Dwww.mozilla.org%26utm_medium%3Dreferral%26utm_campaign%3Dfirefox-browsers-mobile-focus",
            req_headers=UA_ANDROID,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/firefox/browsers/mobile/app/?product=klar&campaign=firefox-browsers-mobile-focus",
            "https://apps.apple.com/app/apple-store/id1073435754?pt=373246&ct=firefox-browsers-mobile-focus&mt=8",
            req_headers=UA_IOS,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        # Issue 14221
        url_test("/firefox/products/", "/products/"),
        # Issue 14252
        url_test("/rise25/", "/rise25/nominate/"),
        # Issue 14255
        url_test("/stories/", "https://blog.mozilla.org/category/products/firefox/"),
        # Issue 14231
        url_test("/firefox/flashback/", "/firefox/new/"),
        url_test("/landing/firefox/fx100/", "/firefox/new/"),
        url_test("/{santa-locator,santalocator}/", "/"),
        # Issue 14351
        url_test("/research/", "https://foundation.mozilla.org/research/"),
        url_test("/research/cc/", "https://foundation.mozilla.org/research/library/?topics=187"),
        # Issue 14222
        url_test("/firefox/browsers/", "/firefox/new/"),
        # issue 14467
        url_test("/firefox/125.0/releasenotes/", "/firefox/125.0.1/releasenotes/"),
        # issue 14647
        url_test("/privacy/hubs/", "/privacy/archive/mozilla-hubs/notice-2024-06/"),
        url_test("/about/legal/terms/hubs/", "/privacy/archive/mozilla-hubs/tos-2024-06/"),
        # issue 14248
        url_test("/firefox/privacy/", "/privacy/"),
        url_test("/firefox/privacy/products/", "/products/"),
        url_test("/firefox/privacy/safe-passwords/", "/firefox/features/password-manager/"),
        url_test("/firefox/privacy/book/", "https://support.mozilla.org/kb/how-stay-safe-web"),
        # issue 14944
        url_test("/{nothing-personal,nothingpersonal}/", "/firefox/nothing-personal/"),
        url_test("/firefox/nothingpersonal/", "/firefox/nothing-personal/"),
        # issue 15008
        url_test("/try-picture-in-picture/", "/firefox/features/picture-in-picture/"),
        # issue 15075
        url_test("/newsletter/knowledge-is-power{,/,/confirm,/confirm/token}", "/newsletter/firefox/"),
        url_test("/products/mozsocial/invite/", "/products/"),
        # Issue 15262
        url_test(
            "/products/vpn/mobile/app/?product=vpn",
            "https://play.google.com/store/apps/details?id=org.mozilla.firefox.vpn",
            req_headers=UA_ANDROID,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/products/vpn/mobile/app/?product=vpn",
            "https://apps.apple.com/app/apple-store/id1489407738",
            req_headers=UA_IOS,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/products/vpn/mobile/app/?product=vpn&campaign=vpn-landing-page",
            "https://play.google.com/store/apps/details?id=org.mozilla.firefox.vpn&referrer=utm_source%3Dwww.mozilla.org%26utm_medium%3Dreferral%26utm_campaign%3Dvpn-landing-page",
            req_headers=UA_ANDROID,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        url_test(
            "/products/vpn/mobile/app/?product=vpn&campaign=vpn-landing-page",
            "https://apps.apple.com/app/apple-store/id1489407738?pt=373246&ct=vpn-landing-page&mt=8",
            req_headers=UA_IOS,
            resp_headers={"Cache-Control": "max-age=0"},
        ),
        # Issue 15386
        url_test("/products/vpn/resource-center/no-Logging-vpn-from-mozilla/", "/products/vpn/resource-center/no-logging-vpn-from-mozilla/"),
        # Issue 15841
        url_test("/firefox/tech/", "/firefox/landing/tech/"),
        # Issue 16159
        url_test(
            "/firefox/",
            "https://www.firefox.com/",
        ),
    )
)
