from datetime import datetime


def current_year(request):
    return {"current_year": datetime.today().year}
