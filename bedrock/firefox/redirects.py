from bedrock.redirects.util import redirect, is_firefox_redirector, no_redirect


def firefox_mobile_faq(request, *args, **kwargs):
    qs = request.META.get('QUERY_STRING', '')
    if 'os=firefox-os' in qs:
        return 'https://support.mozilla.org/products/firefox-os'

    return 'firefox.android.faq'


redirectpatterns = (
    # overrides
    redirect('^zh-TW/mobile/?', 'http://mozilla.com.tw/firefox/mobile/', locale_prefix=False),
    redirect('^zh-TW/download/?', 'http://mozilla.com.tw/firefox/download/', locale_prefix=False),

    redirect(r'^firefox/aurora/all/?$', 'firefox.all', to_kwargs={'channel': 'developer'}),

    # bug 831810 & 1142583 & 1239960
    redirect(r'^mwc/?$', 'firefox.os.devices', re_flags='i', query={
        'utm_campaign': 'mwc-redirect',
        'utm_medium': 'referral',
        'utm_source': 'mozilla.org',
    }),

    # bug 748503
    redirect(r'^projects/firefox/[^/]+a[0-9]+/(?:firstrun|whatsnew)(?P<p>.*)$',
             '/firefox/nightly/firstrun{p}'),

    # bug 840814
    redirect(r'^projects/firefox'
             r'(?P<version>/(?:\d+\.\d+\.?(?:\d+)?\.?(?:\d+)?(?:[a|b]?)(?:\d*)(?:pre)?(?:\d)?))'
             r'(?P<page>/(?:firstrun|whatsnew))'
             r'(?P<rest>/.*)?$', '/firefox{version}{page}{rest}'),

    # bug 877165
    redirect(r'^firefox/connect', 'mozorg.home'),

    # bug 657049, 1238851
    redirect(r'^firefox/accountmanager/?$', 'https://developer.mozilla.org/Persona'),

    # bug 841846
    redirect(r'^firefox/nightly/?$', 'https://nightly.mozilla.org/'),

    # Bug 1009247, 1101220
    redirect(r'^((firefox|mobile)/)?beta/?$', 'firefox.channel', anchor='beta'),
    redirect(r'^((firefox|mobile)/)?aurora/?$', 'firefox.channel', anchor='developer'),

    # bug 988044
    redirect(r'^firefox/unsupported-systems\.html$', 'firefox.unsupported-systems'),

    # bug 736934, 860865, 1101220, 1153351
    redirect(r'^mobile/(?P<channel>(?:beta|aurora)/)?notes/?$',
             '/firefox/android/{channel}notes/'),
    redirect(r'^firefox/(?P<channel>(?:beta|aurora|organizations)/)?system-requirements(\.html)?$',
             '/firefox/{channel}system-requirements/'),

    # bug 1155870
    redirect(r'^firefox/os/(releases|notes)/?$',
             'https://developer.mozilla.org/Firefox_OS/Releases'),
    redirect(r'^firefox/os/(?:release)?notes/(?P<v>[^/]+)/?$',
             'https://developer.mozilla.org/Firefox_OS/Releases/{v}'),

    # bug 878871
    redirect(r'^firefoxos', '/firefox/os/'),

    # Bug 1006616
    redirect(r'^download/?$', 'firefox.new'),

    # bug 837883
    redirect(r'^firefox/firefox\.exe$', 'mozorg.home', re_flags='i'),

    # bug 821006
    redirect(r'^firefox/all(\.html)?$', 'firefox.all'),

    # bug 727561
    redirect(r'^firefox/search(?:\.html)?$', 'firefox.new'),

    # bug 860865, 1101220
    redirect(r'^firefox/all-(?:beta|rc)(?:/|\.html)?$', 'firefox.all',
             to_kwargs={'channel': 'beta'}),
    redirect(r'^firefox/all-aurora(?:/|\.html)?$', 'firefox.all',
             to_kwargs={'channel': 'developer'}),
    redirect(r'^firefox/aurora/(?P<page>all|notes|system-requirements)/?$',
             '/firefox/developer/{page}/'),
    redirect(r'^firefox/organizations/all\.html$', 'firefox.all',
             to_kwargs={'channel': 'organizations'}),

    # bug 729329
    redirect(r'^mobile/sync', 'firefox.sync'),

    # bug 882845
    redirect(r'^firefox/toolkit/download-to-your-devices', 'firefox.new'),

    # bug 1014823
    redirect(r'^(products/)?firefox/releases/whatsnew/?$', 'firefox.whatsnew'),

    # bug 929775
    redirect(r'^firefox/update', 'firefox.new', query={
        'utm_source': 'firefox-browser',
        'utm_medium': 'firefox-browser',
        'utm_campaign': 'firefox-update-redirect',
    }),

    # Bug 868182, 986174
    redirect(r'^(m|(firefox/)?mobile)/features/?$', 'firefox.android.index'),
    redirect(r'^(m|(firefox/)?mobile)/faq/?$', firefox_mobile_faq, query=False),

    # bug 884933
    redirect(r'^(m|(firefox/)?mobile)/platforms/?$',
             'https://support.mozilla.org/kb/will-firefox-work-my-mobile-device'),

    redirect(r'^m/?$', 'firefox.new'),

    # Bug 730488 deprecate /firefox/all-older.html
    redirect(r'^firefox/all-older\.html$', 'firefox.new'),

    # bug 1120658
    redirect(r'^seamonkey-transition\.html$',
             'http://www-archive.mozilla.org/seamonkey-transition.html'),

    # bug 1121082
    redirect(r'^hello/?$', 'firefox.hello'),

    # Bug 1186373
    redirect(r'^firefox/hello/npssurvey/?$',
             'https://www.surveygizmo.com/s3/2227372/Firefox-Hello-Product-Survey',
             permanent=False),

    # Bug 1221739
    redirect(r'^firefox/hello/feedbacksurvey/?$',
             'https://www.surveygizmo.com/s3/2319863/d2b7dc4b5687',
             permanent=False),

    # bug 1148127
    redirect(r'^products/?$', 'firefox.family.index'),

    # Bug 1110927
    redirect(r'^(products/)?firefox/start/central\.html$', 'firefox.new'),
    redirect(r'^firefox/sync/firstrun\.html$', 'firefox.sync'),
    redirect(r'^firefox/panorama/?$', 'https://support.mozilla.org/kb/tab-groups-organize-tabs'),

    # Bug 920212
    redirect(r'^firefox/fx/?$', 'firefox.new'),

    # Bug 979670, 979531, 1003727, 979664, 979654, 979660
    redirect(r'^firefox/(.+/)?features/?$', 'firefox.desktop.index'),
    redirect(r'^firefox/customize/?$', 'firefox.desktop.customize'),
    redirect(r'^firefox/(?:performance|happy|speed|memory)/?$', 'firefox.desktop.fast'),
    redirect(r'^firefox/security/?$', 'firefox.desktop.trust'),
    redirect(r'^firefox/technology/?$', 'https://developer.mozilla.org/docs/Tools'),

    # Bug 979527
    redirect(r'^(products/)?firefox/central(/|\.html)$', is_firefox_redirector(
        'https://support.mozilla.org/kb/get-started-firefox-overview-main-features',
        'firefox.new'), cache_timeout=0),

    # bug 868169
    redirect(r'^mobile/android-download\.html$',
             'https://play.google.com/store/apps/details',
             query={'id': 'org.mozilla.firefox'}, merge_query=True),
    redirect(r'^mobile/android-download-beta\.html$',
             'https://play.google.com/store/apps/details',
             query={'id': 'org.mozilla.firefox_beta'}, merge_query=True),

    # bug 675031
    redirect(r'^projects/fennec(?P<page>/[\/\w\.-]+)?',
             'http://website-archive.mozilla.org/www.mozilla.org/fennec_releasenotes/projects/fennec{page}'),

    # bug 876581
    redirect(r'^firefox/phishing-protection(/?)$',
             'https://support.mozilla.org/kb/how-does-phishing-and-malware-protection-work'),

    # bug 1006079
    redirect(r'^mobile/home/?(?:index.html)?$',
             'https://blog.mozilla.org/services/2012/08/31/retiring-firefox-home/'),

    # bug 949562
    redirect(r'^mobile/home/1\.0/releasenotes(?:/(?:index.html)?)?$',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_home/mobile/home/1.0/releasenotes/'),
    redirect(r'^mobile/home/1\.0\.2/releasenotes(?:/(?:index.html)?)?$',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_home/mobile/home/1.0.2/releasenotes/'),
    redirect(r'^mobile/home/faq(?:/(?:index.html)?)?$',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_home/mobile/home/faq/'),

    # bug 960064
    redirect(r'^firefox/(?P<num>vpat-[.1-5]+)(?:\.html)?$',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_vpat/firefox-{num}.html'),
    redirect(r'^firefox/vpat(?:\.html)?',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_vpat/firefox-vpat-3.html'),

    # bug 1017564
    redirect(r'^mobile/.+/system-requirements/?$',
             'https://support.mozilla.org/kb/will-firefox-work-my-mobile-device'),

    # bug 858315
    redirect(r'^projects/devpreview/firstrun(?:/(?:index.html)?)?$', '/firefox/firstrun/'),
    redirect(r'^projects/devpreview/(?P<page>[\/\w\.-]+)?$',
             'http://website-archive.mozilla.org/www.mozilla.org/devpreview_releasenotes/projects/devpreview/{page}'),

    # bug 1001238, 1025056
    no_redirect(r'^firefox/(24\.[5678]\.\d|28\.0)/releasenotes/?$'),

    # bug 947890, 1069902
    redirect(r'^firefox/releases/(?P<v>[01]\.(?:.*))$',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_releasenotes/en-US/firefox/releases/{v}'),
    redirect(r'^(?P<path>(?:firefox|mobile)/(?:\d)\.(?:.*)/releasenotes(?:.*))$',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_releasenotes/en-US/{path}'),
    #
    # bug 988746, 989423, 994186, 1153351
    redirect(r'^mobile/(?P<v>2[38]\.0(?:\.\d)?|29\.0(?:beta|\.\d)?)/releasenotes/?$',
             '/firefox/android/{v}/releasenotes/'),
    redirect(r'^mobile/(?P<v>[3-9]\d\.\d(?:a2|beta|\.\d)?)/(?P<p>aurora|release)notes/?$',
             '/firefox/android/{v}/{p}notes/'),

    # bug 1041712, 1069335, 1069902
    redirect(r'^(?P<prod>firefox|mobile)/(?P<vers>([0-9]|1[0-9]|2[0-8])\.(\d+(?:beta|a2|\.\d+)?))'
             r'/(?P<channel>release|aurora)notes/(?P<page>[\/\w\.-]+)?$',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_releasenotes/en-US'
             '/{prod}/{vers}/{channel}notes/{page}'),

    # bug 767614 superceeded by bug 957711 and 1003718 and 1239960
    redirect(r'^(mobile|fennec)/?$', 'firefox.family.index'),

    # bug 876668
    redirect(r'^mobile/customize(?:/.*)?$', '/firefox/android/'),

    # bug 1211907
    redirect(r'^firefox/independent/?$', 'firefox.new'),
    redirect(r'^firefox/personal/?$', 'firefox.new'),

    # bug 845983
    redirect(r'^metrofirefox(?P<path>/.*)?$', '/firefox{path}'),

    # bug 1003703, 1009630
    redirect(r'^firefox(?P<vers>/.+)/firstrun/eu/?$', '/firefox{vers}/firstrun/', query={
        'utm_source': 'direct',
        'utm_medium': 'none',
        'utm_campaign': 'redirect',
        'utm_content': 'eu-firstrun-redirect',
    }),

    # bug 960543
    redirect(r'^firefox/(?P<vers>[23])\.0/eula', '/legal/eula/firefox-{vers}/'),

    # bug 1224060
    redirect(
        r'^ja/firefox/ios/(?P<vers>[0-9]+(\.[0-9]+)*)/(?P<file>releasenotes|system-requirements)',
        'http://www.mozilla.jp/firefox/ios/{vers}/{file}/', locale_prefix=False),

    # bug 1150713
    redirect(r'^firefox/sms(?:/.*)?$', '/firefox/products/'),

    # Redirects for SeaMonkey project website, now living at seamonkey-project.org
    redirect(r'^projects/seamonkey/$', 'http://www.seamonkey-project.org/'),
    redirect(r'^projects/seamonkey/artwork\.html$',
             'http://www.seamonkey-project.org/dev/artwork'),
    redirect(r'^projects/seamonkey/community\.html$',
             'http://www.seamonkey-project.org/community'),
    redirect(r'^projects/seamonkey/get-involved\.html$',
             'http://www.seamonkey-project.org/dev/get-involved'),
    redirect(r'^projects/seamonkey/index\.html$', 'http://www.seamonkey-project.org/'),
    redirect(r'^projects/seamonkey/news\.html$', 'http://www.seamonkey-project.org/news'),
    redirect(r'^projects/seamonkey/project-areas\.html$',
             'http://www.seamonkey-project.org/dev/project-areas'),
    redirect(r'^projects/seamonkey/releases/$', 'http://www.seamonkey-project.org/releases/'),
    redirect(r'^projects/seamonkey/releases/index\.html$',
             'http://www.seamonkey-project.org/releases/'),
    redirect(r'^projects/seamonkey/review-and-flags\.html$',
             'http://www.seamonkey-project.org/dev/review-and-flags'),
    redirect(r'^projects/seamonkey/releases/(?P<vers>1\..*)\.html$',
             'http://www.seamonkey-project.org/releases/{vers}'),
    redirect(r'^projects/seamonkey/releases/seamonkey(?P<x>.*)/index.html$',
             'http://www.seamonkey-project.org/releases/seamonkey{x}/'),
    redirect(r'^projects/seamonkey/releases/seamonkey(?P<x>.*/.*).html$',
             'http://www.seamonkey-project.org/releases/seamonkey{x}'),
    redirect(r'^projects/seamonkey/releases/updates/(?P<x>.*)$',
             'http://www.seamonkey-project.org/releases/updates/{x}'),
    redirect(r'^projects/seamonkey/start/$', 'http://www.seamonkey-project.org/start/'),

    # Bug 638948 redirect beta privacy policy link
    redirect(r'^firefox/beta/feedbackprivacypolicy/?$', '/privacy/firefox/'),

    # Bug 1238248
    redirect(r'^firefox/push/?$',
             'https://support.mozilla.org/kb/push-notifications-firefox'),

    # Bug 1239960
    redirect(r'^firefox/partners/?$', 'firefox.os.index'),

    # Bug 1243060
    redirect(r'^firefox/tiles/?$',
             'https://support.mozilla.org/kb/about-tiles-new-tab'),

    # Bug 1239863
    redirect(r'^firefox/os/1\.1/?$', 'firefox.os.index'),
    redirect(r'^firefox/os/1\.3/?$', 'firefox.os.index'),
    redirect(r'^firefox/os/1\.3t/?$', 'firefox.os.index'),
    redirect(r'^firefox/os/1\.4/?$', 'firefox.os.index'),
    redirect(r'^firefox/os/2\.0/?$', 'firefox.os.index'),
    redirect(r'^firefox/os/2\.5/?$', 'firefox.os.index'),
    redirect(r'^firefox/os/faq/?$',
             'https://support.mozilla.org/products/firefox-os'),

    # Bug 1252332
    redirect(r'^sync/?$', 'firefox.sync'),

    # Bug 424204
    redirect(r'^firefox/help/?$', 'https://support.mozilla.com/{locale}kb/'),

    redirect(r'^fxandroid/?$', 'firefox.android.index'),

    # Bug 1255882
    redirect(r'^firefox/personal', 'firefox.new'),
    redirect(r'^firefox/upgrade', 'firefox.new'),
    redirect(r'^firefox/ie', 'firefox.new'),

    # Bug 1255882
    redirect(r'^projects/bonecho/anti-phishing/?$',
             'https://support.mozilla.org/kb/how-does-phishing-and-malware-protection-work'),
    redirect(r'^projects/bonecho(/.*)?$', '/firefox/channel/'),
    redirect(r'^projects/bonsai(/.*)?$', 'https://wiki.mozilla.org/Bonsai'),
    redirect(r'^projects/camino(/.*)?$', 'http://caminobrowser.org/'),
    redirect(r'^projects/cck(/.*)?$', 'https://wiki.mozilla.org/CCK'),
    redirect(r'^projects/chimera(/.*)?$', 'http://caminobrowser.org/'),
    redirect(r'^projects/deerpark(/.*)?$', '/firefox/channel/'),
    redirect(r'^projects/embedding(/.*)?$',
             'https://developer.mozilla.org/en/Embedding_Mozilla'),
    redirect(r'^projects/granparadiso(/.*)?$', '/firefox/channel/'),
    redirect(r'^projects/inspector(/.*)?$',
             'https://developer.mozilla.org/En/DOM_Inspector'),
    redirect(r'^projects/javaconnect(/.*)?$',
             'http://developer.mozilla.org/en/JavaXPCOM'),
    redirect(r'^projects/marketing(/.*)?$',
             'http://contribute.mozilla.org/Marketing'),
    redirect(r'^projects/minefield(/.*)?$',
             'http://www.mozilla.org/projects/firefox/prerelease.html'),
    redirect(r'^projects/minimo(/.*)?$', 'https://wiki.mozilla.org/Mobile'),
    redirect(r'^projects/namoroka(/.*)?$', '/firefox/channel/'),
    redirect(r'^projects/nspr(?:/.*)?$', 'https://developer.mozilla.org/docs/NSPR'),
    redirect(r'^projects/netlib(/.*)?$', 'https://developer.mozilla.org/en/Necko'),
    redirect(r'^projects/plugins(/.*)?$',
             'https://developer.mozilla.org/En/Plugins'),
    redirect(r'^projects/rt-messaging(/.*)?$', 'http://chatzilla.hacksrus.com/'),
    redirect(r'^projects/shiretoko(/.*)?$', '/firefox/channel/'),
    redirect(r'^projects/string(/.*)?$',
             'https://developer.mozilla.org/en/XPCOM_string_guide'),
    redirect(r'^projects/tech-evangelism(/.*)?$',
             'https://wiki.mozilla.org/Evangelism'),
    redirect(r'^projects/venkman(/.*)?$',
             'https://developer.mozilla.org/en/Venkman'),
    redirect(r'^projects/webservices/examples/babelfish-wsdl(/.*)?$',
             'http://developer.mozilla.org/En/XML_Web_Services'),
    redirect(r'^projects/xbl(/.*)?$', 'https://developer.mozilla.org/en/XBL'),
    redirect(r'^projects/xforms(/.*)?$', 'https://developer.mozilla.org/en/XForms'),
    redirect(r'^projects/xpcom(/.*)?$', 'https://developer.mozilla.org/en/XPCOM'),
    redirect(r'^projects/xpinstall(/.*)?$',
             'https://developer.mozilla.org/en/XPInstall'),
    redirect(r'^projects/xslt(/.*)?$', 'https://developer.mozilla.org/en/XSLT'),
    redirect(r'^projects/xul(/.*)?$', 'https://developer.mozilla.org/En/XUL'),
    redirect(r'^quality/help(/.*)?$', 'http://quality.mozilla.org/get-involved'),
    redirect(r'^quality(/.*)?$', 'http://quality.mozilla.org/'),

    # Bug 654614 /blocklist -> addons.m.o/blocked
    redirect(r'^blocklist(/.*)?$', 'https://addons.mozilla.org/blocked/'),


    # bug 857246 redirect /products/firefox/start/  to start.mozilla.org
    redirect(r'^products/firefox/start/?$', 'http://start.mozilla.org'),
    redirect(r'^products/firefox(?P<page>/.*)$', '/firefox{page}'),
)
