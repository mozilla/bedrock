from django.core.exceptions import (
    BadRequest,
    PermissionDenied,
    SuspiciousOperation,
)
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.http.multipartparser import MultiPartParserError
from django.urls import path


def index(request):
    return HttpResponse("test")


def redirect(request):
    return HttpResponseRedirect("/")


def returns_400(request):
    return HttpResponse("400", status=400)


def raises_400_bad_request(request):
    raise BadRequest


def raises_400_multipart_parser_error(request):
    raise MultiPartParserError


def raises_400_suspicious_operation(request):
    raise SuspiciousOperation


def raises_403_permission_denied(request):
    raise PermissionDenied


def returns_404(request):
    return HttpResponse("404", status=404)


def raises_404(request):
    raise Http404


def returns_500(request):
    return HttpResponse("500", status=500)


def raises_500(request):
    raise Exception("500")


urlpatterns = [
    path("", index, name="index"),
    path("redirect/", redirect, name="redirect"),
    path("raises_400_bad_request/", raises_400_bad_request, name="raises_400_bad_request"),
    path("raises_400_multipart_parser_error/", raises_400_multipart_parser_error, name="raises_400_multipart_parser_error"),
    path("raises_400_suspicious_operation/", raises_400_suspicious_operation, name="raises_400_suspicious_operation"),
    path("raises_403_permission_denied/", raises_403_permission_denied, name="raises_403_permission_denied"),
    path("returns_400/", returns_400, name="returns_400"),
    path("raises_404/", raises_404, name="raises_404"),
    path("returns_404/", returns_404, name="returns_404"),
    path("raises_500/", raises_500, name="raises_500"),
    path("returns_500/", returns_500, name="returns_500"),
]
