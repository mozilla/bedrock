# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mock import patch

from bedrock.mozorg.hierarchy import PageNode, PageRoot
from bedrock.mozorg.tests import TestCase


class TestPageNode(TestCase):
    def test_children_parents(self):
        """
        If a node is given children in the constructor, the children must mark
        the node as their parent.
        """
        children = [PageNode('test'), PageNode('test2')]
        parent = PageRoot('parent', children=children)
        for child in children:
            assert child.parent == parent

    def test_full_path(self):
        """
        full_path should return the path of this node and all of its parents
        joined by slashes.
        """
        child = PageNode('test', path='asdf')
        PageRoot('test', path='blah', children=[
            PageNode('test', path='whoo', children=[child])
        ])
        assert child.full_path == 'blah/whoo/asdf'

    def test_full_path_empty(self):
        """
        If one of a node's parents have an empty path, they should not be
        included in the full path.
        """
        child = PageNode('test', path='asdf')
        PageRoot('', path='blah', children=[PageNode('', children=[child])])
        assert child.full_path == 'blah/asdf'

    @patch('bedrock.mozorg.hierarchy.page')
    def test_page(self, page):
        """
        If a pagenode is given a template, it should provide a page for
        inclusion in a urlconf.
        """
        page.return_value = 'testreturn'
        assert PageNode('test').page is None

        node = PageNode('test', path='blah', template='test.html')
        parent = PageRoot('testparent', path='yo', children=[node])
        assert node.page == 'testreturn'
        page.assert_called_with('yo/blah', 'test.html', node_root=parent,
                                node=node)

    def test_path_to_root(self):
        """
        path_to_root should return an iterable of nodes following the route from
        the child node to the root of the tree.
        """
        child1 = PageNode('test')
        child2 = PageNode('test', children=[child1])
        root = PageRoot('test', children=[child2, PageNode('test')])
        assert list(child1.path_to_root) == [child1, child2, root]

    def test_breadcrumbs(self):
        """
        breadcrumbs should return a list of nodes following the path from the
        root to the child node.
        """
        child1 = PageNode('test')
        child2 = PageNode('test', children=[child1])
        root = PageRoot('test', children=[child2, PageNode('test')])
        assert list(child1.breadcrumbs) == [root, child2, child1]

    def test_root(self):
        """root should return the root of the page tree."""
        child1 = PageNode('test')
        child2 = PageNode('test', children=[child1])
        root = PageRoot('test', children=[child2, PageNode('test')])
        assert child1.root == root

    def test_no_root(self):
        """If the root of a tree is not a PageRoot, raise a ValueError."""
        child1 = PageNode('test')
        child2 = PageNode('test', children=[child1])
        PageNode('test', children=[child2, PageNode('test')])
        self.assertRaises(ValueError, lambda: child1.root)

    def test_previous(self):
        """
        Previous should return the previous sibling node, or None if one doesn't
        exist.
        """
        child1 = PageNode('', template='test1.html')
        child2 = PageNode('', template='test2.html')
        PageRoot('', children=[child1, child2])
        assert child2.previous == child1
        assert child1.previous is None

    def test_previous_cross(self):
        """
        If a node has no siblings, attempt to cross over to the children of the
        parent's sibling.
        """
        # Diagram of the final tree:
        #      root
        #      /  \
        #     O    O--
        #    /    /   \
        #   O    O     O
        #  /    / \   / \
        # c1   c2 c3 c4  O
        child1 = PageNode('', template='test1.html')
        child2 = PageNode('', template='test2.html')
        child3 = PageNode('', template='test3.html')
        child4 = PageNode('', template='test4.html')
        root = PageRoot('', template='root.html', children=[
            PageNode('', children=[
                PageNode('', children=[child1])
            ]),
            PageNode('', children=[
                PageNode('', children=[child2, child3]),
                PageNode('', children=[child4, PageNode('')])
            ])
        ])
        assert root.previous is None
        assert child1.previous == root
        assert child2.previous == child1
        assert child3.previous == child2
        assert child4.previous == child3

    def test_next(self):
        """
        Next should return the next sibling node, or None if one doesn't exist.
        """
        child1 = PageNode('', template='test1.html')
        child2 = PageNode('', template='test1.html')
        PageRoot('', children=[child1, child2])
        assert child1.next == child2
        assert child2.next is None

    def test_next_cross(self):
        """
        If a node has no siblings, attempt to cross over to the children of the
        parent's sibling.
        """
        # Diagram of the final tree:
        #      root
        #      /  \
        #     O    O--
        #    /    /   \
        #   O    O     O
        #  /    / \   / \
        # c1   c2 c3 c4  O
        child1 = PageNode('', template='test1.html')
        child2 = PageNode('', template='test2.html')
        child3 = PageNode('', template='test3.html')
        child4 = PageNode('', template='test4.html')
        root = PageRoot('', template='root.html', children=[
            PageNode('', children=[
                PageNode('', children=[child1])
            ]),
            PageNode('', children=[
                PageNode('', children=[child2, child3]),
                PageNode('', children=[child4, PageNode('')])
            ])
        ])
        assert root.next == child1
        assert child1.next == child2
        assert child2.next == child3
        assert child3.next == child4
        assert child4.next is None

    @patch('bedrock.mozorg.hierarchy.reverse')
    def test_url(self, reverse):
        """If a node has a page, url should return the url for that page."""
        node = PageRoot('test', path='asdf/qwer', template='fake.html')
        reverse.return_value = 'asdf'
        assert node.url == 'asdf'
        reverse.assert_called_with('fake')

    @patch('bedrock.mozorg.hierarchy.reverse')
    def test_url_child(self, reverse):
        """
        If a node doesn't have a page, but has children, it should return the
        url of its first child.
        """
        child1 = PageNode('test', path='asdf/qwer', template='fake.html')
        child2 = PageNode('test', path='bb/qr', template='fake2.html')
        parent = PageRoot('', children=[child1, child2])

        reverse.return_value = 'asdf'
        assert parent.url == 'asdf'
        reverse.assert_called_with('fake')

    def test_url_none(self):
        """If a node doesn't have a page or children, url should return None."""
        node = PageNode('')
        assert node.url is None


class TestPageRoot(TestCase):
    @patch.object(PageNode, 'page')
    def test_as_urlpatterns(self, page):
        """
        as_urlpatterns should return a urlconf with the pages for all the nodes
        included in the tree.
        """
        child1 = PageNode('child1', path='asdf/qwer', template='fake.html')
        child2 = PageNode('child2', path='bb/qr', template='fake2.html')
        parent = PageNode('parent', children=[child1, child2])
        root = PageRoot('root', path='badsbi', template='fake3.html',
                        children=[parent])

        # Mocking properties
        page.__get__ = lambda mock, self, cls: self.display_name

        assert root.as_urlpatterns() == ['root', 'child1', 'child2']
