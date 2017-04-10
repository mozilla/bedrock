from django.views.generic import TemplateView

from bedrock.wordpress.models import BlogPost
from lib.l10n_utils import LangFilesMixin


class BlogPostsMixin(object):
    blog_tags = None
    blog_slug = None

    def get_context_data(self, **kwargs):
        ctx = super(BlogPostsMixin, self).get_context_data(**kwargs)
        if self.blog_slug:
            blog = BlogPost.objects.filter_by_blog(self.blog_slug)
            if self.blog_tags:
                blog = blog.filter_by_tags(*self.blog_tags)

            ctx['blog_posts'] = blog
        else:
            ctx['blog_posts'] = []

        return ctx


class BlogPostsView(BlogPostsMixin, LangFilesMixin, TemplateView):
    pass
