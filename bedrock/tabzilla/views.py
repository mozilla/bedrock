import l10n_utils


def tabzilla_js(request):
    return l10n_utils.render(request, 'tabzilla/tabzilla.js',
                             content_type='text/javascript')
