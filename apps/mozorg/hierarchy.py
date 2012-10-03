from functools import wraps

from django.conf.urls.defaults import patterns

from funfactory.urlresolvers import reverse

from mozorg.util import page


def requires_parent(f):
    @wraps(f)
    def wrapped(self, *args, **kwargs):
        if self.parent is None:
            return None
        else:
            return f(self, *args, **kwargs)
    return wrapped


class PageNode(object):
    """
    A utility for representing a hierarchical page structure.

    A PageNode is associated with a static page and can have several child nodes
    that themselves have pages and children, forming a tree structure. The root
    of the tree can then be used to create a urlconf representing every page
    within it.

    Example:

        hierarchy = PageNode('Root', path='root', children=[
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
        return list(self.path_to_root)[-1]

    @property
    @requires_parent
    def previous(self):
        """
        The previous sibling node of the current node.

        If this node has no previous siblings, return the last child of our
        parent's previous sibling. If that fails, return None.
        """
        children = self.parent.children
        index = children.index(self)
        if index == 0:
            parent_previous = self.parent.previous
            if parent_previous is None or not parent_previous.children:
                return None
            else:
                return parent_previous.children[-1]
        else:
            return children[index - 1]

    @property
    @requires_parent
    def next(self):
        """
        The next sibling node of the current node.

        If this node has no following siblings, return the first child of our
        parent's next sibling. If that fails, return None.
        """
        children = self.parent.children
        index = children.index(self)
        if index + 1 == len(children):
            parent_next = self.parent.next
            if parent_next is None or not parent_next.children:
                return None
            else:
                return parent_next.children[0]
        else:
            return children[index + 1]

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

    def as_urlpatterns(self):
        """Return a urlconf for this PageTree and its children."""
        pages = []
        nodes = [self]
        while nodes:
            node = nodes.pop()
            if node.template:
                pages.append(node.page)
            nodes += node.children
        return patterns('', *pages)
