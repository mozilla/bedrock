from bedrock.redirects.util import no_redirect, redirect

redirectpatterns = (
    # bug 1319207
    # 'Firefox Focus' cannot be used in de locale due to legal constraints
    redirect(r'^de/privacy/firefox-focus/?', '/de/privacy/firefox-klar/', locale_prefix=False),
    # special de URL should not be accessible from other locales
    no_redirect(r'^de/privacy/firefox-klar/?', locale_prefix=False),
    redirect(r'^privacy/firefox-klar/?', 'privacy.notices.firefox-focus'),
)
