import l10n_utils


def index(request):
    return l10n_utils.render(request, "mozorg/index.html")

def channel(request):
    return l10n_utils.render(request, "mozorg/channel.html")

def button(request):
    return l10n_utils.render(request, "mozorg/button.html")

def new(request):
    return l10n_utils.render(request, "mozorg/new.html")
