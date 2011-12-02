# Django settings file for bedrock.

import os

from django.utils.functional import lazy

from funfactory.settings_base import *

# Make file paths relative to settings.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = lambda *a: os.path.join(ROOT, *a)

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

SESSION_COOKIE_SECURE = True

# Accepted locales
PROD_LANGUAGES = ('de', 'en-US', 'es', 'fr',)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1iz#v0m55@h26^m6hxk3a7at*h$qj_2a$juu1#nv50548j(x1v'

TEMPLATE_DIRS = (
    path('templates'),
    path('locale')
)

def JINJA_CONFIG():
    import jinja2
    from django.conf import settings
    config = {'extensions': ['tower.template.i18n', 'jinja2.ext.do',
                             'jinja2.ext.with_', 'jinja2.ext.loopcontrols',
                             'l10n_utils.template.l10n_blocks'],
              'finalize': lambda x: x if x is not None else ''}
    return config

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'common': (
            'css/covehead/template.css',
            'css/covehead/content.css',
            'css/careers.css',
        ),
        'benefits': (
            'css/benefits.css',
        ),
    },
    'js': {
        'common': (
            'js/libs/jquery-1.4.4.min.js',
            'js/util.js',
            'js/nav-main.js',
        ),
        'benefits': (
            'js/benefits.js',
        ),
    }
}

INSTALLED_APPS = list(INSTALLED_APPS) + [
    # Local apps
    'careers',
    'l10n_example',  # DELETEME
    'mozorg',

    # libs
    'l10n_utils',

    # Jobvite
    'django_jobvite',
]

## Auth
PWD_ALGORITHM = 'bcrypt'
HMAC_KEYS = {
    #'2011-01-01': 'cheesecake',
}

# Jobvite XML URI
JOBVITE_URI = '' # http://www.jobvite.com/CompanyJobs/Xml.aspx?c=...
