from bedrock.redirects.util import (redirect, platform_redirector, no_redirect)


def firefox_mobile_faq(request, *args, **kwargs):
    qs = request.META.get('QUERY_STRING', '')
    if 'os=firefox-os' in qs:
        return 'https://support.mozilla.org/products/firefox-os'

    return 'https://support.mozilla.org/products/mobile'


def firefox_channel(*args, **kwargs):
    return platform_redirector('firefox.channel.desktop',
                               'firefox.channel.android',
                               'firefox.channel.ios')


redirectpatterns = (
    # overrides

    # issue 8096
    redirect(r'^firefox/beta/all/?$', 'firefox.all', anchor='product-desktop-beta'),
    redirect(r'^firefox/developer/all/?$', 'firefox.all', anchor='product-desktop-developer'),
    redirect(r'^firefox/aurora/all/?$', 'firefox.all', anchor='product-desktop-developer'),
    redirect(r'^firefox/nightly/all/?$', 'firefox.all', anchor='product-desktop-nightly'),
    redirect(r'^firefox/organizations/all/?$', 'firefox.all', anchor='product-desktop-esr'),
    redirect(r'^firefox/android/all/?$', 'firefox.all', anchor='product-android-release'),
    redirect(r'^firefox/android/beta/all/?$', 'firefox.all', anchor='product-android-beta'),
    redirect(r'^firefox/android/nightly/all/?$', 'firefox.all', anchor='product-android-nightly'),

    # bug 831810 & 1142583 & 1239960, 1329931
    redirect(r'^mwc/?$', 'https://support.mozilla.org/products/firefox-os', re_flags='i'),

    # bug 748503
    redirect(r'^projects/firefox/[^/]+a[0-9]+/firstrun(?P<p>.*)$',
             '/firefox/nightly/firstrun{p}'),

    # bug 1275483
    redirect(r'^firefox/nightly/whatsnew/?', 'firefox.nightly.firstrun'),

    # bug 840814
    redirect(r'^projects/firefox'
             r'(?P<version>/(?:\d+\.\d+\.?(?:\d+)?\.?(?:\d+)?(?:[a|b]?)(?:\d*)(?:pre)?(?:\d)?))'
             r'(?P<page>/(?:firstrun|whatsnew))'
             r'(?P<rest>/.*)?$', '/firefox{version}{page}{rest}'),

    # bug 877165
    redirect(r'^firefox/connect', 'mozorg.home'),

    # bug 657049, 1238851
    redirect(r'^firefox/accountmanager/?$', 'https://developer.mozilla.org/Persona'),

    # Bug 1009247, 1101220, 1299947, 1314603, 1328409
    redirect(r'^(firefox/)?beta/?$', firefox_channel(), cache_timeout=0, anchor='beta'),
    redirect(r'^(firefox/)?aurora/?$', firefox_channel(), cache_timeout=0, anchor='aurora'),
    redirect(r'^(firefox/)?nightly/?$', firefox_channel(), cache_timeout=0, anchor='nightly'),
    redirect(r'^mobile/beta/?$', 'firefox.channel.android', anchor='beta'),
    redirect(r'^mobile/aurora/?$', 'firefox.channel.android', anchor='aurora'),
    redirect(r'^mobile/nightly/?$', 'firefox.channel.android', anchor='nightly'),

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

    # bug 1438302
    no_redirect(r'^firefox/download/thanks/?$'),

    # Bug 1006616
    redirect(r'^download/?$', 'firefox.new'),

    # Bug 1409554
    redirect(r'^(firefox|mobile)/download', 'firefox.new'),

    # bug 837883
    redirect(r'^firefox/firefox\.exe$', 'mozorg.home', re_flags='i'),

    # bug 821006
    redirect(r'^firefox/all(\.html)?$', 'firefox.all'),

    # bug 727561
    redirect(r'^firefox/search(?:\.html)?$', 'firefox.new'),

    # bug 860865, 1101220, issue 8096
    redirect(r'^firefox/all-(?:beta|rc)(?:/|\.html)?$', 'firefox.all',
             anchor='product-desktop-beta'),
    redirect(r'^firefox/all-aurora(?:/|\.html)?$', 'firefox.all',
             anchor='product-desktop-developer'),
    redirect(r'^firefox/aurora/(?P<page>all|notes|system-requirements)/?$',
             '/firefox/developer/{page}/'),
    redirect(r'^firefox/organizations/all\.html$', 'firefox.all',
             anchor='product-desktop-esr'),

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
    redirect(r'^(m|(firefox/)?mobile)/features/?$', 'firefox.mobile.index'),
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

    # Bug 1186373
    redirect(r'^firefox/hello/npssurvey/?$',
             'https://www.surveygizmo.com/s3/2227372/Firefox-Hello-Product-Survey',
             permanent=False),

    # Bug 1221739
    redirect(r'^firefox/hello/feedbacksurvey/?$',
             'https://www.surveygizmo.com/s3/2319863/d2b7dc4b5687',
             permanent=False),

    # bug 1148127
    redirect(r'^products/?$', 'firefox'),

    # Bug 1110927
    redirect(r'^(products/)?firefox/start/central\.html$', 'firefox.new'),
    redirect(r'^firefox/sync/firstrun\.html$', 'firefox.sync'),

    # Bug 920212
    redirect(r'^firefox/fx(/.*)?', 'firefox'),

    # Bug 979531, 1003727, 979664, 979654, 979660
    redirect(r'^firefox/customize/?$', 'https://support.mozilla.org/kb/customize-firefox-controls-buttons-and-toolbars'),
    redirect(r'^firefox/(?:performance|happy|speed|memory)/?$', 'firefox.features.fast'),
    redirect(r'^firefox/security/?$', 'firefox.features.independent'),
    redirect(r'^firefox/technology/?$', 'https://developer.mozilla.org/docs/Tools'),

    # Previously Bug 979527 / Github #10004 "Getting Started" Page
    redirect(r'^(products/)?firefox/central(/|\.html|-lite\.html)?$', 'firefox'),

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
    redirect(r'^mobile/home/?(?:index\.html)?$',
             'https://blog.mozilla.org/services/2012/08/31/retiring-firefox-home/'),

    # bug 949562
    redirect(r'^mobile/home/1\.0/releasenotes(?:/(?:index\.html)?)?$',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_home/mobile/home/1.0/releasenotes/'),
    redirect(r'^mobile/home/1\.0\.2/releasenotes(?:/(?:index\.html)?)?$',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_home/mobile/home/1.0.2/releasenotes/'),
    redirect(r'^mobile/home/faq(?:/(?:index\.html)?)?$',
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
    redirect(r'^projects/devpreview/firstrun(?:/(?:index\.html)?)?$', '/firefox/firstrun/'),
    redirect(r'^projects/devpreview/(?P<page>[\/\w\.-]+)?$',
             'http://website-archive.mozilla.org/www.mozilla.org/devpreview_releasenotes/projects/devpreview/{page}'),

    # bug 1001238, 1025056
    no_redirect(r'^firefox/(24\.[5678]\.\d|28\.0)/releasenotes/?$'),

    # bug 1235082
    no_redirect(r'^firefox/23\.0(\.1)?/releasenotes/?$'),

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
    redirect(r'^(fennec)/?$', 'firefox'),

    # issue 8749
    redirect(r'^(mobile)/?$', '/firefox/mobile/'),

    # bug 876668
    redirect(r'^mobile/customize(?:/.*)?$', '/firefox/mobile/'),

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

    # bug 1150713
    redirect(r'^firefox/sms(?:/.*)?$', 'firefox'),

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
    redirect(r'^projects/seamonkey/releases/seamonkey(?P<x>.*)/index\.html$',
             'http://www.seamonkey-project.org/releases/seamonkey{x}/'),
    redirect(r'^projects/seamonkey/releases/seamonkey(?P<x>.*/.*)\.html$',
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
    redirect(r'^firefox/partners/?$', 'https://support.mozilla.org/products/firefox-os'),

    # Bug 1243060
    redirect(r'^firefox/tiles/?$',
             'https://support.mozilla.org/kb/about-tiles-new-tab'),

    # Bug 1239863, 1329931
    redirect(r'^firefox/os(/.*)?$', 'https://support.mozilla.org/products/firefox-os'),

    # Bug 1252332
    redirect(r'^sync/?$', 'firefox.sync'),

    # Bug 424204
    redirect(r'^firefox/help/?$', 'https://support.mozilla.org/'),

    redirect(r'^fxandroid/?$', 'firefox.mobile.index'),

    # Bug 1255882
    redirect(r'^firefox/personal', 'firefox.new'),
    redirect(r'^firefox/upgrade', 'firefox.new'),
    redirect(r'^firefox/ie', 'firefox.new'),

    # must go above the bug 1255882 stuff below
    redirect(r'^projects/xul/joy-of-xul\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Tech/XUL/The_Joy_of_XUL'),
    redirect(r'^projects/xul/xre(old)?\.html$',
             'https://developer.mozilla.org/docs/Archive/Mozilla/XULRunner'),
    redirect(r'^projects/xslt/js-interface\.html$',
             'https://developer.mozilla.org/docs/'
             'Web/XSLT/Using_the_Mozilla_JavaScript_interface_to_XSL_Transformations'),
    redirect(r'^projects/xslt/faq\.html$',
             'https://developer.mozilla.org/docs/'
             'Web/API/XSLTProcessor/XSL_Transformations_in_Mozilla_FAQ'),
    redirect(r'^projects/xslt/standalone\.html$',
             'https://developer.mozilla.org/docs/'
             'Archive/Mozilla/Building_TransforMiiX_standalone'),
    redirect(r'^projects/plugins/first-install-problem\.html$',
             'https://developer.mozilla.org/Add-ons/Plugins/The_First_Install_Problem'),
    redirect(r'^projects/plugins/install-scheme\.html$',
             'https://developer.mozilla.org/docs/'
             'Installing_plugins_to_Gecko_embedding_browsers_on_Windows'),
    redirect(r'^projects/plugins/npruntime-sample-in-visual-studio\.html$',
             'https://developer.mozilla.org/docs/'
             'Compiling_The_npruntime_Sample_Plugin_in_Visual_Studio'),
    redirect(r'^projects/plugins/npruntime\.html$',
             'https://developer.mozilla.org/docs/Plugins/Guide/Scripting_plugins'),
    redirect(r'^projects/plugins/plugin-host-control\.html$',
             'https://developer.mozilla.org/docs/'
             'Archive/Mozilla/ActiveX_Control_for_Hosting_Netscape_Plug-ins_in_IE'),
    redirect(r'^projects/plugins/xembed-plugin-extension\.html$',
             'https://developer.mozilla.org/Add-ons/Plugins/XEmbed_Extension_for_Mozilla_Plugins'),
    redirect(r'^projects/netlib/http/http-debugging\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Debugging/HTTP_logging'),
    redirect(r'^projects/netlib/integrated-auth\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Integrated_authentication'),
    redirect(r'^projects/netlib/Link_Prefetching_FAQ\.html$',
             'https://developer.mozilla.org/docs/Web/HTTP/Link_prefetching_FAQ'),
    redirect(r'^projects/embedding/GRE\.html$',
             'https://developer.mozilla.org/docs/Archive/Mozilla/GRE'),
    redirect(r'^projects/embedding/windowAPIs\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Tech/Embedded_Dialog_API'),
    redirect(r'^projects/embedding/howto/config\.html$',
             'https://developer.mozilla.org/docs/Gecko/Embedding_Mozilla/Roll_your_own_browser'),
    redirect(r'^projects/embedding/howto/Initializations\.html$',
             'https://developer.mozilla.org/docs/Gecko/Embedding_Mozilla/Roll_your_own_browser'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasicsTOC\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics#toc'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics2\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics#Why_Gecko'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics3\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics'
             '#What_You_Need_to_Embed'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics4\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics'
             '#Getting_the_Code'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics5\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics'
             '#Understanding_the_Coding_Environment'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics6\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics#XPCOM'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics7\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics#XPIDL'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics8\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics'
             '#XPConnect_and_XPT_files'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics9\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics'
             '#String_classes'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics10\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics#XUL.2FXBL'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics11\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics'
             '#Choosing_Additional_Functionalities'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics12\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics'
             '#What_Gecko_Provides'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics13\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics'
             '#What_You_Provide'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics14\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics'
             '#Common_Embedding_Tasks'),
    redirect(r'^projects/embedding/embedoverview/EmbeddingBasics16\.html$',
             'https://developer.mozilla.org/docs/Mozilla/Gecko/Gecko_Embedding_Basics'
             '#Appendix:_Data_Flow_Inside_Gecko'),
    redirect(r'^projects/embedding/examples/',
             'https://developer.mozilla.org/docs/Gecko/Embedding_Mozilla/Roll_your_own_browser'),

    # Bug 1255882
    redirect(r'^projects/bonecho/anti-phishing/?$',
             'https://support.mozilla.org/kb/how-does-phishing-and-malware-protection-work'),
    redirect(r'^projects/bonecho(/.*)?$', 'firefox.channel.desktop'),
    redirect(r'^projects/bonsai(/.*)?$', 'https://wiki.mozilla.org/Bonsai'),
    redirect(r'^projects/camino(/.*)?$', 'http://caminobrowser.org/'),
    redirect(r'^projects/cck(/.*)?$', 'https://wiki.mozilla.org/CCK'),
    redirect(r'^projects/chimera(/.*)?$', 'http://caminobrowser.org/'),
    redirect(r'^projects/deerpark(/.*)?$', 'firefox.channel.desktop'),
    redirect(r'^projects/embedding/faq\.html$',
             'https://developer.mozilla.org/docs/Gecko/Embedding_Mozilla/FAQ/How_do_I...'),
    redirect(r'^projects/embedding(/.*)?$',
             'https://developer.mozilla.org/docs/Gecko/Embedding_Mozilla'),
    redirect(r'^projects/granparadiso(/.*)?$', 'firefox.channel.desktop'),
    redirect(r'^projects/inspector/faq\.html$',
             'https://developer.mozilla.org/docs/Tools/Add-ons/DOM_Inspector/DOM_Inspector_FAQ'),
    redirect(r'^projects/inspector(/.*)?$',
             'https://developer.mozilla.org/docs/Tools/Add-ons/DOM_Inspector'),
    redirect(r'^projects/javaconnect(/.*)?$',
             'http://developer.mozilla.org/en/JavaXPCOM'),
    redirect(r'^projects/minefield(/.*)?$', 'firefox.channel.desktop'),
    redirect(r'^projects/minimo(/.*)?$', 'https://wiki.mozilla.org/Mobile'),
    redirect(r'^projects/namoroka(/.*)?$', 'firefox.channel.desktop'),
    redirect(r'^projects/nspr(?:/.*)?$', 'https://developer.mozilla.org/docs/NSPR'),
    redirect(r'^projects/netlib(/.*)?$',
             'https://developer.mozilla.org/docs/Mozilla/Projects/Necko'),
    redirect(r'^projects/plugins(/.*)?$', 'https://developer.mozilla.org/Add-ons/Plugins'),
    redirect(r'^projects/rt-messaging(/.*)?$', 'http://chatzilla.hacksrus.com/'),
    redirect(r'^projects/shiretoko(/.*)?$', 'firefox.channel.desktop'),
    redirect(r'^projects/string(/.*)?$',
             'https://developer.mozilla.org/en/XPCOM_string_guide'),
    redirect(r'^projects/tech-evangelism(/.*)?$',
             'https://wiki.mozilla.org/Evangelism'),
    redirect(r'^projects/venkman(/.*)?$',
             'https://developer.mozilla.org/docs/Archive/Mozilla/Venkman'),
    redirect(r'^projects/webservices/examples/babelfish-wsdl(/.*)?$',
             'https://developer.mozilla.org/docs/SOAP_in_Gecko-based_Browsers'),
    redirect(r'^projects/xbl(/.*)?$', 'https://developer.mozilla.org/docs/Mozilla/Tech/XBL'),
    redirect(r'^projects/xforms(/.*)?$', 'https://developer.mozilla.org/docs/Archive/Web/XForms'),
    redirect(r'^projects/xpcom(/.*)?$', 'https://developer.mozilla.org/docs/Mozilla/Tech/XPCOM'),
    redirect(r'^projects/xpinstall(/.*)?$',
             'https://developer.mozilla.org/docs/Archive/Mozilla/XPInstall'),
    redirect(r'^projects/xslt(/.*)?$', 'https://developer.mozilla.org/docs/Web/XSLT'),
    redirect(r'^projects/xul(/.*)?$', 'https://developer.mozilla.org/docs/Mozilla/Tech/XUL'),
    redirect(r'^quality/help(/.*)?$', 'http://quality.mozilla.org/get-involved'),
    redirect(r'^quality(/.*)?$', 'http://quality.mozilla.org/'),

    # Bug 654614 /blocklist -> addons.m.o/blocked
    redirect(r'^blocklist(/.*)?$', 'https://addons.mozilla.org/blocked/'),

    redirect(r'^products/firebird/compare/?$', '/firefox/browsers/compare/'),
    redirect(r'^products/firebird/?$', 'firefox'),
    redirect(r'^products/firebird/download/$', 'firefox.new'),
    redirect(r'^products/firefox/add-engines\.html$',
             'https://addons.mozilla.org/search-engines.php'),
    redirect(r'^products/firefox/all$', '/firefox/all/'),
    redirect(r'^products/firefox/all\.html$', '/firefox/all/'),
    redirect(r'^products/firefox/banners\.html$', '/contribute/friends/'),
    redirect(r'^products/firefox/buttons\.html$', '/contribute/friends/'),
    redirect(r'^products/firefox/download', 'firefox.new'),
    redirect(r'^products/firefox/get$', 'firefox.new'),
    redirect(r'^products/firefox/live-bookmarks', '/firefox/features/'),
    redirect(r'^products/firefox/mirrors\.html$', 'http://www-archive.mozilla.org/mirrors.html'),
    redirect(r'^products/firefox/releases/$', '/firefox/releases/'),
    redirect(r'^products/firefox/releases/0\.9\.2\.html$',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_releasenotes'
             '/en-US/firefox/releases/0.9.1.html'),
    redirect(r'^products/firefox/releases/0\.10\.1\.html$',
             'http://website-archive.mozilla.org/www.mozilla.org/firefox_releasenotes'
             '/en-US/firefox/releases/0.10.html'),
    redirect(r'^products/firefox/search', '/firefox/features/'),
    redirect(r'^products/firefox/shelf\.html$', 'https://blog.mozilla.org/press/awards/'),
    redirect(r'^products/firefox/smart-keywords\.html$',
             'https://support.mozilla.org/en-US/kb/Smart+keywords'),
    redirect(r'^products/firefox/support/$', 'https://support.mozilla.org/'),
    redirect(r'^products/firefox/switch', 'firefox.new'),
    redirect(r'^products/firefox/system-requirements', '/firefox/system-requirements/'),
    redirect(r'^products/firefox/tabbed-browsing', 'firefox'),
    redirect(r'^products/firefox/text-zoom\.html$',
             'https://support.mozilla.org/kb/font-size-and-zoom-increase-size-of-web-pages'),
    redirect(r'^products/firefox/themes$', 'https://addons.mozilla.org/themes/'),
    redirect(r'^products/firefox/themes\.html$', 'https://addons.mozilla.org/themes/'),
    redirect(r'^products/firefox/ui-customize\.html$',
             'https://support.mozilla.org/kb/customize-firefox-controls-buttons-and-toolbars'),
    redirect(r'^products/firefox/upgrade', 'firefox.new'),
    redirect(r'^products/firefox/why/$', 'firefox'),

    # bug 857246 redirect /products/firefox/start/  to start.mozilla.org
    redirect(r'^products/firefox/start/?$', 'http://start.mozilla.org'),

    # issue 9008
    redirect(r'^products/firefox(/.*)?$', 'firefox.products.index'),

    # bug 1260423
    redirect(r'^firefox/choose/?$', 'firefox.new'),

    # bug 1288552 - redirect /secondrun/ traffic from funnelcake test
    redirect(r'^firefox(?:\/\d+\.\d+(?:\.\d+)?(?:a\d+)?)?/secondrun(?:/.*)?',
             'firefox.mobile.index', query=False),

    # bug 1293539
    redirect(r'^firefox(?:\/\d+\.\d+(?:\.\d+)?(?:a\d+)?)?/tour/?$',
             'https://support.mozilla.org/kb/get-started-firefox-overview-main-features'),

    # bug 1295332
    redirect(r'^hello/?$', 'https://support.mozilla.org/kb/hello-status'),
    redirect(r'^firefox/hello/?$', 'https://support.mozilla.org/kb/hello-status'),
    redirect(r'^firefox(?:\/\d+\.\d+(?:\.\d+)?(?:a\d+)?)?/hello/start/?$', 'https://support.mozilla.org/kb/hello-status'),

    # bug 1299947, 1326383
    redirect(r'^firefox/channel/?$', firefox_channel(), cache_timeout=0),

    # Bug 1277196
    redirect(r'^firefox(?:\/\d+\.\d+(?:\.\d+)?(?:a\d+)?)?/firstrun/learnmore/?$', 'firefox.features.index', query={
        'utm_source': 'firefox-browser',
        'utm_medium': 'firefox-browser',
        'utm_campaign': 'redirect',
        'utm_content': 'learnmore-tab',
    }),
    redirect(r'^firefox/windows-10/welcome/?$', 'https://support.mozilla.org/kb/how-change-your-default-browser-windows-10', query={
        'utm_source': 'firefox-browser',
        'utm_medium': 'firefox-browser',
        'utm_campaign': 'redirect',
        'utm_content': 'windows10-welcome-tab',
    }),

    # bug 1369732
    redirect(r'^Firefox/?$', 'firefox'),

    # bug 1386112
    redirect(r'^firefox/android/faq/?', 'https://support.mozilla.org/products/mobile'),

    # bug 1392796
    redirect(r'^firefox/desktop/fast/?', 'firefox.features.fast'),
    redirect(r'^firefox/desktop/trust/?', 'firefox.features.independent'),
    redirect(r'^firefox/desktop/tips/?', 'firefox.features.index'),
    redirect(r'^firefox/desktop/customize/?', 'https://support.mozilla.org/kb/customize-firefox-controls-buttons-and-toolbars'),
    redirect(r'^firefox/private-browsing/?', 'firefox.features.private-browsing'),

    # bug 1405436
    redirect(r'^firefox/organic', '/firefox/'),
    redirect(r'^firefox/landing/better', '/firefox/'),
    redirect(r'^firefox/(new/)?addon', 'https://addons.mozilla.org'),
    redirect(r'^firefox/tips', '/firefox/features/'),
    redirect(r'^firefox/new/.+', '/firefox/new/'),
    redirect(r'^firefox/38\.0\.3/releasenotes/$', '/firefox/38.0.5/releasenotes/'),
    redirect(r'^firefox/default\.htm', '/firefox/'),
    redirect(r'^firefox/android/(?P<version>\d+\.\d+(?:\.\d+)?)$', '/firefox/android/{version}/releasenotes/'),
    redirect(r'^firefox/stats/', '/firefox/'),

    # bug 1416706
    redirect(r'^firefox/desktop/?', 'firefox.new'),

    # bug 1418500
    redirect(r'^firefox/android/?$', 'firefox.mobile.index'),
    redirect(r'^firefox/focus/?$', 'firefox.mobile.index'),
    redirect(r'^firefox/ios/?$', 'firefox.mobile.index'),

    # issue 9502
    redirect(r'^firefox/quantum/?', '/firefox/browsers/quantum/'),

    # bug 1421584, issue 7491
    redirect(r'^firefox/organizations/faq/?$', 'firefox.enterprise.index'),

    # bug 1425865 - Amazon Fire TV goes to SUMO until we have a product page.
    redirect(
        r'^firefox/fire-tv/?$',
        'https://support.mozilla.org/products/firefox-fire-tv/',
        permanent=False,
    ),

    # bug 1430894
    redirect(r'^firefox/interest-dashboard/?', 'https://support.mozilla.org/kb/firefox-add-technology-modernizing'),

    # bug 1419244
    redirect(r'^firefox/mobile-download(/.*)?', 'firefox.mobile.index'),

    # bug 960651, 1436973
    redirect(r'(firefox|mobile)/([^/]+)/details(/|/.+\.html)?$', 'firefox.unsupported-systems',
             locale_prefix=False),
    redirect(r'^firefox/unsupported/', 'firefox.unsupported-systems'),

    # bug 1428783
    redirect(r'^firefox/dnt/?$', 'https://support.mozilla.org/kb/how-do-i-turn-do-not-track-feature'),

    # issue 6209
    redirect(r'^pocket/?', '/firefox/pocket/'),

    # issue 6186
    redirect(r'^vote/?', '/firefox/election/'),

    # issue 9391
    redirect(r'^/firefox/election/?$', 'firefox'),

    # fxa
    redirect(r'^firefox/accounts/features/?', 'firefox.accounts'),

    # issue 9490
    redirect(r'^firefox/features/sync/?', 'firefox.sync'),

    # bug 1577449
    redirect(r'^firefox/features/send-tabs/?', 'https://support.mozilla.org/kb/send-tab-firefox-desktop-other-devices'),

    # issue 6512
    redirect(r'^firefox/firefox\.html$', 'firefox.new'),

    # issue 6979
    redirect(r'^firefoxfightsforyou/?', 'firefox'),

    # issue 7210
    redirect(r'^firefox/account/?$', 'firefox.accounts'),

    # issue 7287
    redirect(r'^accounts/?$', 'firefox.accounts'),

    # issue 7436
    redirect(r'^firefox/feedback/?$', 'https://support.mozilla.org/questions/new/desktop'),

    # issue 7491
    redirect(r'^firefox/organizations/?$', 'firefox.enterprise.index'),

    # issue 7670
    redirect(r'^/firefox/fights-for-you/?', 'firefox'),

    # issue #7424
    redirect(r'^firefox(?:\/\d+\.\d+(?:\.\d+)?(?:a\d+)?)?/content-blocking/start/?$', 'https://support.mozilla.org/kb/content-blocking'),

    # issue #7424
    redirect(r'^firefox(?:\/\d+\.\d+(?:\.\d+)?(?:a\d+)?)?/tracking-protection/start/?$', 'https://support.mozilla.org/kb/tracking-protection'),

    # issue 8596
    redirect(r'firefox/xr/?$', 'https://support.mozilla.org/kb/webxr-permission-info-page'),

    # issue 8419
    redirect(r'firefox/this-browser-comes-highly-recommended/?$', 'firefox.developer.index'),

    # issue 8420
    redirect(r'firefox/dedicated-profiles/?$', 'https://support.mozilla.org/kb/dedicated-profiles-firefox-installation'),

    # issue 8641
    redirect(r'^/firefox/windows-64-bit/?$', 'firefox.browsers.windows-64-bit'),
    redirect(r'^/firefox/best-browser/?$', 'firefox.browsers.best-browser'),

    # Unfck campaign
    redirect(r'^firefox/unfuck/?$', 'firefox.campaign.unfck.index'),
    redirect(r'^firefox/love/?$', 'firefox.campaign.unfck.index'),
    redirect(r'^firefox/liebe/?$', 'firefox.campaign.unfck.index'),
    redirect(r'^firefox/rendonslenetplusnet/?$', 'firefox.campaign.unfck.index'),
    redirect(r'^(unfu?ck|love|liebe|rendonslenetplusnet)/?$', 'firefox.campaign.unfck.index'),

    # issue 9148
    redirect(r'^/firefox/campaign/?$', 'firefox.new'),

    # issue 9788
    redirect(r'^/firefox/enterprise/signup(/.*)?$', 'firefox.enterprise.index'),

    # issue 9953
    redirect(r'^/firefox/features/pip/?$', 'firefox.features.picture-in-picture'),
)
