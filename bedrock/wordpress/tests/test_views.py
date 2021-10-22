# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test import RequestFactory, override_settings

import pytest
import responses

from bedrock.wordpress.models import BlogPost
from bedrock.wordpress.tests.test_models import TEST_WP_BLOGS, setup_responses
from bedrock.wordpress.views import BlogPostsView


@responses.activate
@override_settings(WP_BLOGS=TEST_WP_BLOGS)
@pytest.mark.django_db
def test_blog_posts_view():
    setup_responses("firefox")
    BlogPost.objects.refresh("firefox")
    setup_responses("hacks")
    BlogPost.objects.refresh("hacks")

    req = RequestFactory().get("/")
    view = BlogPostsView(blog_slugs="firefox", blog_tags=["browser", "jank"], template_name="mozorg/book.html")
    view.request = req
    blog_posts = view.get_context_data()["blog_posts"]
    assert len(blog_posts) == 2
    assert blog_posts[0].wp_id == 10
    assert blog_posts[1].wp_id == 69

    # no tags defined
    view = BlogPostsView(blog_slugs="firefox", template_name="mozorg/book.html")
    view.request = req
    blog_posts = view.get_context_data()["blog_posts"]
    assert len(blog_posts) == 3

    # multiple blogs
    view = BlogPostsView(blog_slugs=["firefox", "hacks"], blog_posts_limit=8, template_name="mozorg/book.html")
    view.request = req
    blog_posts = view.get_context_data()["blog_posts"]
    assert len(blog_posts) == 6

    # multiple blogs with tags
    view = BlogPostsView(blog_slugs=["firefox", "hacks"], blog_tags=["browser", "jank"], blog_posts_limit=8, template_name="mozorg/book.html")
    view.request = req
    blog_posts = view.get_context_data()["blog_posts"]
    assert len(blog_posts) == 4

    # incorrect blog slug
    view = BlogPostsView(blog_slugs="not-a-blog", template_name="mozorg/book.html")
    view.request = req
    blog_posts = view.get_context_data()["blog_posts"]
    assert len(blog_posts) == 0

    # no blog defined, but limited
    view = BlogPostsView(blog_posts_limit=2, blog_posts_template_variable="articles", template_name="mozorg/book.html")
    view.request = req
    blog_posts = view.get_context_data()["articles"]
    assert len(blog_posts) == 2
