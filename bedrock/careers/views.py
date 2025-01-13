# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.cache import cache
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


class DiversityView(L10nTemplateView):
    template_name = "careers/diversity.html"

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


class TeamsView(L10nTemplateView):
    template_name = "careers/teams.html"


class LocationsView(L10nTemplateView):
    template_name = "careers/locations.html"


class BenefitsView(L10nTemplateView):
    template_name = "careers/benefits.html"


class PositionListView(LangFilesMixin, RequireSafeMixin, ListView):
    template_name = "careers/listings.html"
    context_object_name = "positions"

    def get_queryset(self):
        _key = "careers_position_listing_qs"
        qs = cache.get(_key)
        if qs is None:
            qs = Position.objects.exclude(job_locations="Remote")
            cache.set(_key, qs, settings.CACHE_TIME_SHORT)
        return qs

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

        post = get_object_or_404(queryset, **self.kwargs)
        return post.cover

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        position = context["position"]

        context["meta_description"] = generate_position_meta_description(position)
        context["postings"] = list(Position.objects.filter(internal_job_id=position.internal_job_id).exclude(job_locations="Remote"))

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
