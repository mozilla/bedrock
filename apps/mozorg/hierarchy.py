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
    def __init__(self, display_name, path=None, template=None, children=None):
        self.display_name = display_name

        self.path = path
        self.template = template
        self.parent = None

        self.children = children or ()
        for child in self.children:
            child.parent = self

    @property
    def full_path(self):
        return '/'.join([node.path for node in self.breadcrumbs
                         if node.path is not None])

    @property
    def page(self):
        if self.template:
            return page(self.full_path, self.template, node_root=self.root,
                        node=self)
        else:
            return None

    @property
    def path_to_root(self):
        node = self
        while node:
            yield node
            node = node.parent

    @property
    def breadcrumbs(self):
        path = list(self.path_to_root)
        path.reverse()
        return path

    @property
    def root(self):
        return list(self.path_to_root)[-1]

    @property
    @requires_parent
    def previous(self):
        children = self.parent.children
        index = children.index(self)
        if index == 0:
            return self.parent.previous
        return children[index - 1]

    @property
    @requires_parent
    def next(self):
        children = self.parent.children
        index = children.index(self)
        if index + 1 == len(children):
            return self.parent.next
        return children[index + 1]

    @property
    def url(self):
        if self.page:
            return reverse(self.page.name)
        elif self.children:
            return self.children[0].url
        else:
            return None

    def as_urlpattern(self):
        """Return a urlconf for this PageTree and its children."""
        pages = []
        nodes = [self]
        while nodes:
            node = nodes.pop()
            if node.template:
                pages.append(node.page)
            nodes += node.children
        return patterns('', *pages)
