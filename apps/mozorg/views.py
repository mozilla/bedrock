import l10n_utils

def channel(request):
    data = {}

    if 'mobile_first' in request.GET:
        data['mobile_first'] = True

    return l10n_utils.render(request, "mozorg/channel.html", data)
