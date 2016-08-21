from django.http import HttpResponse

from lib import l10n_utils


def health_check(request):
    return HttpResponse('OK')


def server_error_view(request, template_name='500.html'):
    """500 error handler that runs context processors."""
    return l10n_utils.render(request, template_name, status=500)
