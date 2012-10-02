from mock import Mock, patch
from nose.tools import eq_, ok_

from mozorg.hierarchy import PageNode, requires_parent
from mozorg.tests import TestCase


class MyNode(object):
        def __init__(self, parent=None):
            self.parent = parent

        @requires_parent
        def myfunc(self):
            return True


class TestRequiresParent(TestCase):
    def test_requires_parent(self):
        """
        If a method requires the parent attribute, it should return None when
        the attribute is not set.
        """
        mynode = MyNode()
        eq_(mynode.myfunc(), None)

        mynode = MyNode(True)
        eq_(mynode.myfunc(), True)


class TestPageNode(TestCase):
    def test_children_parents(self):
        """
        If a node is given children in the constructor, the children must mark
        the node as their parent.
        """
        children = [PageNode('test'), PageNode('test2')]
        parent = PageNode('parent', children=children)
        for child in children:
            eq_(child.parent, parent)

    def test_full_path(self):
        """
        full_path should return the path of this node and all of its parents
        joined by slashes.
        """
        child = PageNode('test', path='asdf')
        PageNode('test', path='blah', children=[
                 PageNode('test', path='whoo', children=[child])
        ])
        eq_(child.full_path, 'blah/whoo/asdf')

    def test_full_path_empty(self):
        """
        If one of a node's parents have an empty path, they should not be
        included in the full path.
        """
        child = PageNode('test', path='asdf')
        PageNode('', path='blah', children=[PageNode('', children=[child])])
        eq_(child.full_path, 'blah/asdf')

    @patch('mozorg.hierarchy.page')
    def test_page(self, page):
        """
        If a pagenode is given a template, it should provide a page for
        inclusion in a urlconf.
        """
        page.return_value = 'testreturn'
        eq_(PageNode('test').page, None)

        node = PageNode('test', path='blah', template='test.html')
        parent = PageNode('testparent', path='yo', children=[node])
        eq_(node.page, 'testreturn')
        page.assert_called_with('yo/blah', 'test.html', node_root=parent,
                                node=node)

    def test_path_to_root(self):
        """
        path_to_root should return an iterable of nodes following the route from
        the child node to the root of the tree.
        """
        child1 = PageNode('test')
        child2 = PageNode('test', children=[child1])
        root = PageNode('test', children=[child2, PageNode('test')])
        eq_(list(child1.path_to_root), [child1, child2, root])

    def test_breadcrumbs(self):
        """
        breadcrumbs should return a list of nodes following the path from the
        root to the child node.
        """
        child1 = PageNode('test')
        child2 = PageNode('test', children=[child1])
        root = PageNode('test', children=[child2, PageNode('test')])
        eq_(list(child1.breadcrumbs), [root, child2, child1])

    def test_root(self):
        """root should return the root of the page tree."""
        child1 = PageNode('test')
        child2 = PageNode('test', children=[child1])
        root = PageNode('test', children=[child2, PageNode('test')])
        eq_(child1.root, root)

    def test_previous(self):
        """
        Previous should return the previous sibling node, or None if one doesn't
        exist.
        """
        child1 = PageNode('')
        child2 = PageNode('')
        PageNode('', children=[child1, child2])
        eq_(child2.previous, child1)
        eq_(child1.previous, None)

    def test_next(self):
        """
        Next should return the next sibling node, or None if one doesn't exist.
        """
        child1 = PageNode('')
        child2 = PageNode('')
        PageNode('', children=[child1, child2])
        eq_(child1.next, child2)
        eq_(child2.next, None)

    @patch('mozorg.hierarchy.reverse')
    def test_url(self, reverse):
        """If a node has a page, url should return the url for that page."""
        node = PageNode('test', path='asdf/qwer', template='fake.html')
        reverse.return_value = 'asdf'
        eq_(node.url, 'asdf')
        reverse.assert_called_with('fake')

    @patch('mozorg.hierarchy.reverse')
    def test_url_child(self, reverse):
        """
        If a node doesn't have a page, but has children, it should return the
        url of its first child.
        """
        child1 = PageNode('test', path='asdf/qwer', template='fake.html')
        child2 = PageNode('test', path='bb/qr', template='fake2.html')
        parent = PageNode('', children=[child1, child2])

        reverse.return_value = 'asdf'
        eq_(parent.url, 'asdf')
        reverse.assert_called_with('fake')

    def test_url_none(self):
        """If a node doesn't have a page or children, url should return None."""
        node = PageNode('')
        eq_(node.url, None)

    @patch('mozorg.hierarchy.patterns')
    @patch.object(PageNode, 'page')
    def test_as_urlpatterns(self, page, patterns):
        """
        as_urlpatterns should return a urlconf with the pages for all the nodes
        included in the tree.
        """
        child1 = PageNode('child1', path='asdf/qwer', template='fake.html')
        child2 = PageNode('child2', path='bb/qr', template='fake2.html')
        parent = PageNode('parent', children=[child1, child2])
        root = PageNode('root', path='badsbi', template='fake3.html',
                        children=[parent])

        patterns.return_value = 'asdf'
        # Mocking properties
        page.__get__ = lambda mock, self, cls: self.display_name

        eq_(root.as_urlpatterns(), 'asdf')

        args = patterns.call_args[0]
        eq_(args[0], '')
        print args
        ok_('child1' in args)
        ok_('child2' in args)
        ok_('root' in args)
        ok_('parent' not in args)
