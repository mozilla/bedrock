Django reCAPTCHA
================
**Django reCAPTCHA form field/widget integration app.**

.. contents:: Contents
    :depth: 5

django-recaptcha uses a modified version of the `Python reCAPTCHA client <http://pypi.python.org/pypi/recaptcha-client>`_ which is included in the package as ``client.py``.


Installation
------------

#. Install or add ``django-recaptcha`` to your Python path.

#. Add ``captcha`` to your ``INSTALLED_APPS`` setting.

#. Add a ``RECAPTCHA_PUBLIC_KEY`` setting to the project's ``settings.py`` file. This is your public API key as provided by reCAPTCHA, i.e.::
    
    RECAPTCHA_PUBLIC_KEY = '76wtgdfsjhsydt7r5FFGFhgsdfytd656sad75fgh'
    
   This can be seperately specified at runtime by passing a ``public_key`` parameter when constructing the ``ReCaptchaField``, see field usage below.

#. Add a ``RECAPTCHA_PRIVATE_KEY`` setting to the project's ``settings.py`` file. This is your private API key as provided by reCAPTCHA, i.e.::
    
    RECAPTCHA_PRIVATE_KEY = '98dfg6df7g56df6gdfgdfg65JHJH656565GFGFGs'
   
   This can be seperately specified at runtime by passing a ``private_key`` parameter when constructing the ``ReCaptchaField``, see field usage below.

#. Optionally add a ``RECAPTCHA_USE_SSL`` setting to the project's ``settings.py`` file. This causes reCAPTCHA validation submits to be made over SSL, i.e.::
    
    RECAPTCHA_USE_SSL = True

   If you don't add this setting the default behaviour is to **NOT** use SSL.
   This can be seperately specified at runtime by passing a ``use_ssl`` parameter when constructing the ``ReCaptchaField``, see field usage below.

Usage
-----

Field
~~~~~
The quickest way to add reCAPTHCA to a form is to use the included ``ReCaptchaField`` field type. A ``ReCaptcha`` widget will be rendered with the field validating itself without any further action required from you. For example::

    from django import forms
    from captcha.fields import ReCaptchaField

    class FormWithCaptcha(forms.Form):
        captcha = ReCaptchaField()

To allow for runtime specification of keys and SSL usage you can optionally pass ``private_key``, ``public_key`` or ``use_ssl`` parameters to the constructor, i.e.::
    
    captcha = ReCaptchaField(
        public_key='76wtgdfsjhsydt7r5FFGFhgsdfytd656sad75fgh',
        private_key='98dfg6df7g56df6gdfgdfg65JHJH656565GFGFGs',
        use_ssl=True
    )

If specified these parameters will be used instead of your reCAPCTHA project settings.
        
The reCAPTCHA widget supports several `Javascript options variables <https://code.google.com/apis/recaptcha/docs/customization.html>`_ customizing the behaviour of the widget, such as ``theme`` and ``lang``. You can forward these options to the widget by passing an ``attr`` parameter containing a dictionary of options to ``ReCaptchaField``, i.e.::

    captcha = ReCaptchaField(attrs={'theme' : 'clean'})

The captcha client takes the key/value pairs and writes out the RecaptchaOptions value in JavaScript.


Unit Testing
~~~~~~~~~~~~
django-recaptcha detects for `DEBUG = True` in the settings.py to facilitate unit tests.
When `DEBUG = TRUE`, using `PASSED` as the `recaptcha_response_field` value.

Example:

    form_params = {'recaptcha_response_field': 'PASSED'}
    form = RegistrationForm(form_params) # assuming only one ReCaptchaField
    form.is_valid() # True

Passing any other values will cause django-recaptcha to continue normal processing and return a form error.


django-registration
~~~~~~~~~~~~~~~~~~~
django-recaptcha ships with a `django-registration <https://bitbucket.org/ubernostrum/django-registration>`_ backend extending the default backend to include a reCAPTCHA field. This is included mostly as an example of how you could intergrate a reCAPTCHA field with django-registration. I suggest you familiarize yourself with `the django-registration docs <http://docs.b-list.org/django-registration/0.8/index.html>`_ for more comprehensive documentation. 

.. note::

    This backend will only work with django-registration versions `0.8-alpha-1 <https://bitbucket.org/ubernostrum/django-registration/downloads/django-registration-0.8-alpha-1.tar.gz>`_ and up.

To use the reCAPTHCA backend complete these steps:

#. Add ``registration`` to your ``INSTALLED_APPS`` setting.

#. Add captcha registration backend url include to your project's ``urls.py`` file::

    (r'^accounts/', include('captcha.backends.default.urls')),

#. Add an ``ACCOUNT_ACTIVATION_DAYS`` setting to the project's ``settings.py`` file. This is the number of days users will have to activate their accounts after registering, as required by django-registration, i.e.::
    
    ACCOUNT_ACTIVATION_DAYS = 7

#. Implement the various `templates as required by django-registration <http://docs.b-list.org/django-registration/0.8/quickstart.html#required-templates>`_.

Once done you should be able to access `/accounts/register/ <http://localhost:8000/accounts/register/>`_ and see the reCAPTCHA field in action as part of the registration process.

Credits
-------
Inspired Marco Fucci's blogpost titled `Integrating reCAPTCHA with Django <http://www.marcofucci.com/tumblelog/26/jul/2009/integrating-recaptcha-with-django>`_


``client.py`` taken from `recaptcha-client <http://pypi.python.org/pypi/recaptcha-client>`_ licenced MIT/X11 by Mike Crawford.

reCAPTCHA copyright 2011 Google.

