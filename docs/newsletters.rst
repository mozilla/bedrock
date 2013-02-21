.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _newsletters:

===========
Newsletters
===========

Bedrock includes support for signing up for and managing subscriptions and
preferences for Mozilla newsletters.

By default, every page's footer has a form to signup for the default newsletter,
"Firefox & You".

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

  QUESTION: what do we do if a user later changes their global language
  preference to one that some of their subscribed newsletters don't support?
  Language seems to be a single preference in basket and our vendor -
  this might boil down to what our vendor does in this case.

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

/newsletter/hacks.mozilla.org/ - subscribe to 'app-dev' newsletter ('Firefox Apps & Hacks').
This one is displayed as a frame inside some other page(s), so it works differently than
the other signup pages.

/newsletter/existing/USERTOKEN/ - user management of their preferences and subscriptions

/newsletter/new/ - user lands here after subscribing via /newsletter/ and is offered the chance to sign up for more newsletters.



Configuration
-------------

Currently, information about the available newsletters is configured in the
Django settings. It is hoped that can be retrieved dynamically from the
backend at some point.

The most important setting looks like this example:

.. code-block:: python

    MOZILLA_NEWSLETTERS = SortedDict()   # Allow setting display order by the order we set here
    for newsletter, data in (
        (    'mozilla-and-you' , {
                'title' : 'Firefox & You',
                'desc' : 'A monthly newsletter packed with tips to improve your browsing experience.',
                'show': True}),
        (    'about-mozilla' , {'title' : 'About Mozilla'}),
        ):
        MOZILLA_NEWSLETTERS[newsletter] = data


MOZILLA_NEWSLETTERS is a dictionary whose keys are internal names for
the newsletters, and whose values are dictionaries with information
about the newsletters.

The dictionary is ordered, so that pages display the newsletters in the
order they're configured here.

Every newsletter has a title. Some have a description
in ``'desc'``.

On pages that list multiple newsletters to sign up for, we show the
newsletters that have ``'show'`` present and ``True``, plus any that the
user is already signed up for.

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
``newsletter_id`` parameter controls which newsletter is signed up for,
and ``title`` can override the text:

.. code-block:: jinja

    {% block email_form %}
        {{ email_newsletter_form('app-dev',
                                 _('Sign up for more news about the Firefox Marketplace.')) }})
    {% endblock %}

Pages can control whether country or language fields are included by passing
include_language=[True|False] and/or include_country=[True|False].

Creating a signup page
----------------------

Start with a template that extends ``'newsletter/one_newsletter_signup.html'``.
It's probably simplest to copy an existing one, like ``'newsletter/mobile.html'``.

The name of the template *must* be the internal name of newsletter, e.g.
for the newsletter with internal name ``mobile``, the template is
``'newsletter/mobile.html'``.  (The view could easily be enhanced to allow
overriding this if needed.)

Override at least the `page_title` and `newsletter_content` blocks:

.. code-block:: jinja

    {% block page_title %}Firefox and You{% endblock %}

    {% block newsletter_content %}
      <div id="main-feature">
        <h2>Subscribe to <span>about:mobile</span>!</h2>
        <p>Our about:mobile newsletter brings you the latest and greatest news
            from the Mozilla contributor community.
        </p>
      </div>
    {% endblock %}

Then add a url to ``newsletter/urls.py``:

.. code-block:: python

    # "about:mobile"
    url(r'^newsletter/about_mobile/$',
        views.one_newsletter_signup,
        kwargs={'newsletter': 'mobile'},
        name='newsletter.mobile',
    ),

Pass the newsletter internal name, and choose a URL and URL name. The view
will do the rest.  Look at the parent template and the view code to learn
more.
