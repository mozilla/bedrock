from bedrock.redirects.util import redirect


redirectpatterns = (
    # bug 1243240
    redirect(r'^about/legal/report-abuse/?$', 'legal.report-infringement'),

    # bug 1321033
    redirect(r'^about/legal/terms/firefox-hello', 'privacy.archive.hello-2014-11'),

    # issue 5816
    redirect(r'^about/logo', 'styleguide.index')
)
