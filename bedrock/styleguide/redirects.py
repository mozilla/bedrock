from bedrock.redirects.util import redirect


redirectpatterns = (
    # bug 1433749
    redirect(r'^styleguide/(.+)', 'styleguide.index'),
)
