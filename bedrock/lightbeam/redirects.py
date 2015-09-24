from bedrock.redirects.util import redirect


redirectpatterns = (
    # bug 931042
    redirect(r'^collusion', 'lightbeam.lightbeam'),
)
