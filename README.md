bedrock
=======

*bedrock* is the code name of the new mozilla.org. It is bound to be as shiny,
awesome, and open sourcy as always. Perhaps even a little more.

Stay tuned.

Install
-------

To install bedrock, fire a commandline and type the following:

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements/dev.txt

Once you've done that, you'll need to configure the application to run
locally. Create a `settings/local.py` file, containing the following:

        # This is an example settings_local.py file.
    # Copy it and add your local settings here.

    from settings import *


    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sql',
        },
    }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'translations'
        }
    }

    DEBUG = TEMPLATE_DEBUG = True
    LESS_PREPROCESS = True

You will need to have a less compiler. You can get one on debian/ubuntu by
installing the "libjs-less" package.

Make it run
-----------

To make the server run, make sure you are inside a virtualenv, and then
run the server with your local settings:

    python manage.py runserver --settings settings.local

If you are not inside a virtualenv, you can activate it by doing

    source venv/bin/activate

Docs
----

bedrock is a [playdoh project][playdoh]. Check out the [playdoh docs][pd-docs]
for general technical documentation. In addition, there are project-specific
[bedrock docs][br-docs].

[playdoh]: https://github.com/mozilla/playdoh
[pd-docs]: http://playdoh.readthedocs.org/
[br-docs]: http://bedrock.readthedocs.org/

Contributing
------------

Patches are welcome! Feel free to fork and contribute to this project on
[github][gh-bedrock].

[gh-bedrock]: https://github.com/mozilla/bedrock


License
-------
This software is licensed under the [MPL/GPL/LGPL tri-license][MPL]. For more
information, read the file ``LICENSE``.

[MPL]: http://www.mozilla.org/MPL/


