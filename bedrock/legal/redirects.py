from bedrock.redirects.util import redirect


redirectpatterns = (
    # bug 1243240
    redirect(r'^about/legal/report-abuse/?$', 'legal.report-infringement'),
)
