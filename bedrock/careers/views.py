# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from bedrock.careers.forms import PositionFilterForm
from bedrock.careers.models import Position
from bedrock.careers.utils import generate_position_meta_description
from bedrock.wordpress.models import BlogPost
from lib.l10n_utils import L10nTemplateView, LangFilesMixin, RequireSafeMixin, render


class HomeView(L10nTemplateView):
    template_name = "careers/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = BlogPost.objects.filter_by_blogs("careers")
        featured = posts.filter_by_tags("story").first()
        if featured:
            context["featured_post"] = featured
            context["recent_posts"] = posts.exclude(id=featured.id)[:2]
        else:
            context["featured_post"] = None
            context["recent_posts"] = posts[:3]

        return context


class InternshipsView(L10nTemplateView):
    template_name = "careers/internships.html"


class BenefitsView(L10nTemplateView):
    template_name = "careers/benefits.html"


class PositionListView(LangFilesMixin, RequireSafeMixin, ListView):
    model = Position
    template_name = "careers/listings.html"
    context_object_name = "positions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PositionFilterForm()
        return context


class PositionDetailView(LangFilesMixin, RequireSafeMixin, DetailView):
    model = Position
    context_object_name = "position"
    template_name = "careers/position.html"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        position = context["position"]

        context["meta_description"] = generate_position_meta_description(position)
        context["postings"] = list(Position.objects.filter(internal_job_id=position.internal_job_id))

        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return render(
                self.request,
                "careers/404.html",
                status=404,
            )
