.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _newsletters:

===========
Newsletters
===========

Bedrock includes support for signing up for and managing subscriptions and
preferences for Mozilla newsletters.

By default, every page's footer has a form to signup for the default newsletters,
"Mozilla Foundation" and "Firefox & You".

Features
--------

- ability to subscribe to a newsletter from a page's footer area. Many pages
  on the site might include this.

- whole pages devoted to subscribing to one newsletter, often with custom
  text, branding, and layout

- newsletter preference center - allow user to change their email address,
  preferences (e.g. language, HTML vs. text), which newsletters they're
  subscribed to, etc. Access is limited by requiring a user-specific
  token in the URL (it's a UUID).  The full URL is included as a link in
  each newsletter sent to the user, which is the only way (currently) they
  can get the token.

- landing pages that user ends up on after subscribing. These can vary depending
  on where they're coming from.

Newsletters
-----------

Newsletters have a variety of characteristics. Some of these are implemented
in Bedrock, others are transparent to Bedrock but implemented in the
basket back-end that provides our interface to the newsletter vendor.

- Public name - the name that is displayed to users, e.g. "Firefox Weekly Tips".

- Internal name- a short string that is used internal to Bedrock and basket
  to identify a newsletter. Typically these are lowercase strings of words
  joined by hyphens, e.g. "firefox-tips".  This is what we send to basket
  to identify a newsletter, e.g. to subscribe a user to it.

- Show publicly - pages like the newsletter preferences center show a list
  of unsubscribed newsletters and allow subscribing to them. Some newsletters
  aren't included in that list by default (though they are shown if the
  user is already subscribed, to let them unsubscribe).

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

  Because drip campaigns depend on the signup date of the user, we're careful
  not to accidentally change the signup date, which could happen if we sent
  redundant subscription commands to our backend.

Bedrock and Basket
------------------

Bedrock is the user-facing web application. It presents an interface for
users to subscribe and manage their subscriptions and preferences. It does
not store any information. It gets all newsletter and user-related
information, and makes updates, via web requests to the Basket server.

The Basket server implements an HTTP API for the newsletters.  The front-end
(Bedrock) can make calls to it to retrieve or change users' preferences and
subscriptions, and information about the available newsletters. Basket
implements some of that itself, and other functions by
calling the newsletter vendor's API. Details of that are outside the scope
of this document, but it's worth mentioning that both the user token (UUID)
and the newsletter internal name mentioned above are used only between
Bedrock and Basket.

URLs
----

Here are a few important URLs implemented. These were established before
Bedrock came along and so are unlikely to be changed.

(Not all of these might be implemented in Bedrock yet.)

/newsletter/ - subscribe to 'mozilla-and-you' newsletter (public name: "Firefox & You")

/newsletter/existing/USERTOKEN/ - user management of their preferences and subscriptions


Configuration
-------------

Currently, information about the available newsletters is configured in
Basket. `See Basket for more information <https://basket.readthedocs.io/>`_.

Footer signup
-------------

Customize the footer signup form by overriding the email_form template
block.  For example, to have no signup form:

.. code-block:: jinja

    {% block email_form %}{% endblock %}

The default is:

.. code-block:: jinja

    {% block email_form %}{{ email_newsletter_form() }}{% endblock %}

which gives a signup for Firefox & You.  You can pass parameters to the
macro ``email_newsletter_form`` to change that.  For example, the
``newsletters`` parameter controls which newsletter is signed up for,
and ``title`` can override the text:

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
include_language=[True|False] and/or include_country=[True|False].

You can also use the same form outside a page footer by passing ``footer=False``
to the macro.

You can also specify one of three color variants for the "Sign Up Now" button. The options are:

* default - Which sets the border and font color to a light blue [#00afe5]
* dark - Which sets the border and font color to the dark Firefox blue [00539F]
* white - Which sets the border and font color to white [#fff]

This is done in a template as follows:

.. code-block:: jinja

    # default
    {% block email_form %}
        {{ email_newsletter_form() }}
    {% endblock %}

    # dark
    {% block email_form %}
        {{ email_newsletter_form(button_class='button-dark') }}
    {% endblock %}

    # white
    {% block email_form %}
        {{ email_newsletter_form(button_class='button-light') }}
    {% endblock %}
