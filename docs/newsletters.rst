.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _newsletters:

===========
Newsletters
===========

Bedrock includes support for signing up for and managing subscriptions and
preferences for Mozilla newsletters.

Many pages have a form to sign-up for the default newsletters, "Mozilla
Foundation" and "Firefox & You". Other pages have more specific sign up
forms, such as the contribute page, or Mozilla VPN wait-list page.

Features
--------

- Ability to subscribe to a newsletter from a web form. Many pages
  on the site might include this form.

- Whole pages devoted to subscribing to one newsletter, often with custom
  text, branding, and layout.

- Newsletter preference center - allow user to change their email preferences
  (e.g. language, HTML vs. text), as well as which newsletters they're
  subscribed to, etc. Access is limited by requiring a user-specific
  token in the URL (it's a UUID).  The full URL is included as a link in
  each newsletter sent to the user. Users can also recover a link to their
  token by visiting the newsletter recovery page and entering their email
  address.

Newsletters
-----------

Newsletters have a variety of characteristics. Some of these are implemented
in Bedrock, others are transparent to Bedrock but implemented in the
basket back-end that provides our interface to the newsletter vendor.

- Public name - the name that is displayed to users, e.g. "Firefox Weekly Tips".

- Internal name - a short string that is used internal to Bedrock and basket
  to identify a newsletter. Typically these are lowercase strings of words
  joined by hyphens, e.g. "firefox-tips". This is what we send to basket
  to identify a newsletter, e.g. to subscribe a user to it.

- Show publicly - pages like the newsletter preferences center show a list
  of unsubscribed newsletters and allow subscribing to them. Some newsletters
  aren't included in that list by default (though they are shown if the
  user is already subscribed, to let them unsubscribe). If the user has a
  Mozilla account, there are also some other related newsletters that will
  always be shown in the list.

- Languages - newsletters are available in a particular set of languages.
  Typically when subscribing to a newsletter, a user can choose their
  preferred language. We should try not to let them subscribe to a newsletter
  in a language that it doesn't support.

  The backend only stores one language for the user though, so whenever
  the user submits one of our forms, whatever language they last submitted
  is what is saved for their preference for everything.

- Welcome message - each newsletter can have a canned welcome message that
  is sent to a user when they subscribe to it. Newsletters should have both
  an HTML and a text version of this.

- Drip campaigns - some newsletters implement so-called drip campaigns, in
  which a series of canned messages are dribbled out to the user over a
  period of time. E.g. 1 week after subscribing, they might get message 1;
  a week later, message 2, and so on until all the canned messages have been
  sent.

  Because drip campaigns depend on the sign-up date of the user, we're careful
  not to accidentally change the sign-up date, which could happen if we sent
  redundant subscription commands to our backend.

Bedrock and Basket
------------------

Bedrock is the user-facing web application. It presents an interface for
users to subscribe and manage their subscriptions and preferences. It does
not store any information. It gets all newsletter and user-related information,
and makes updates, via web requests to the Basket server. These requests are
made typically made by Bedrock's front-end JavaScript modules.

The Basket server implements an HTTP API for the newsletters. The front-end
(Bedrock) can make calls to it to retrieve or change users' preferences and
subscriptions, and information about the available newsletters. Basket
implements some of that itself, and other functions by calling the newsletter
vendor's API. Details of that are outside the scope of this document, but it's
worth mentioning that both the user token (UUID) and the newsletter internal
name mentioned above are used only between Bedrock and Basket.

`See the Basket docs for more information <https://basket.readthedocs.io/>`_.

URLs
----

Here are a few important mozorg newsletter URLs. Some of these were established before
Bedrock came along, and so are unlikely to be changed.

- ``/newsletter/`` - Subscribe to 'mozilla-and-you' newsletter (public name: "Firefox & You")

- ``/newsletter/existing/{USERTOKEN}/`` - User management of their preferences and subscriptions.

- ``/newsletter/confirm/{USERTOKEN}/`` - URL someone lands on when they confirm their email address after initially subscribing.

- ``/newsletter/country/{USERTOKEN}/`` - Allows users to change their country.

- ``/newsletter/recovery/`` - Allows users to recover a link containing their token so they can manage their subscriptions.

- ``/newsletter/updated/`` - A page users are redirected to after updating their details, or unsubscribing.

.. note::

    URLs that contain ``{USERTOKEN}`` will have their path rewritten on page load
    so that they no longer contain the token e.g. ``/newsletter/existing/{USERTOKEN}/``
    will be rewritten to just ``/newsletter/existing/``. This helps to prevent
    accidental sharing of user tokens in URLS and also against referral
    information leakage.

Footer sign-up
--------------

In some common templates, you can customize the footer sign-up form by
overriding the email_form template block. For example, to have no sign-up form:

.. code-block:: jinja

    {% block email_form %}{% endblock %}

The default is:

.. code-block:: jinja

    {% block email_form %}{{ email_newsletter_form() }}{% endblock %}

This will render a sign-up for "Firefox & You". You can pass parameters to the
macro ``email_newsletter_form`` to change that.  For example, the ``newsletters``
parameter controls which newsletter is signed up for, and ``title`` can override
the text:

.. code-block:: jinja

    {% block email_form %}
        {{ email_newsletter_form('app-dev',
                                 'Sign up for more news about the Firefox Marketplace.') }}
    {% endblock %}

The `newsletters` parameter, the first positional argument, can be either a list
of newsletter IDs or a comma separated list of newsletters IDs:

.. code-block:: jinja

    {% block email_form %}
        {{ email_newsletter_form('mozilla-foundation, mozilla-and-you') }}
    {% endblock %}

Pages can control whether country or language fields are included by passing
``include_language=[True|False]`` and/or ``include_country=[True|False]``.
