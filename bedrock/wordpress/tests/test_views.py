from django.test import override_settings, RequestFactory

import pytest
import responses

from bedrock.wordpress.models import BlogPost
from bedrock.wordpress.tests.test_models import setup_responses, TEST_WP_BLOGS
from bedrock.wordpress.views import BlogPostsView


@responses.activate
@override_settings(WP_BLOGS=TEST_WP_BLOGS)
@pytest.mark.django_db
def test_blog_posts_view():
    setup_responses()
    BlogPost.objects.refresh('firefox')

    req = RequestFactory().get('/')
    view = BlogPostsView(blog_slug='firefox', blog_tags=['browser', 'jank'],
                         template_name='mozorg/book.html')
    view.request = req
    blog_posts = view.get_context_data()['blog_posts']
    assert len(blog_posts) == 2
    assert blog_posts[0].wp_id == 10
    assert blog_posts[1].wp_id == 69

    # no tags defined
    view = BlogPostsView(blog_slug='firefox', template_name='mozorg/book.html')
    view.request = req
    blog_posts = view.get_context_data()['blog_posts']
    assert len(blog_posts) == 3

    # incorrect blog slug
    view = BlogPostsView(blog_slug='not-a-blog', template_name='mozorg/book.html')
    view.request = req
    blog_posts = view.get_context_data()['blog_posts']
    assert len(blog_posts) == 0

    # no blog defined
    view = BlogPostsView(template_name='mozorg/book.html')
    view.request = req
    blog_posts = view.get_context_data()['blog_posts']
    assert len(blog_posts) == 0
