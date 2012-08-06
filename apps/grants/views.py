from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
import l10n_utils
from models import Grant
from forms import GrantForm


@csrf_exempt
def index (request):
    template = 'grants/index.html'

    context = {
        'grants': Grant.grants.all()[:10],
        'fields': GrantForm().visible_fields(),
    }

    return l10n_utils.render(request, template, context)


@csrf_exempt
def list (request):
    template = 'grants/list.html'

    context = {
        'grants': Grant.grants.all(),
        'fields': GrantForm().visible_fields(),
    }

    return l10n_utils.render(request, template, context)


@csrf_exempt
def single (request, slug):
    try:
        template = 'grants/single.html'

        context = {
            'grant': Grant.grants.get(slug=slug),
            'fields': GrantForm().visible_fields(),
        }

        return l10n_utils.render(request, template, context)
    except Grant.DoesNotExist:
        raise Http404
