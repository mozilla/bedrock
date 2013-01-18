import l10n_utils

from mozorg.decorators import cache_control_expires


@cache_control_expires(12)
def tabzilla_js(request):
    return l10n_utils.render(request, 'tabzilla/tabzilla.js',
                             content_type='text/javascript')
