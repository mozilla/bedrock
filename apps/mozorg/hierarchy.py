# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import patterns

from funfactory.urlresolvers import reverse

from mozorg.util import page


class PageNode(object):
    """
    A utility for representing a hierarchical page structure.

    A PageNode is associated with a static page and can have several child nodes
    that themselves have pages and children, forming a tree structure. The root
    of the tree can then be used to create a urlconf representing every page
    within it.

    Example:

        hierarchy = PageRoot('Root', path='root', children=[
            PageNode('Child1', path='child1', template='child1.html'),
            PageNode('Child2', path='child2', template='child2.html')
        ])
        urlpatterns = hierarchy.as_urlpatterns()

    In the example above, the template `child1.html` will be available at the
    url `/root/child1/`.
    """
    def __init__(self, display_name, path=None, template=None, children=None):
        """
        Create a new PageNode.

        display_name is a user-facing name for this node that may be shown in
        hierarchical navigation or breadcrumb navigation.

        path is a url path component that will be appended to the front of any
        child node paths, as well as the final path component for this node's
        page.

        template is the path to the template that this node's page will use. If
        it is None, this node won't have a template.

        children is a list of child nodes.
        """
        self.display_name = display_name

        self.path = path
        self.template = template
        self.parent = None

        self.children = children or ()
        for child in self.children:
            child.parent = self

    @property
    def full_path(self):
        """
        The full url path for this node, including the paths of its parent
        nodes.
        """
        return '/'.join([node.path for node in self.breadcrumbs
                         if node.path is not None])

    @property
    def page(self):
        """The page for this node, which is a RegexURLPattern."""
        if self.template:
            return page(self.full_path, self.template, node_root=self.root,
                        node=self)
        else:
            return None

    @property
    def path_to_root(self):
        """
        An iterable that contains the nodes that lead to the tree's root,
        starting with the current node.
        """
        node = self
        while node:
            yield node
            node = node.parent

    @property
    def breadcrumbs(self):
        """
        A list of nodes that form a path from the tree root to the current node.
        """
        path = list(self.path_to_root)
        path.reverse()
        return path

    @property
    def root(self):
        """The root of the tree that this node is in."""
        root = list(self.path_to_root)[-1]
        if not isinstance(root, PageRoot):
            raise ValueError('Root node is not a PageRoot object.')
        return root

    @property
    def previous(self):
        """
        The previous node with a page in a pre-order traversal of the tree.
        """
        return self.root.get_previous_node(self)

    @property
    def next(self):
        """The next node with a page in a pre-order traversal of the tree."""
        return self.root.get_next_node(self)

    @property
    def url(self):
        """
        The url for this node's page.

        If this node doesn't have a page, it will return the url of its first
        child. If it has no children, it will return None.
        """
        if self.page:
            return reverse(self.page.name)
        elif self.children:
            return self.children[0].url
        else:
            return None

    def __repr__(self):
        return u'{0}(display_name="{1}", path="{2}", template="{3})"'.format(
            self.__class__.__name__, self.display_name, self.full_path,
            self.template)


class PageRoot(PageNode):
    """
    Root of a PageNode tree.

    The root node of a PageNode tree MUST be a PageRoot. If it is not, any
    reference to the root of the tree with throw a ValueError.
    """
    def __init__(self, *args, **kwargs):
        super(PageRoot, self).__init__(*args, **kwargs)

        # Buid a pre-order traversal of this tree's nodes.
        self.preordered_nodes = []
        nodes = [self]
        while nodes:
            node = nodes.pop()
            self.preordered_nodes.append(node)
            nodes.extend(reversed(node.children))

    def get_previous_node(self, current_node):
        end = self.preordered_nodes.index(current_node)
        for node in reversed(self.preordered_nodes[0:end]):
            if node.template:
                return node
        return None

    def get_next_node(self, current_node):
        start = self.preordered_nodes.index(current_node) + 1
        for node in self.preordered_nodes[start:]:
            if node.template:
                return node
        return None

    def as_urlpatterns(self):
        """Return a urlconf for this PageRoot and its children."""
        return patterns('', *[node.page for node in self.preordered_nodes if
                              node.template])
