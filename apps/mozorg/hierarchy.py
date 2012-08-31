from django.conf.urls.defaults import patterns
from funfactory.urlresolvers import reverse

from mozorg.util import page
# TODO : Write tests
# TODO : Where should breadcrumbs with no view link to?
# TODO : Should prev and next link outside of their hierarchy?


def node(display_name, *args):
    """A simple node in the hierarchy"""
    _node = Node(display_name)
    for child in args:
        _node.append(child)
    return _node


def nodeview(display_name, name, template, *args):
    """A node that also has a view associated"""
    _node = Node(display_name, name, template)
    for child in args:
        _node.append(child)
    return _node


class Node:
    def __init__(self, display_name, name=None, template=None):
        self.display_name = display_name
        # TODO : Check that name and template are both None or both not None
        self.name = name
        self.template = template
        self.children = []
        self.parent = None
        self.page = None
        self._breadcrumbs = None
        self._url = None

    def append(self, child):
        self.children.append(child)
        child.parent = self

    def previous_sibling(self):
        if not self.parent:
            return None
        children = self.parent.children
        index = children.index(self)
        if index == 0:
            return None
        return children[index - 1]

    def next_sibling(self):
        if not self.parent:
            return None
        children = self.parent.children
        index = children.index(self)
        if index + 1 == len(children):
            return None
        return children[index + 1]

    @property
    def breadcrumbs(self):
        if self._breadcrumbs:
            return self._breadcrumbs

        self._breadcrumbs = []
        _node = self
        while _node:
            self._breadcrumbs.append(_node)
            _node = _node.parent
        self._breadcrumbs.reverse()
        return self._breadcrumbs

    def nodes_with_view(self, foo):
        """Recursively appends all nodes with a view to foo"""
        if self.template:
            foo.append(self)
        for node in self.children:
            node.nodes_with_view(foo)

    @property
    def url(self):
        if not self.page:
            return None
        if not self._url:
            self._url = reverse(self.page.name)
        return self._url

    def as_urlpattern(self):
        """Creates a flat list of patterns for the Django URLs"""
        nodes_with_view = []
        urlpatterns = []
        self.nodes_with_view(nodes_with_view)
        for node_with_view in nodes_with_view:
            node_with_view.page = page(node_with_view.name,
                                       node_with_view.template,
                                       hierarchy=self, node=node_with_view)
            urlpatterns.append(node_with_view.page)
        return patterns('', *urlpatterns)
