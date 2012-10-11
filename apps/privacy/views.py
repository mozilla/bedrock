import l10n_utils
from commonware.response.decorators import xframe_allow


@xframe_allow
def facebook(request):
    return l10n_utils.render(request, 'privacy/facebook.html')
