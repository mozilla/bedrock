import l10n_utils

def channel(request):
    return l10n_utils.render(request, "mozorg/channel.html")

def button(request):
    return l10n_utils.render(request, "mozorg/button.html")
