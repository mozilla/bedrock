from bedrock.redirects.util import redirect


redirectpatterns = (
    # bug 818323
    redirect(r'^projects/security/known-vulnerabilities\.html$', 'security.known-vulnerabilities'),
    redirect(r'^projects/security/older-vulnerabilities\.html$', 'security.older-vulnerabilities'),

    # bug 1090468
    redirect(r'^security/(?P<page>older-alerts|security-announcement|phishing-test(-results)?)\.html$',
             'http://website-archive.mozilla.org/www.mozilla.org/security/security/{page}.html'),
    redirect(r'^security/iSECPartners_Phishing\.pdf$',
             'http://website-archive.mozilla.org/www.mozilla.org/security/security/iSECPartners_Phishing.pdf'),
)
