from bedrock.redirects.util import redirect, ua_redirector


def to_uppercase(url):
    def decider(request, **kwargs):
        kwargs = {k: v.upper() for k, v in kwargs.items() if k != 'locale'}
        return url.format(**kwargs)

    return decider


redirectpatterns = (
    # bug 755826
    redirect('^zh-CN/?$', 'http://firefox.com.cn/', locale_prefix=False),

    # bug 764261, 841393, 996608, 1008162, 1067691, 1113136, 1119022, 1131680, 1115626
    redirect('^zh-TW/?$', 'http://mozilla.com.tw/', locale_prefix=False),
    redirect('^zh-TW/mobile/?', 'http://mozilla.com.tw/firefox/mobile/', locale_prefix=False),
    redirect('^zh-TW/download/?', 'http://mozilla.com.tw/firefox/download/', locale_prefix=False),

    # bug 1013082
    redirect('^ja/?$', 'http://www.mozilla.jp/', locale_prefix=False),

    # bug 1051686
    redirect('^ja/firefox/organizations/?$', 'http://www.mozilla.jp/business/downloads/',
             locale_prefix=False),

    # bug 874913
    redirect('products/download.html', 'firefox.new', anchor='download-fx'),

    # bug 845580
    redirect('^home/?$', 'firefox.new'),

    # bug 948605
    redirect('^firefox/xp', 'firefox.new'),

    # bug 857246 redirect /products/firefox/start/  to start.mozilla.org
    redirect('^products/firefox/start/?$', 'http://start.mozilla.org'),

    # bug 875052
    redirect('^start/', ua_redirector('seamonkey',
                                      'http://www.seamonkey-project.org/start/',
                                      'firefox.new'), vary='User-Agent'),

    # bug 856081 redirect /about/drivers https://wiki.mozilla.org/Firefox/Drivers
    redirect('^about/drivers(\.html|/)?$', 'https://wiki.mozilla.org/Firefox/Drivers'),

    # community
    # bug 885797
    redirect('^community/(directory|wikis|blogs|websites)\.html$',
             'https://wiki.mozilla.org/Websites/Directory', locale_prefix=False),

    # bug 885856
    redirect('^projects/index\.(de|fr|hr|sq).html$', '/{}/firefox/products/',
             locale_prefix=False),

    # bug 856075
    redirect('^projects/technologies\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Using_Mozilla_code_in_other_projects',
             locale_prefix=False),

    # bug 787269
    redirect('^projects/security/components/signed-script(?:s|-example)\.html$',
             'https://developer.mozilla.org/docs/Bypassing_Security_Restrictions_and_Signing_Code'),

    # bug 874526, 877698
    redirect('^projects/security/components(?P<path>.*)$',
             'http://www-archive.mozilla.org/projects/security/components{path}'),

    # bug 876889
    redirect('^projects/testopia/?',
             'https://developer.mozilla.org/docs/Mozilla/Bugzilla/Testopia'),

    # bug 874525
    redirect(r'^projects/security/pki/(?P<match>[nj])ss',
             to_uppercase('https://developer.mozilla.org/docs/{match}SS')),

    # bug 866190
    redirect('^projects/security/pki/python-nss/?$',
             'https://developer.mozilla.org/docs/Python_binding_for_NSS'),

    # bug 1043035
    redirect('^projects/security/pki(?:/|/index\.html)?$',
             'https://developer.mozilla.org/docs/PKI'),
    redirect('^projects/security/pki/pkcs11',
             'https://developer.mozilla.org/docs/Mozilla/Projects/NSS#PKCS_.2311_information'),
    redirect('^projects/security/pki/psm',
             'https://developer.mozilla.org/docs/Mozilla/Projects/PSM'),
    redirect('^projects/security/pki/src',
             'https://developer.mozilla.org/docs/Mozilla/Projects/NSS/NSS_Sources_Building_Testing'),

    # bug 975476
    redirect('^projects/security/pki/python-nss/doc/api/current/html(?P<path>.*)$',
             'https://mozilla.github.io/python-nss-docs{path}'),

    # bug 780672
    redirect('^firefox/webhero', 'firefox.new'),

    # bug 964107
    redirect('^firefox/video', 'https://www.youtube.com/firefoxchannel'),

    # bug 948520
    redirect('^firefox/livebookmarks',
             'https://support.mozilla.org/kb/Live%20Bookmarks'),

    # bug 782333
    redirect('^firefox/backtoschool/?$',
             'https://addons.mozilla.org/firefox/collections/mozilla/back-to-school/'),
    redirect('^firefox/backtoschool/firstrun/?$', 'firefox.firstrun'),

    # bug 824126, 837942
    redirect('^ports/qtmozilla(?:/|/index.html)?$', 'https://wiki.mozilla.org/Qt'),
    redirect('^ports/os2/?$', 'https://wiki.mozilla.org/Ports/os2'),
    redirect('^ports(?P<path>.*)', 'http://www-archive.mozilla.org/ports{path}'),

    redirect(r'^b2g', 'firefox.partners.index'),

    # Bug 781914
    redirect(r'^contribute/areas.html$', 'mozorg.contribute'),
    redirect(r'^contribute/universityambassadors',
             'mozorg.contribute.studentambassadors.landing'),

    # Bug 1144949
    redirect(r'^contribute/page/?$',
             'https://wiki.mozilla.org/Webdev/GetInvolved/mozilla.org'),

    # Bug 763665, 1148127
    redirect(r'^projects/?$', 'firefox.family.index'),


    # Bug 792185 Brand Toolkit -> Style Guide
    redirect(r'^firefox/brand/?$', 'styleguide.home'),
    redirect(r'^firefox/brand/platform/?$',
             'styleguide.identity.firefox-family-platform'),
    redirect(r'^firefox/brand/identity/?$',
             'styleguide.identity.firefox-branding'),
    redirect(r'^firefox/brand/identity/channel-logos/?$',
             'styleguide.identity.firefox-channels'),
    redirect(r'^firefox/brand/identity/wordmarks/?$',
             'styleguide.identity.firefox-wordmarks'),
    redirect(r'^firefox/brand/identity/typefaces/?$',
             'styleguide.communications.typefaces'),
    redirect(r'^firefox/brand/artwork/?$', 'styleguide.home'),
    redirect(r'^firefox/brand/artwork/gear/?$', 'styleguide.home'),
    redirect(r'^firefox/brand/website/?$',
             'styleguide.websites.sandstone-intro'),
    redirect(r'^firefox/brand/website/domain-strategy/?$',
             'styleguide.websites.domains-overview'),
    redirect(r'^firefox/brand/copy/?$', 'styleguide.communications.copy-tone'),
    redirect(r'^firefox/brand/copy/l10n/?$',
             'styleguide.communications.translation'),
    redirect(r'^firefox/brand/copy/rules/?$',
             'styleguide.communications.copy-rules'),
    redirect(r'^firefox/brand/downloads/?$', 'styleguide.home'),

    # Bug 1186373
    redirect(r'^firefox/hello/npssurvey/?$',
             'https://www.surveygizmo.com/s3/2227372/Firefox-Hello-Product-Survey',
             permanent=False),

    # Bug 1071318
    redirect(r'^firefox/mobile/?$', 'firefox.android.index'),

    # Bug 804810 Identity Guidelines -> Style Guide
    redirect(r'^foundation/identity-guidelines/index.html', 'styleguide.home'),
    redirect(r'^foundation/identity-guidelines/mozilla-foundation.html',
             'styleguide.identity.mozilla-branding'),
    redirect(r'^foundation/identity-guidelines/thunderbird.html',
             'styleguide.identity.thunderbird-logo'),

    # Bug 945474 - delete Marketplace marketing product page
    # and redirect
    redirect(r'^apps/?$', 'https://marketplace.firefox.com/'),

    # Bug 800467 /apps/partners ->
    # marketplace.firefox.com/developers
    redirect(r'apps/partners/?$',
             'https://marketplace.firefox.com/developers/'),

    # Bug 815527 /m/privacy.html -> /privacy/firefox/
    redirect(r'^m/privacy.html$', 'privacy.notices.firefox'),

    # Bug 1109318 /privacy/you -> privacy/tips/
    redirect(r'^privacy/you/?$',
             'privacy.privacy-day'),

    # Bug 821047 /about/mission.html -> /mission/
    redirect(r'^about/mission.html$', '/mission/'),

    # Bug 1171763 - delete researchers and projects and redirect
    redirect(r'^research/.+', '/research/'),

    # Bug 800298 /webmaker/ -> wm.o and /webmaker/videos/ ->
    # wm.o/videos/
    redirect(r'webmaker/?$', 'https://webmaker.org'),
    redirect(r'webmaker/videos/?$', 'https://webmaker.org/videos/'),

    # Bug 819317 /gameon/ -> gameon.m.o
    redirect(r'gameon/?$', 'https://gameon.mozilla.org'),

    # Bug 822817 /telemetry/ ->
    # https://wiki.mozilla.org/Telemetry/FAQ
    redirect(r'telemetry/?$', 'https://wiki.mozilla.org/Telemetry/FAQ'),

    # Bug 854561 - move /projects/mozilla-based/ to
    # /about/mozilla-based/
    redirect(r'^projects/mozilla-based/?$', '/about/mozilla-based/'),

    # Bug 867773 - Redirect the Persona "Developer FAQ" link
    # to MDN
    redirect(r'^persona/developer-faq/?$',
             'https://developer.mozilla.org/persona'),

    # Bug 981176 - For now we'll hard-code a redirect to 1.3
    # In the future this should automatically go to the
    # latest version's notes
    redirect(r'^firefox/os/notes/?$', '/firefox/os/notes/1.3/'),

    # Bug 896585 - Send /contact/ to the spaces landing
    redirect(r'^contact/?$', '/contact/spaces/'),

    # Bug 997577 - /legal/ -> /about/legal/
    redirect(r'^legal/fraud-report/?$', '/about/legal/fraud-report/'),
    redirect(r'^legal/eula/?$', '/about/legal/eula/'),
    redirect(r'^legal/eula/firefox-2/?$', '/about/legal/eula/firefox-2/'),
    redirect(r'^legal/eula/firefox-3/?$', '/about/legal/eula/firefox-3/'),

    # Bug 1073269 /dnt/ -> /firefox/dnt/
    redirect(r'^dnt/?$', 'firefox.dnt'),

    # bug 832348 **/index.html -> **/
    redirect('^(.*)/index.html$', '/{}/', locale_prefix=False),

    # bug 845988 - remove double slashes in URLs
    redirect('^(.*)//(.*)$', '/{}/{}', locale_prefix=False),
)
