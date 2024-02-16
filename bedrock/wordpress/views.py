# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from sentry_sdk import capture_exception

from bedrock.wordpress.models import BlogPost
from lib.l10n_utils import L10nTemplateView


class BlogPostsMixin:
    blog_tags = None
    blog_slugs = None
    blog_posts_limit = 4
    blog_posts_template_variable = "blog_posts"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        blog = BlogPost.objects.all()
        if self.blog_slugs:
            if isinstance(self.blog_slugs, str):
                blog_slugs = [self.blog_slugs]
            else:
                blog_slugs = self.blog_slugs

            blog = blog.filter_by_blogs(*blog_slugs)
            ctx["blog_slugs"] = blog_slugs

        if self.blog_tags:
            blog = blog.filter_by_tags(*self.blog_tags)
            ctx["blog_tags"] = self.blog_tags

        if self.blog_posts_limit:
            blog = blog[: self.blog_posts_limit]

        try:
            # run the query here so that we can catch exceptions
            # and render the page without blog posts
            ctx[self.blog_posts_template_variable] = list(blog)
        except Exception:
            capture_exception()
            ctx[self.blog_posts_template_variable] = []

        return ctx


class BlogPostsView(BlogPostsMixin, L10nTemplateView):
    pass
