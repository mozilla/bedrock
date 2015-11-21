from __future__ import absolute_import

from .base import flatten, url_test


URLS = flatten((
    # bug 832348 **/index.html -> **/
    url_test('/any/random/url/with/index.html', '/any/random/url/with/'),

    # bug 774675
    url_test('/en/', '/en-US/'),
    url_test('/es/', '/es-ES/'),
    url_test('/pt/', '/pt-BR/'),

    # bug 795970 - lowercase to uppercase, e.g. en-us to en-US
    url_test('/en-us/firefox/', '/en-US/firefox/'),
    url_test('/es-es/firefox/', '/es-ES/firefox/'),
    url_test('/pt-br/MPL/', '/pt-BR/MPL/'),

    # bug 880182
    url_test('/ja-JP-mac/', '/ja/'),

    # bug 795970 - lowercase to uppercase, e.g. en-us to en-US
    url_test('/en-us/', '/en-US/'),
    url_test('/pt-br/', '/pt-BR/'),

    # bug 845988 - remove double slashes in URLs
    url_test('/en-US/firefox//all/', '/en-US/firefox/all/'),
    url_test('/pt-BR/////thunderbird/', '/pt-BR/thunderbird/'),

    # bug 755826, 1222348
    url_test('/zh-CN/', 'http://www.firefox.com.cn/', query={
        'utm_medium': 'referral',
        'utm_source': 'mozilla.org'
    }),

    # bug 764261, 841393, 996608, 1008162, 1067691, 1113136, 1119022, 1131680, 1115626
    url_test('/zh-TW/', 'http://mozilla.com.tw/'),
    url_test('/zh-TW/mobile/', 'http://mozilla.com.tw/firefox/mobile/'),
    url_test('/zh-TW/download/', 'http://mozilla.com.tw/firefox/download/'),

    # bug 874913
    url_test('/en-US/products/download.html{,?stuff=whatnot}', '/en-US/firefox/new/'),

    # bug 845580
    url_test('/en-US/home/', '/en-US/firefox/new/'),

    # bug 948605
    url_test('/en-US/firefox/xp-any-random-thing', '/en-US/firefox/new/'),
    url_test('/en-US/products/firefox/start/', 'http://start.mozilla.org'),

    url_test('/start/the-sm-one', 'http://www.seamonkey-project.org/start/',
             req_headers={'User-Agent': 'mozilla seamonkey'},
             resp_headers={'vary': 'user-agent'}),
    url_test('/start/any-random-thing', '/firefox/new/',
             resp_headers={'vary': 'user-agent'}),

    # bug 856081 redirect /about/drivers https://wiki.mozilla.org/Firefox/Drivers
    url_test('/about/drivers{/,.html}', 'https://wiki.mozilla.org/Firefox/Drivers'),

    # community
    # bug 885797
    url_test('/community/{directory,wikis,blogs,websites}.html',
             'https://wiki.mozilla.org/Websites/Directory'),

    # bug 885856
    url_test('/projects/index.{de,fr,hr,sq}.html', '/{de,fr,hr,sq}/firefox/products/'),

    # bug 856075
    url_test('/projects/technologies.html',
             'https://developer.mozilla.org/docs/Mozilla/Using_Mozilla_code_in_other_projects'),

    # bug 787269
    url_test('/projects/security/components/signed-script{s,-example}.html',
             'https://developer.mozilla.org/docs/Bypassing_Security_Restrictions_and_Signing_Code'),

    # bug 874526, 877698
    url_test('/projects/security/components/any-random-thing',
             'http://www-archive.mozilla.org/projects/security/components/any-random-thing'),

    # bug 876889
    url_test('/projects/testopia/',
             'https://developer.mozilla.org/docs/Mozilla/Bugzilla/Testopia'),

    # bug 874525
    url_test('/projects/security/pki/{n,j}ss/random-thing',
             'https://developer.mozilla.org/docs/{N,J}SS'),

    # bug 866190
    url_test('/projects/security/pki/python-nss/',
             'https://developer.mozilla.org/docs/Python_binding_for_NSS'),

    # bug 1043035
    url_test('/projects/security/pki/{,index.html}',
             'https://developer.mozilla.org/docs/PKI'),
    url_test('/projects/security/pki/pkcs11-random-thing',
             'https://developer.mozilla.org/docs/Mozilla/Projects/NSS#PKCS_.2311_information'),
    url_test('/projects/security/pki/psm-random-thing',
             'https://developer.mozilla.org/docs/Mozilla/Projects/PSM'),
    url_test('/projects/security/pki/src-random-thing',
             'https://developer.mozilla.org/docs/Mozilla/Projects/NSS/NSS_Sources_Building_Testing'),

    # bug 975476
    url_test('/projects/security/pki/python-nss/doc/api/current/html/random/stuff/',
             'https://mozilla.github.io/python-nss-docs/random/stuff/'),

    # bug 780672
    url_test('/firefox/webhero/random/stuff/', '/firefox/new/'),

    # bug 964107
    url_test('/firefox/video/random/stuff/', 'https://www.youtube.com/firefoxchannel'),

    # bug 948520
    url_test('/firefox/livebookmarks/random/stuff/',
             'https://support.mozilla.org/kb/Live%20Bookmarks'),

    # bug 782333
    url_test('/firefox/backtoschool/',
             'https://addons.mozilla.org/firefox/collections/mozilla/back-to-school/'),
    url_test('/firefox/backtoschool/firstrun/', '/firefox/firstrun/'),

    # bug 824126, 837942
    url_test('/ports/qtmozilla/{,index.html}', 'https://wiki.mozilla.org/Qt'),
    url_test('/ports/os2/', 'https://wiki.mozilla.org/Ports/os2'),
    url_test('/ports/other-things/', 'http://www-archive.mozilla.org/ports/other-things/'),

    # bug 1013082
    url_test('/ja/', 'http://www.mozilla.jp/'),

    # bug 1051686
    url_test('/ja/firefox/organizations/', 'http://www.mozilla.jp/business/downloads/'),

    # bug 1205632
    url_test('/js/language/',
             'https://developer.mozilla.org/docs/Web/JavaScript/Language_Resources'),
    url_test('/js/language/js20/', 'http://www.ecmascript-lang.org'),
    url_test('/js/language/es4/', 'http://www.ecmascript-lang.org'),
    url_test('/js/language/E262-3-errata.html',
             'http://www-archive.mozilla.org/js/language/E262-3-errata.html'),

    # bug 1138280
    url_test('/ja/firefox/beta/notes/', 'http://www.mozilla.jp/firefox/beta/notes/'),
    url_test('/ja/thunderbird/notes/', 'http://www.mozilla.jp/thunderbird/notes/'),
    url_test('/ja/thunderbird/android/2.2beta/releasenotes/',
             'http://www.mozilla.jp/thunderbird/android/2.2beta/releasenotes/'),

    # bug 987059, 1050149, 1072170, 1208358
    url_test('/ja/about/', 'http://www.mozilla.jp/about/mozilla/'),
    url_test('/ja/about/japan/', 'http://www.mozilla.jp/about/japan/'),

    # bug 927442
    url_test('{/firefox,}/community/', '/contribute/'),

    # bug 925551
    url_test('/plugincheck/more_info.html', '/plugincheck/'),

    # bug 854561
    url_test('/projects/mozilla-based{.html,/}', '/about/mozilla-based/'),

    # bug 851727
    url_test('/projects/powered-by{.html,/}', '/about/powered-by/'),

    # bug 957664
    url_test('/press/awards{/,.html}', 'https://blog.mozilla.org/press/awards/'),

    url_test('/firefox/aurora/all/', '/firefox/developer/all/'),
    url_test('/projects/firefox/3.6.10/whatsnew/bunny-lebowski/',
             '/firefox/3.6.10/whatsnew/bunny-lebowski/'),
    url_test('/projects/firefox/4.0/firstrun/', '/firefox/4.0/firstrun/'),
    url_test('/projects/firefox/4.0a2/{firstrun,whatsnew}/stuff',
             '/firefox/nightly/firstrun/stuff'),

    url_test('/{{firefox,mobile}/,}beta/', '/firefox/channel/#beta'),
    url_test('/{{firefox,mobile}/,}aurora/', '/firefox/channel/#developer'),

    url_test('/firefox/unsupported-systems.html', '/firefox/unsupported-systems/'),
    url_test('/download/', '/firefox/new/'),

    url_test('/firefox/firefox.exe', '/'),
    # should be case insensitive
    url_test('/pt-BR/FireFox/Firefox.EXE', '/pt-BR/'),

    # bug 821006
    url_test('/firefox/all.html', '/firefox/all/'),

    # bug 727561
    url_test('/firefox/search{,.html}', '/firefox/new/'),

    # bug 860865, 1101220
    url_test('/firefox/all-{beta,rc}{/,.html}', '/firefox/beta/all/'),
    url_test('/firefox/all-aurora{/,.html}', '/firefox/developer/all/'),
    url_test('/firefox/aurora/{all,notes,system-requirements}/'
             '/firefox/developer/{all,notes,system-requirements}/'),
    url_test('/firefox/organizations/all.html', '/firefox/organizations/all/'),

    # bug 729329
    url_test('/mobile/sync/is/da/best/', '/firefox/sync/'),

    # bug 882845
    url_test('/firefox/toolkit/download-to-your-devices/because-i-say-so/', '/firefox/new/'),

    # bug 1091977
    url_test('/ja/contribute/random/stuff/', 'http://www.mozilla.jp/community/'),

    # bug 1014823
    url_test('/pt-BR/firefox/releases/whatsnew/', '/pt-BR/firefox/whatsnew/'),

    # bug 929775
    url_test('/firefox/update/and/stuff/', '/firefox/new/', query={
        'utm_source': 'firefox-browser',
        'utm_medium': 'firefox-browser',
        'utm_campaign': 'firefox-update-redirect',
    }),

    # bug 868182
    url_test('/firefox/mobile/faq/?os=firefox-os', '/firefox/os/faq/'),

    # Bug 986174
    url_test('/{m,{firefox/,}mobile}/features/', '/firefox/android/'),
    url_test('/{m,{firefox/,}mobile}/faq/', '/firefox/android/faq/'),


    # bug 885799, 952429
    url_test('/projects/calendar/holidays.html', '/projects/calendar/holidays/'),
    url_test('/en-US/projects/calendar/random/stuff/', '/projects/calendar/'),
    # redirects don't catch real urls
    url_test('/en-US/projects/calendar/', status_code=200),
    url_test('/en-US/projects/calendar/holidays/', status_code=200),

    # bug 1124038
    url_test('/thunderbird/organizations/{all-esr.html,faq/}', '/thunderbird/organizations/'),

    # bug 1123399, 1150649
    url_test('/thunderbird/all.htm', '/thunderbird/all/'),
    url_test('/thunderbird/all-beta.html', '/thunderbird/beta/all/'),
    url_test('/thunderbird/early_releases/downloads/', '/thunderbird/beta/all/'),
    url_test('/thunderbird/early_releases/', '/thunderbird/channel/'),

    # bug 1081917, 1029829, 1029838
    url_test('/thunderbird/releases/0.9.html',
             'http://website-archive.mozilla.org/www.mozilla.org/thunderbird_releasenotes'
             '/en-US/thunderbird/releases/0.9.html'),
    # should catch everything 1.* to 29.*
    url_test('/thunderbird/{1,5,15,29}.0beta/{releasenotes,system-requirements}/',
             'http://website-archive.mozilla.org/www.mozilla.org/thunderbird_releasenotes'
             '/en-US/thunderbird/{1,5,15,29}.0beta/{releasenotes,system-requirements}/'),

    # bug 1124042
    url_test('/thunderbird/features/email_providers.html', '/thunderbird/email-providers/'),

    # bug 1133266
    url_test('/thunderbird/legal/privacy/', '/privacy/thunderbird/'),
    url_test('/thunderbird/about/privacy-policy/', '/privacy/archive/thunderbird/2010-06/'),

    # bug 1196578
    url_test('/thunderbird/about/legal/eula/', '/about/legal/eula/'),
    url_test('/thunderbird/about/legal/eula/thunderbird2.html', '/about/legal/eula/thunderbird-2/'),
    url_test('/thunderbird/about/legal/eula/thunderbird.html', '/about/legal/eula/thunderbird-1.5/'),

    # bug 1204579
    url_test('/thunderbird/2.0.0.0/eula/', '/about/legal/eula/thunderbird-2/'),
    url_test('/thunderbird/about/legal/', '/about/legal/terms/mozilla/'),
    url_test('/thunderbird/download/', '/thunderbird/'),
    url_test('/thunderbird/about/', 'https://wiki.mozilla.org/Thunderbird'),
    url_test('/thunderbird/about/mission/', 'https://wiki.mozilla.org/Thunderbird'),
    url_test('/thunderbird/about/{careers,contact,get-involved}/',
             'https://wiki.mozilla.org/Thunderbird#Contributing'),
    url_test('/thunderbird/community/', 'https://wiki.mozilla.org/Thunderbird#Contributing'),
    url_test('/thunderbird/3.1{a,b,rc}{1,2}/',
             'http://website-archive.mozilla.org/www.mozilla.org/thunderbird/thunderbird/3.1{a,b,rc}{1,2}/'),
    url_test('/thunderbird/{6,7,8,9}.0beta/',
             'http://website-archive.mozilla.org/www.mozilla.org/thunderbird/thunderbird/{6,7,8,9}.0beta/'),
    url_test('/thunderbird/about/{board,press,staff}/',
             'http://website-archive.mozilla.org/www.mozilla.org/thunderbird/thunderbird/about/{board,press,staff}/'),

    # bug 1121082
    url_test('/hello/', '/firefox/hello/'),

    # bug 1148127
    url_test('/products/', '/firefox/products/'),

    # Bug 1110927
    url_test('/firefox/start/central.html', '/firefox/new/'),
    url_test('/firefox/sync/firstrun.html', '/firefox/sync/'),
    url_test('/firefox/panorama/', 'https://support.mozilla.org/kb/tab-groups-organize-tabs'),

    # bug 876810
    url_test('/hacking/commit-access-policy/',
             '/about/governance/policies/commit/access-policy/'),
    url_test('/hacking/committer/{,faq.html}', '/about/governance/policies/commit/'),
    url_test('/hacking/notification/', '/about/governance/policies/commit/'),
    url_test('/hacking/committer/committers-agreement.{odt,pdf,txt}',
             'https://static.mozilla.com/foundation/documents/'
             'commit-access/committers-agreement.{odt,pdf,txt}'),
    url_test('/hacking/notification/acceptance-email.txt',
             'https://static.mozilla.com/foundation/documents/commit-access/acceptance-email.txt'),

    # bug 1165344
    url_test('/hacking/CVS-Contributor-Form.{pdf,ps}', '/about/governance/policies/commit/'),
    url_test('/hacking/{form,getting-cvs-write-access}.html',
             '/about/governance/policies/commit/'),
    url_test('/hacking/portable-cpp.html',
             'https://developer.mozilla.org/docs/Mozilla/C++_Portability_Guide'),
    url_test('/hacking/rules.html', 'https://developer.mozilla.org/docs/mozilla-central'),
    url_test('/hacking/{module-ownership,reviewers}.html',
             '/about/governance/policies/{module-ownership,reviewers}/'),
    url_test('/hacking/regression-policy.html', '/about/governance/policies/regressions/'),

    # Bug 1040970
    url_test('/mozillacareers', 'https://wiki.mozilla.org/People/mozillacareers', query={
        'utm_medium': 'redirect',
        'utm_source': 'mozillacareers-vanity',
    }),

    # Bug 987852 & 1201914
    url_test('/MPL/Revision-FAQ.html', '/MPL/Revision-FAQ/'),
    url_test('/MPL/2.0/index.txt', '/media/MPL/2.0/index.txt'),

    # Bug 1090468
    url_test('/security/transition.txt', '/media/security/transition.txt'),

    # Bug 920212
    url_test('/firefox/fx/', '/firefox/new/'),

    # Bug 979670, 979531, 1003727, 979664, 979654, 979660
    url_test('/firefox/features/', '/firefox/desktop/'),
    url_test('/firefox/customize/', '/firefox/desktop/customize/'),
    url_test('/firefox/{performance,happy,speed,memory}/', '/firefox/desktop/fast/'),
    url_test('/firefox/security/', '/firefox/desktop/trust/'),
    url_test('/firefox/technology/', 'https://developer.mozilla.org/docs/Tools'),

    # Bug 979527
    url_test('/firefox/central/', '/firefox/new/',
             req_headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) '
                                        'Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1'},
             resp_headers={'vary': 'user-agent'}),
    url_test('/firefox/central/',
             'https://support.mozilla.org/kb/get-started-firefox-overview-main-features',
             req_headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) '
                                        'Gecko/20100101 Firefox/42.0'},
             resp_headers={'vary': 'user-agent'}),

    # bug 868169
    url_test('/mobile/android-download.html?dude=abiding',
             'https://play.google.com/store/apps/details', query={'id': 'org.mozilla.firefox',
                                                                  'dude': 'abiding'}),
    url_test('/mobile/android-download-beta.html?walter=raging',
             'https://play.google.com/store/apps/details', query={'id': 'org.mozilla.firefox_beta',
                                                                  'walter': 'raging'}),
    # bug 877198
    url_test('/press/news.html', 'http://blog.mozilla.org/press/'),
    url_test('/press/mozilla-2003-10-15.html',
             'http://blog.mozilla.org/press/2003/10/mozilla-foundation-launches-new-web-browser-and-end-user-services/'),
    url_test('/press/mozilla-2004-02-09.html',
             'https://blog.mozilla.org/press/2004/02/new-round-of-releases-extends-mozilla-project%C2%92s-standards-based-open-source-offerings/'),
    url_test('/press/mozilla-2004-02-17.html',
             'http://blog.mozilla.org/press/2004/02/mozilla-gains-stronghold-in-europe/'),
    url_test('/press/mozilla-2004-02-26.html',
             'https://blog.mozilla.org/press/2004/02/mozilla-foundation-rallies-supporters-to-take-back-the-web/'),
    url_test('/press/mozilla-2004-05-03.html',
             'http://blog.mozilla.org/press/2004/05/mozilla-foundation-releases-thunderbird-0-6/'),
    url_test('/press/mozilla-2004-06-15.html',
             'http://blog.mozilla.org/press/2004/06/mozilla-reloads-firefox/'),
    url_test('/press/mozilla-2004-06-16.html',
             'http://blog.mozilla.org/press/2004/06/mozilla-foundation-releases-thunderbird-0-7/'),
    url_test('/press/mozilla-2004-06-30.html',
             'http://blog.mozilla.org/press/2013/11/mozilla-foundation-announces-more-open-scriptable-plugins/'),
    url_test('/press/mozilla-2004-08-02.html',
             'http://blog.mozilla.org/press/2004/08/mozilla-foundation-announces-security-bug-bounty-program/'),
    url_test('/press/mozilla-2004-08-10.html',
             'http://blog.mozilla.org/press/2004/08/mozilla-foundation-announces-xforms-development-project/'),
    url_test('/press/mozilla-2004-08-18.html',
             'http://blog.mozilla.org/press/2004/08/mozilla-affiliate-in-japan-kicks-off/'),
    url_test('/press/mozilla-2004-09-14-01.html',
             'http://blog.mozilla.org/press/2004/09/mozilla-foundation-announces-first-payments-of-security-bug-bounty-program-further-strengthens-browser-security/'),
    url_test('/press/mozilla-2004-09-14-02.html',
             'http://blog.mozilla.org/press/2013/11/firefox-preview-release-and-thunderbird-0-8-released/'),
    url_test('/press/mozilla-2004-09-20.html',
             'http://blog.mozilla.org/press/2004/09/mozilla-firefox-preview-release-hits-one-million-downloads-in-first-four-days-of-availability/'),
    url_test('/press/mozilla-2004-10-01-02.html',
             'http://blog.mozilla.org/press/2004/10/important-security-update-for-firefox-available/'),
    url_test('/press/mozilla-2004-11-09.html',
             'http://blog.mozilla.org/press/2004/11/mozilla-foundation-releases-the-highly-anticipated-mozilla-firefox-1-0-web-browser/'),
    url_test('/press/mozilla-2004-11-22.html',
             'http://blog.mozilla.org/press/2004/11/important-update-to-german-language-version-of-firefox-1-0/'),
    url_test('/press/mozilla-2004-12-15.html',
             'http://blog.mozilla.org/press/2004/12/mozilla-foundation-places-two-page-advocacy-ad-in-the-new-york-times/'),
    url_test('/press/mozilla-2004-12-7.html',
             'http://blog.mozilla.org/press/2004/12/mozilla-thunderbird-1-0-email-client-has-landed/'),
    url_test('/press/mozilla-2005-01-07.html',
             'http://blog.mozilla.org/press/2005/01/mozilla-firefox-and-thunderbird-to-support-new-open-standard-platform-for-usb-drives/'),
    url_test('/press/mozilla-2005-02-02.html',
             'http://blog.mozilla.org/press/2005/02/mozilla-foundation-announces-beta-release-of-xforms-1-0-recommendation/'),
    url_test('/press/mozilla-2005-02-16.html',
             'http://blog.mozilla.org/press/2005/01/mozilla-firefox-and-thunderbird-to-support-new-open-standard-platform-for-usb-drives/'),
    url_test('/press/mozilla-2005-02-24.html',
             'http://blog.mozilla.org/press/2005/02/mozilla-foundation-announces-update-to-firefox/'),
    url_test('/press/mozilla-2005-03-04.html',
             'http://blog.mozilla.org/press/2005/03/mozilla-foundation-expands-with-launch-of-mozilla-china/'),
    url_test('/press/mozilla-2005-03-23.html',
             'http://blog.mozilla.org/press/2005/03/mozilla-foundation-releases-security-update-to-firefox/'),
    url_test('/press/mozilla-2005-03-28.html',
             'http://blog.mozilla.org/press/2005/03/mozilla-foundation-awards-bug-bounties/'),
    url_test('/press/mozilla-2005-05-13.html',
             'http://blog.mozilla.org/press/2005/05/mozilla-foundation-co-hosts-europes-leading-xml-and-web-developer-conference/'),
    url_test('/press/mozilla-2005-07-28.html',
             'http://blog.mozilla.org/press/2005/07/mozilla-headlines-two-key-open-source-development-conferences-in-august/'),
    url_test('/press/mozilla-2005-08-03.html',
             'http://blog.mozilla.org/press/2005/08/mozilla-foundation-forms-new-organization-to-further-the-creation-of-free-open-source-internet-software-including-the-award-winning-mozilla-firefox-browser/'),
    url_test('/press/mozilla-2005-10-03.html',
             'http://blog.mozilla.org/press/2005/10/mozilla-launches-beta-of-comprehensive-online-developer-center/'),
    url_test('/press/mozilla-2005-10-19.html',
             'http://blog.mozilla.org/press/2005/10/firefox-surpasses-100-million-downloads/'),
    url_test('/press/mozilla-2005-11-29.html',
             'http://blog.mozilla.org/press/2005/11/mozilla-introduces-firefox-1-5-and-ups-the-ante-in-web-browsing/'),
    url_test('/press/mozilla-2005-11-3.html',
             'http://blog.mozilla.org/press/2005/11/mozilla-kicks-off-extend-firefox-competition/'),
    url_test('/press/mozilla-2005-11-30.html',
             'http://blog.mozilla.org/press/2005/11/firefox-1-5-adds-answers-com-for-quick-reference/'),
    url_test('/press/mozilla-2005-12-2.html',
             'http://blog.mozilla.org/press/2005/12/mozilla-launches-firefox-flicks-campaign/'),
    url_test('/press/mozilla-2005-12-22.html',
             'http://blog.mozilla.org/press/2005/12/mozilla-launches-firefox-flicks-ad-contest/'),
    url_test('/press/mozilla-2006-01-12.html',
             'http://blog.mozilla.org/press/2006/01/mozilla-releases-thunderbird-1-5-email-client/'),
    url_test('/press/mozilla-2006-01-24.html',
             'http://blog.mozilla.org/press/2006/01/firefox-1-5-adoption-rising-as-browser-garners-acclaim/'),
    url_test('/press/mozilla-2006-01-25.html',
             'http://blog.mozilla.org/press/2006/01/indie-film-all-stars-foin-firefox-flicks-crew/'),
    url_test('/press/mozilla-2006-02-03.html',
             'http://blog.mozilla.org/press/2006/02/mozilla-releases-preview-of-application-framework-for-development-of-cross-platform-internet-client-applications/'),
    url_test('/press/mozilla-2006-03-02.html',
             'http://blog.mozilla.org/press/2006/03/mozilla-announces-winners-of-extend-firefox-competition/'),
    url_test('/press/mozilla-2006-04-12.html',
             'http://blog.mozilla.org/press/2006/04/mozilla-showcases-first-round-of-community-produced-firefox-flicks-videos/'),
    url_test('/press/mozilla-2006-04-18.html',
             'http://blog.mozilla.org/press/2006/04/mozilla-receives-over-280-community-produced-videos-for-firefox-flicks/'),
    url_test('/press/mozilla-2006-04-27.html',
             'http://blog.mozilla.org/press/2006/04/firefox-flicks-video-contest-winners-announced/'),
    url_test('/press/mozilla-2006-06-14.html',
             'http://blog.mozilla.org/press/2006/06/mozilla-feeds-soccer-fans-passion-with-new-firefox-add-on/'),
    url_test('/press/mozilla-2006-10-11.html',
             'http://blog.mozilla.org/press/2006/10/qualcomm-launches-project-in-collaboration-with-mozilla-foundation-to-develop-open-source-version-of-eudora-email-program/'),
    url_test('/press/mozilla-2006-10-24-02.html',
             'http://blog.mozilla.org/press/2006/10/firefox-moving-the-internet-forward/'),
    url_test('/press/mozilla-2006-10-24.html',
             'http://blog.mozilla.org/press/2006/10/mozilla-releases-major-update-to-firefox-and-raises-the-bar-for-online-experience/'),
    url_test('/press/mozilla-2006-11-07.html',
             'http://blog.mozilla.org/press/2006/11/adobe-and-mozilla-foundation-to-open-source-flash-player-scripting-engine/'),
    url_test('/press/mozilla-2006-12-04.html',
             'http://blog.mozilla.org/press/2006/12/the-world-economic-forum-announces-technology-pioneers-2007-mozilla-selected/'),
    url_test('/press/mozilla-2006-12-11.html',
             'http://blog.mozilla.org/press/2006/12/mozilla-firefox-headed-for-primetime/'),
    url_test('/press/mozilla-2007-02-07.html',
             'http://blog.mozilla.org/press/2007/02/kodak-and-mozilla-join-forces-to-make-sharing-photos-even-easier/'),
    url_test('/press/mozilla-2007-03-27.html',
             'http://blog.mozilla.org/press/2007/03/mozilla-launches-new-firefox-add-ons-web-site/'),
    url_test('/press/mozilla-2007-03-28.html',
             'http://blog.mozilla.org/press/2007/03/mozilla-and-ebay-working-together-to-make-the-auction-experience-easier-for-firefox-users-in-france-germany-and-the-uk/'),
    url_test('/press/mozilla-2007-04-19.html',
             'http://blog.mozilla.org/press/2007/04/mozilla-thunderbird-2-soars-to-new-heights/'),
    url_test('/press/mozilla-2007-05-16.html',
             'http://blog.mozilla.org/press/2007/05/united-nations-agency-awards-mozilla-world-information-society-award/'),
    url_test('/press/mozilla-2007-07-04.html',
             'http://blog.mozilla.org/press/2007/07/mozilla-and-ebay-launch-firefox-companion-for-ebay-users/'),
    url_test('/press/mozilla-2007-08-10.html',
             'http://blog.mozilla.org/press/2007/08/mozilla-to-host-24-hour-worldwide-community-event/'),
    url_test('/press/mozilla-2007-08-28.html',
             'http://blog.mozilla.org/press/2007/08/mozilla-welcomes-students-back-to-school-with-firefox-campus-edition/'),
    url_test('/press/mozilla-2007-09-17-faq.html',
             'http://blog.mozilla.org/press/2007/09/mozilla-launches-internet-mail-and-communications-initiative/'),
    url_test('/press/mozilla-2007-09-17.html',
             'http://blog.mozilla.org/press/2007/09/mozilla-launches-internet-mail-and-communications-initiative/'),
    url_test('/press/mozilla-2008-01-07-faq.html',
             'http://blog.mozilla.org/press/2008/01/mozilla-appoints-john-lilly-as-chief-executive-officer/'),
    url_test('/press/mozilla-2008-01-07.html',
             'http://blog.mozilla.org/press/2008/01/mozilla-appoints-john-lilly-as-chief-executive-officer/'),
    url_test('/press/mozilla-2008-02-19-faq.html',
             'http://blog.mozilla.org/press/2008/02/mozilla-messaging-starts-up-operations/'),
    url_test('/press/mozilla-2008-02-19.html',
             'http://blog.mozilla.org/press/2008/02/mozilla-messaging-starts-up-operations/'),
    url_test('/press/mozilla-2008-05-28.html',
             'http://blog.mozilla.org/press/2008/05/mozilla-aims-to-set-guinness-world-record-on-firefox-3-download-day/'),
    url_test('/press/mozilla-2008-06-17-faq.html',
             'http://blog.mozilla.org/press/2008/06/mozilla-releases-firefox-3-and-redefines-the-web-experience/'),
    url_test('/press/mozilla-2008-06-17.html',
             'http://blog.mozilla.org/press/2008/06/mozilla-releases-firefox-3-and-redefines-the-web-experience/'),
    url_test('/press/mozilla-2008-07-02.html',
             'http://blog.mozilla.org/press/2008/07/mozilla-sets-new-guinness-world-record-with-firefox-3-downloads/'),
    url_test('/press/mozilla-2008-11-18.html',
             'http://blog.mozilla.org/press/2008/11/mozilla-launches-fashion-your-firefox-and-makes-it-easy-to-customize-the-browsing-experience/'),
    url_test('/press/mozilla-2008-12-03.html',
             'http://blog.mozilla.org/press/2008/12/mozilla-and-zazzle-announce-strategic-relationship-for-apparel-on-demand/'),
    url_test('/press/mozilla-2009-03-31.html',
             'https://blog.mozilla.org/press/2009/03/%C2%AD%C2%ADmozilla-adds-style-and-star-power-to-firefox-with-new-personas/'),
    url_test('/press/mozilla-2009-06-30-faq.html',
             'http://blog.mozilla.org/press/2009/04/mozilla-advances-the-web-with-firefox-3-5/'),
    url_test('/press/mozilla-2009-06-30.html',
             'http://blog.mozilla.org/press/2009/04/mozilla-advances-the-web-with-firefox-3-5/'),
    url_test('/press/mozilla-foundation.html',
             'http://blog.mozilla.org/press/2003/07/mozilla-org-announces-launch-of-the-mozilla-foundation-to-lead-open-source-browser-efforts/'),
    url_test('/press/mozilla1.0.html',
             'http://blog.mozilla.org/press/2002/06/mozilla-org-launches-mozilla-1-0/'),
    url_test('/press/open-source-security.html',
             'http://blog.mozilla.org/press/2000/01/open-source-development-of-security-products-possible-worldwide-enhancing-security-and-privacy-for-e-commerce-and-communication/'),

    # Bug 608370, 957664
    url_test('/press/kit{.html,s/}', 'https://blog.mozilla.org/press/kits/'),

    # bug 957637
    url_test('/sopa/',
             'https://blog.mozilla.org/blog/2012/01/19/firefox-users-engage-congress-sopa-strike-stats/'),

    # bug 675031
    url_test('/projects/fennec/is/a/pretty/fox.html',
             'http://website-archive.mozilla.org/www.mozilla.org/fennec_releasenotes/projects/fennec/is/a/pretty/fox.html'),

    # bug 924687
    url_test('/opportunities{,/,/index.html}', 'https://careers.mozilla.org/'),

    # bug 884933
    url_test('/{m,{firefox/,}mobile}/platforms/',
             'https://support.mozilla.org/kb/will-firefox-work-my-mobile-device'),

    url_test('/m/', '/firefox/new/'),

    # bug 876581
    url_test('/firefox/phishing-protection/',
             'https://support.mozilla.org/kb/how-does-phishing-and-malware-protection-work'),

    # bug 1006079
    url_test('/mobile/home/{,index.html}',
             'https://blog.mozilla.org/services/2012/08/31/retiring-firefox-home/'),

    # bug 949562
    url_test('/mobile/home/1.0/releasenotes/{,index.html}',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_home/mobile/home/1.0/releasenotes/'),
    url_test('/mobile/home/1.0.2/releasenotes/{,index.html}',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_home/mobile/home/1.0.2/releasenotes/'),
    url_test('/mobile/home/faq/{,index.html}',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_home/mobile/home/faq/'),

    # bug 960064
    url_test('/firefox/vpat-1.5.html',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_vpat/firefox-vpat-1.5.html'),
    url_test('/firefox/vpat.html',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_vpat/firefox-vpat-3.html'),

    # bug 1068931
    url_test('/advocacy/', 'https://advocacy.mozilla.org/'),

    # bug 887426
    url_test('/about/policies/', '/about/governance/policies/'),
    url_test('/about/policies/participation.html', '/about/governance/policies/participation/'),
    url_test('/about/policies/policies.html', '/about/governance/policies/'),

    # bug 882923
    url_test('/opt-out.html', '/privacy/websites/#user-choices'),

    # bug 818321
    url_test('/projects/security/tld-idn-policy-list.html',
             '/about/governance/policies/security-group/tld-idn/'),
    url_test('/projects/security/membership-policy.html',
             '/about/governance/policies/security-group/membership/'),
    url_test('/projects/security/secgrouplist.html',
             '/about/governance/policies/security-group/'),
    url_test('/projects/security/security-bugs-policy.html',
             '/about/governance/policies/security-group/bugs/'),

    # bug 818316, 1128579
    url_test('/projects/security/certs/', '/about/governance/policies/security-group/certs/'),
    url_test('/projects/security/certs/included/', 'https://wiki.mozilla.org/CA:IncludedCAs'),
    url_test('/projects/security/certs/pending/', 'https://wiki.mozilla.org/CA:PendingCAs'),
    url_test('/about/governance/policies/security-group/certs/included/',
             'https://wiki.mozilla.org/CA:IncludedCAs'),
    url_test('/about/governance/policies/security-group/certs/pending/',
             'https://wiki.mozilla.org/CA:PendingCAs'),
    url_test('/projects/security/certs/policy/',
             '/about/governance/policies/security-group/certs/policy/'),
    url_test('/projects/security/certs/policy/EnforcementPolicy.html',
             '/about/governance/policies/security-group/certs/policy/enforcement/'),
    url_test('/projects/security/certs/policy/MaintenancePolicy.html',
             '/about/governance/policies/security-group/certs/policy/maintenance/'),
    url_test('/projects/security/certs/policy/InclusionPolicy.html',
             '/about/governance/policies/security-group/certs/policy/inclusion/'),

    # bug 926629
    url_test('/newsletter/about_mobile/', '/newsletter/'),
    url_test('/newsletter/about_mozilla/', '/contribute/'),
    url_test('/newsletter/new/', '/newsletter/'),

    # bug 818323
    url_test('/projects/security/known-vulnerabilities.html', '/security/known-vulnerabilities/'),
    url_test('/projects/security/older-vulnerabilities.html',
             '/security/known-vulnerabilities/older-vulnerabilities/'),

    # bug 1017564
    url_test('/mobile/RANDOM-STUFF/system-requirements/',
             'https://support.mozilla.org/kb/will-firefox-work-my-mobile-device'),

    # bug 1041712, 1069335, 1069902
    url_test('/{firefox,mobile}/{2,19,27}.0{a2,beta,.2}/{release,aurora}notes/{,stuff}',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_releasenotes/en-US'
             '/{firefox,mobile}/{2,19,27}.0{a2,beta,.2}/{release,aurora}notes/{,stuff}'),

    # bug 1090468
    url_test('/security/{older-alerts,security-announcement,phishing-test{,-results}}.html',
             'http://website-archive.mozilla.org/www.mozilla.org/security/security'
             '/{older-alerts,security-announcement,phishing-test{,-results}}.html'),
    url_test('/security/iSECPartners_Phishing.pdf',
             'http://website-archive.mozilla.org/www.mozilla.org/security/security'
             '/iSECPartners_Phishing.pdf'),

    # bug 878039
    url_test('/access/', 'https://developer.mozilla.org/docs/Web/Accessibility'),
    url_test('/access/architecture.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_architecture'),
    url_test('/access/at-vendors.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_Assistive_Technology_Vendors'),
    url_test('/access/authors.html',
             'https://developer.mozilla.org/docs/Web/Accessibility/Information_for_Web_authors'),
    url_test('/access/core-developers.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_Information_for_Core_Gecko_Developer'),
    url_test('/access/evaluators.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_Governments_and_Other_Organization'),
    url_test('/access/event-flow.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Event_Process_Procedure'),
    url_test('/access/external-developers.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_External_Developers_Dealing_with_A#community'),
    url_test('/access/features.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_Features_in_Firefox'),
    url_test('/access/highlevel.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/CSUN_Firefox_Materials'),
    url_test('/access/platform-apis.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_API_cross-reference#Accessible_Roles'),
    url_test('/access/plugins-work.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Mozilla_Plugin_Accessibility'),
    url_test('/access/prefs-and-apis.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Embedding_API_for_Accessibility'),
    url_test('/access/resources.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Links_and_Resources'),
    url_test('/access/section508.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Mozilla_s_Section_508_Compliance'),
    url_test('/access/today.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Software_accessibility_today'),
    url_test('/access/toolkit-checklist.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/What_needs_to_be_done_when_building_new_toolkits'),
    url_test('/access/ui-developers.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Accessibility_information_for_UI_designers'),
    url_test('/access/users.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Information_for_users'),
    url_test('/access/w3c-uaag.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/UAAG_evaluation_report'),
    url_test('/access/w4a.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/W4A'),
    url_test('/access/windows/at-apis.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/Gecko_info_for_Windows_accessibility_vendors'),
    url_test('/access/windows/msaa-server.html',
             'https://developer.mozilla.org/docs/Web/Accessibility/Implementing_MSAA_server'),
    url_test('/access/windows/zoomtext.html',
             'https://developer.mozilla.org/docs/Mozilla/Accessibility/ZoomText'),

    # bug 1148187
    url_test('/access/unix.html',
             'http://website-archive.mozilla.org/www.mozilla.org/access/access/unix.html'),

    # bug 1216953
    url_test('/MPL/MPL-1.0.html',
             'http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/1.0/'),
    url_test('/MPL/MPL-1.1.html', '/MPL/1.1/'),

    # bug 987852
    url_test('/MPL/0.95/stuff.html',
             'http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/0.95/stuff.html'),
    url_test('/MPL/1.0/stuff.html',
             'http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/1.0/stuff.html'),
    url_test('/MPL/2.0/process/stuff.html',
             'http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/2.0/process/stuff.html'),
    url_test('/MPL/NPL/stuff.html',
             'http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/NPL/stuff.html'),
    url_test('/MPL/boilerplate-1.1/stuff.html',
             'http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/boilerplate-1.1/stuff.html'),
    url_test('/MPL/missing.html',
             'http://website-archive.mozilla.org/www.mozilla.org/mpl/MPL/missing.html'),

    # bug 858315
    url_test('/projects/devpreview/firstrun/', '/firefox/firstrun/'),
    url_test('/projects/devpreview/stuff.html',
             'http://website-archive.mozilla.org/www.mozilla.org/devpreview_releasenotes/projects/devpreview/stuff.html'),

    # bug 947890, 1069902
    url_test('/firefox/releases/{0.9.1,1.5.0.1}.html',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_releasenotes/en-US'
             '/firefox/releases/{0.9.1,1.5.0.1}.html'),
    url_test('/{firefox,mobile}/{2,9,18,25}.0/releasenotes/',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_releasenotes/en-US'
             '/{firefox,mobile}/{2,9,18,25}.0/releasenotes/'),

    # bug 988746, 989423, 994186, 1153351
    url_test('/mobile/{23,28,29}.0/releasenotes/',
             '/firefox/android/{23,28,29}.0/releasenotes/'),
    url_test('/mobile/{3,4}2.0beta/{aurora,release}notes/',
             '/firefox/android/{3,4}2.0beta/{aurora,release}notes/'),

    # bug 724682
    url_test('/projects/mathml/demo/texvsmml.html',
             'https://developer.mozilla.org/docs/Mozilla_MathML_Project/MathML_Torture_Test'),
    url_test('/projects/mathml/{,demo/}',
             'https://developer.mozilla.org/en-US/docs/Mozilla/MathML_Project'),
    url_test('/projects/mathml/fonts/',
             'https://developer.mozilla.org/Mozilla_MathML_Project/Fonts'),
    url_test('/projects/mathml/screenshots/',
             'https://developer.mozilla.org/Mozilla_MathML_Project/Screenshots'),

    # bug 961010
    url_test('/mobile/credits/credits-people-list.html', '/credits/'),

    url_test('/{mobile,fennec}/', '/firefox/partners/'),

    # bug 876668
    url_test('/mobile/customize/', '/firefox/android/'),

    # bug 736934, 860865, 1101220, 1153351
    url_test('/mobile/{{beta,aurora}/,}notes/', '/firefox/android/{{beta,aurora}/,}notes/'),
    url_test('/firefox/{{beta,aurora,organizations}/,}system-requirements.html',
             '/firefox/{{beta,aurora,organizations}/,}system-requirements/'),

    # bug 897082
    url_test('/about/mozilla-spaces/stuff.html', '/contact/spaces/'),
    url_test('/about/contact/stuff.html', '/contact/spaces/'),
    url_test('/contribute/local/', '/contact/communities/'),
    url_test('/contribute/local/northamerica.html', '/contact/communities/north-america/'),
    url_test('/contribute/local/europe.html', '/contact/communities/europe/'),
    url_test('/contribute/local/latinamerica.html', '/contact/communities/latin-america/'),
    url_test('/contribute/local/africamideast.html', '/contact/communities/africa-middle-east/'),
    url_test('/contribute/local/asia.html', '/contact/communities/asia-south-pacific/'),
    url_test('/contribute/local/southpole.html', '/contact/communities/antarctica/'),

    # bug 875052
    url_test('/about/get-involved/whanot/', '/contribute/'),

    # bug 1155870
    url_test('/firefox/os/{releases,notes}/',
             'https://developer.mozilla.org/Firefox_OS/Releases'),
    url_test('/firefox/os/{release,}notes/2.0/',
             'https://developer.mozilla.org/Firefox_OS/Releases/2.0'),

    # bug 878871
    url_test('/firefoxos/is.great/', '/firefox/os/'),

    # bug 831810 & 1142583
    url_test('/{mwc,MWC}/', '/firefox/partners/', query={
        'utm_campaign': 'mwc-redirect',
        'utm_medium': 'referral',
        'utm_source': 'mozilla.org',
    }),

    # bug 878926
    url_test('/{de/,}firefoxflicks/{,stuff}',
             'https://firefoxflicks.mozilla.org/{de/,}{,stuff}'),

    # bug 849426
    url_test('/about/history.html', '/about/history/'),
    url_test('/about/bookmarks.html', 'https://wiki.mozilla.org/Historical_Documents'),
    url_test('/about/timeline.html', 'https://wiki.mozilla.org/Timeline'),

    # bug 1016400
    url_test('/about/careers.html', 'https://careers.mozilla.org/'),

    # bug 861243 and bug 869489
    url_test('/about/manifesto.html', '/about/manifesto/'),
    url_test('/about/manifesto.{de,pt-BR}.html', '/{de,pt-BR}/about/manifesto/'),

    # bug 856077
    url_test('/projects/toolkit/', 'https://developer.mozilla.org/docs/Toolkit_API'),

    # bug 877165
    url_test('/firefox/connect/random/stuff', '/'),

    # bug 657049
    url_test('/firefox/accountmanager/', '/persona/'),

    # bug 841846
    url_test('/firefox/nightly/', 'https://nightly.mozilla.org/'),

    # bug 1209720
    url_test('/thunderbird/releasenotes' '/thunderbird/notes/'),

    url_test('/rhino/download.html',
             'https://developer.mozilla.org/docs/Mozilla/Projects/Rhino/Download_Rhino'),
    url_test('/rhino/doc.html',
             'https://developer.mozilla.org/docs/Mozilla/Projects/Rhino/Documentation'),
    url_test('/rhino/random/stuff/', 'https://developer.mozilla.org/docs/Mozilla/Projects/Rhino'),

    # Bug 730488 deprecate /firefox/all-older.html
    url_test('/firefox/all-older.html', '/firefox/new/'),

    # Bug 1209643
    url_test('/legal/bylaws_amendment_1.html', '/foundation/documents/bylaws-amendment-1/'),
    url_test('/legal/bylaws_amendment_2.html', '/foundation/documents/bylaws-amendment-2/'),
    url_test('/legal/articles.html', '/foundation/documents/articles-of-incorporation/'),
    url_test('/legal/amendment.html', '/foundation/documents/articles-of-incorporation/amendment/'),
    url_test('/legal/bylaws.html', '/foundation/documents/bylaws/'),

    # bug 1211007
    url_test('/thunderbird/download', '/thunderbird/'),

    # bug 1211907
    url_test('/firefox/independent', '/firefox/new/'),
    url_test('/firefox/personal', '/firefox/new/'),

    # bug 960689, 1013349, 896474
    url_test('/about/legal.html', '/about/legal/'),
    url_test('/about/partnerships.html', '/about/partnerships/'),

    # bug 846362
    url_test('/community/{index{.{de,fr},}.html,}', '/contribute/'),

    # bug 1003703, 1009630
    url_test('/firefox/42.0/firstrun/eu/', '/firefox/42.0/firstrun/', query={
        'utm_source': 'direct',
        'utm_medium': 'none',
        'utm_campaign': 'redirect',
        'utm_content': 'eu-firstrun-redirect',
    }),

    # bug 845983
    url_test('/metrofirefox/random/stuff/', '/firefox/random/stuff/'),

    # bug 860532 - Reidrects for governance pages
    url_test('/about/governance.html', '/about/governance/'),
    url_test('/about/roles.html', '/about/governance/roles/'),
    url_test('/about/organizations.html', '/about/governance/organizations/'),

    # bug 876233
    url_test('/about/participate/', '/contribute/'),

    # bug 790784
    url_test('/{about/policies/,foundation/,}privacy-policy{/,.html,}', '/privacy/websites/'),
    url_test('/privacy-policy.pdf',
             'https://static.mozilla.com/moco/en-US/pdf/mozilla_privacypolicy.pdf'),

    # bug 1074354
    url_test('/legal/', '/about/legal/'),

    # bug 963816
    url_test('/legal/privacy/', '/privacy/'),
    url_test('/legal/privacy/firefox{/,.html}', '/privacy/firefox/'),
    url_test('/legal/privacy/oct-2006', '/privacy/archive/firefox/2006-10/'),
    url_test('/legal/privacy/june-2008', '/privacy/archive/firefox/2008-06/'),
    url_test('/legal/privacy/jan-2009', '/privacy/archive/firefox/2009-01/'),
    url_test('/legal/privacy/sept-2009', '/privacy/archive/firefox/2009-09/'),
    url_test('/legal/privacy/jan-2010', '/privacy/archive/firefox/2010-01/'),
    url_test('/legal/privacy/dec-2010', '/privacy/archive/firefox/2010-12/'),
    url_test('/legal/privacy/june-2011', '/privacy/archive/firefox/2011-06/'),
    url_test('/legal/privacy/june-2012', '/privacy/archive/firefox/2012-06/'),
    url_test('/legal/privacy/sept-2012', '/privacy/archive/firefox/2012-09/'),
    url_test('/legal/privacy/dec-2012', '/privacy/archive/firefox/2012-12/'),
    url_test('/legal/privacy/firefox-third-party', '/privacy/archive/firefox/third-party/'),
    url_test('/legal/privacy/notices-firefox', '/legal/firefox/'),
    url_test('/privacy/policies/{facebook,firefox-os,websites}/',
             '/privacy/{facebook,firefox-os,websites}/'),

    # bug 1034859
    url_test('/en-US/about/buttons/dude.jpg', '/media/img/careers/buttons/dude.jpg'),

    # bug 1003737
    url_test('/de/impressum/', '/de/about/legal/impressum/'),

    # bug 960543
    url_test('/firefox/{2,3}.0/eula/random/stuff/', '/legal/eula/firefox-{2,3}/'),

    # bug 724633 - Porting foundation pages
    # Add redirects for the pdfs that were under /foundation/documents/
    # that will now be served from static.mozilla.com/foundation/documents/
    # (The links within the foundation pages have been updated, but there are
    # probably many links to them from other pages and sites that need to keep
    # working.)
    url_test('/foundation/documents/random-stuff.pdf',
             'https://static.mozilla.com/foundation/documents/random-stuff.pdf'),
    url_test('/foundation/donate_form.pdf',
             'https://static.mozilla.com/foundation/documents/donate_form.pdf'),

    # openwebfund/ and openwebfund/index.html redirect to another site.  Careful because
    # there are other pages under openwebfund that still need to be served from Bedrock.
    url_test('/foundation/openwebfund/',
             'https://sendto.mozilla.org/page/contribute/join-mozilla?source=owf_redirect'),
    url_test('/foundation/donate.html',
             'https://sendto.mozilla.org/page/contribute/openwebfund'),

    # FIXUPs for changing foo/bar.html to foo/bar/
    # Redirect foundation/foo.html to foundation/foo/, with a redirect for the nice search engines
    url_test('/foundation/{about,careers,licensing,moco,mocosc}.html',
             '/foundation/{about,careers,licensing,moco,mocosc}/'),
    # Redirect foundation/anything/foo.html to foundation/anything/foo/,
    # with a redirect for the nice search engines
    url_test('/foundation/{annualreport,documents,feed-icon-guidelines,'
             'licensing,openwebfund,trademarks}/random-stuff.html',
             '/foundation/{annualreport,documents,feed-icon-guidelines,'
             'licensing,openwebfund,trademarks}/random-stuff/'),
    url_test('/foundation/documents/{index,mozilla-2002-financial-faq}.html',
             '/foundation/{index,mozilla-2002-financial-faq}/'),

    # bug 442671
    url_test('/foundation/trademarks/l10n-policy/', '/foundation/trademarks/'),

    # Bug 1186373
    url_test('/firefox/hello/npssurvey/',
             'https://www.surveygizmo.com/s3/2227372/Firefox-Hello-Product-Survey',
             status_code=302),

    # Bug 1221739
    url_test('/firefox/hello/feedbacksurvey/',
             'https://www.surveygizmo.com/s3/2319863/d2b7dc4b5687',
             status_code=302),
))
