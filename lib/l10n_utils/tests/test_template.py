import os

from jingo import env
from jinja2 import FileSystemLoader
from mock import patch
from nose.plugins.skip import SkipTest
from nose.tools import eq_

from mozorg.tests import TestCase


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')
TEMPLATE_DIRS = (os.path.join(ROOT, 'templates'),)


class TestTemplateLangFiles(TestCase):
    @patch.object(env, 'loader', FileSystemLoader(TEMPLATE_DIRS))
    def test_added_lang_files(self):
        """
        Lang files specified in the template should be added to the defaults.
        """
        template = env.get_template('some_lang_files.html')
        # make a dummy object capable of having arbitrary attrs assigned
        request = type('request', (), {})()
        template.render(request=request)
        eq_(request.langfiles, ['dude', 'walter',
                                'main', 'base', 'newsletter'])

    @patch.object(env, 'loader', FileSystemLoader(TEMPLATE_DIRS))
    def test_added_lang_files_inheritance(self):
        """
        Lang files specified in the template should be added to the defaults
        and any specified in parent templates.
        """
        raise SkipTest
        # TODO fix this. it is broken. hence the skip.
        #      does not pick up the files from the parent.
        #      captured in bug 797984.
        template = env.get_template('even_more_lang_files.html')
        # make a dummy object capable of having arbitrary attrs assigned
        request = type('request', (), {})()
        template.render(request=request)
        eq_(request.langfiles, ['donnie', 'smokey', 'jesus', 'dude', 'walter',
                                'main', 'base', 'newsletter'])
