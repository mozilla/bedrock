from bedrock.redirects.util import redirect


redirectpatterns = (
    # bug 1255785
    redirect(r'^styleguide/identity/mozilla/logo-prototype/?$', 'styleguide.home'),
)
