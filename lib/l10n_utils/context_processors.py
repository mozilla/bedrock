from dotlang import Translations


def trans(request):
    # Make a box for our translations so that they can be updated by
    # helpers
    return {'__trans': Translations()}
