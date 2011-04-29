import l10n_utils


def example(request):
    return l10n_utils.render(request, 'l10n_example/example.html')
