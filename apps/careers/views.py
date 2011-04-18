import jingo


def careers(request):
    return jingo.render(request, 'careers/home.html')
