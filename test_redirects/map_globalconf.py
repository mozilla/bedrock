from __future__ import absolute_import

from .base import flatten, url_test


URLS = flatten((
    # bug 832348 **/index.html -> **/
    url_test('/any/random/url/with/index.html', '/any/random/url/with/'),

    # bug 774675
    url_test('/en/', '/en-US/'),
    url_test('/es/', '/es-ES/'),
    url_test('/pt/', '/pt-BR/'),

    # bug 880182
    url_test('/ja-JP-mac/', '/ja/'),

    # bug 795970 - lowercase to uppercase, e.g. en-us to en-US
    url_test('/en-us/', '/en-US/'),
    url_test('/pt-br/', '/pt-BR/'),

    # bug 845988 - remove double slashes in URLs
    url_test('/en-US/firefox//all/', '/en-US/firefox/all/'),

    # bug 755826
    url_test('/zh-CN/', 'http://firefox.com.cn/'),

    # bug 764261, 841393, 996608, 1008162, 1067691, 1113136, 1119022, 1131680, 1115626
    url_test('/zh-TW/', 'http://mozilla.com.tw/'),
    url_test('/zh-TW/mobile/', 'http://mozilla.com.tw/firefox/mobile/'),
    url_test('/zh-TW/download/', 'http://mozilla.com.tw/firefox/download/'),

    # bug 874913
    url_test('/en-US/products/download.html', '/en-US/firefox/new/?#download-fx'),

    # bug 845580
    url_test('/en-US/home/', '/en-US/firefox/'),

    # bug 948605
    url_test('/en-US/firefox/xp-any-random-thing', '/firefox/'),
    url_test('/en-US/products/firefox/start/', 'http://start.mozilla.org'),
    url_test('/start/the-sm-one', 'http://www.seamonkey-project.org/start/',
             req_headers={'User-Agent': 'mozilla seamonkey'}),
    url_test('/start/any-random-thing', '/firefox/'),

    # bug 856081 redirect /about/drivers https://wiki.mozilla.org/Firefox/Drivers
    url_test('/about/drivers{/,.html}', 'https://wiki.mozilla.org/Firefox/Drivers'),

    # community
    # bug 885797
    url_test('/community/{directory,wikis,blogs,websites}.html',
             'https://wiki.mozilla.org/Websites/Directory'),

    # bug 885856
    url_test('/projects/index.{de,fr,hr,sq}.html', '/{de,fr,hr,sq}/firefox/products/',
             status_code=302),

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
    url_test('/firefox/webhero/random/stuff/', '/firefox/'),

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
    url_test('/ja/', 'http://www.mozilla.jp/', status_code=302),

    # bug 1051686
    url_test('/ja/firefox/organizations/', 'http://www.mozilla.jp/business/downloads/'),


    # TODO: Fix these. They're too broken to use at present.
    # bug 1138280
    # RewriteRule ^/ja/(firefox|thunderbird)/(beta/)?notes/ http://mozilla.jp/$1$2/notes/ [L,R=301]
    # RewriteRule ^/ja/mobile/(beta/?)notes/ http://mozilla.jp/android/$1$2/notes/ [L,R=301]
    # RewriteRule ^/ja/(firefox|thunderbird)/(\d+\.\d+(\.\d+)*)(beta)?/releasenotes(/?|/.+)$ http://mozilla.jp/firefox/$1/$2$3/releasenotes/ [L,R=301]
    # RewriteRule ^/ja/mobile/(\d+\.\d+(\.\d+)*)(beta)?/releasenotes(/?|/.+)$ http://mozillla.jp/firefox/android/$1$2/releasenotes/ [L,R=301]
))
