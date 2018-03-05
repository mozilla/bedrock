.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _mozillapager:

=============
Mozilla Pager
=============

``mozilla-pager.js`` converts a section of markup into a tabbed or carousel interface. At minimum, each pager requires the following HTML elements:

**``mozilla-pager.js`` requires jQuery 1.11.0 or later.**

- A container with the class ``pager``, which contains,
    - A container with the class ``pager-content``, which contains,
        - Multiple containers with the class ``pager-page``.

A very basic (yet fully functional) example might look like::

    <div class="pager pager-auto-init pager-with-nav">
        <div class="pager-content">
            <div class="pager-page">
                <p>Page 1</p>
            </div>
            <div class="pager-page">
                <p>Page 2</p>
            </div>
        </div>
    </div>

See below for explanation of the ``pager-auto-init`` and ``pager-with-nav`` classes.

Defaults
--------

All pagers have the following default behaviors:

- The first page (the first element with class ``pager-page``) will be displayed when the pager is initialized. Can be overridden using either the ``default-page`` class on a specific ``pager-page`` element, or by using the ``pager-random`` class on the ``pager`` element.
- The URL hash will be updated when navigating to a page other than the default page. This URL hash will be honored on page reload, displayed the last viewed pager page. Can be overridden using the ``pager-no-history`` class on the ``pager`` element.

Pager options
-------------

Each pager can be individually configured through classes on the
container ``pager`` element:

``pager-auto-init``
    Instructs the library to initialize the pager on ``$(document).ready()``.
``pager-with-tabs``
    Instructs the ``pager`` to look for a child element with the class
    ``pager-tabs``. Links within this element will be used to show specific
    pages. For example::

        <div class="pager pager-auto-init pager-with-tabs">
            <ol class="pager-tabs">
                <li><a href="#page1">Page 1</a></li>
                <li><a href="#page2">Page 2</a></li>
            </ol>
            <div class="pager-content">
                <div id="page1" class="pager-page">
                    <p>Page 1</p>
                </div>
                <div id="page2" class="pager-page">
                    <p>Page 2</p>
                </div>
            </div>
        </div>

    The ``pager-tabs`` element will usually either be a ``<ul>`` or ``<ol>``, but can be any element you wish. **Note that tab anchor tags must be inside of a container, such as an** ``<li>`` (as shown above).

    The anchor tag linking to the currently displayed page will have a ``selected`` class applied.

``pager-with-nav``
    Instructs the pager to generate and insert navigational markup directly before the ``pager-content`` element. The **generated markup** would look like::


        <div class="pager pager-auto-init pager-with-nav" id="mozilla-pager-1">

            <!-- BEGIN GENERATED MARKUP -->
            <div class="pager-nav">
                <span class="pager-nav-page-number">1 / 2</span>
                <fieldset class="pager-nav-links-wrapper" aria-controls="mozilla-pager-1-pages">
                    <button type="button" class="pager-prev" disabled="disabled" aria-label="Previous">Previous</button>
                    <span class="pager-nav-divider"></span>
                    <button type="button" class="pager-next" aria-label="Next">Next</button>
                </fieldset>
            </div>
            <!-- END GENERATED MARKUP -->

            <div class="pager-content" id="mozilla-pager-1-pages">
                <div id="page1" class="pager-page">
                    <p>Page 1</p>
                </div>
                <div id="page2" class="pager-page">
                    <p>Page 2</p>
                </div>
            </div>
        </div>

    The appearance of the nav can easily be customized by writing your own selectors for the relevant CSS class names.

``pager-no-history``
    Instructs the library **not** to update the URL hash with the currently visible page.
``pager-random``
    The pager will display a random page when initialized.
``pager-auto-rotate``
    The pager will automatically rotate through all pages, looping when when reaching the last page. Rotation will pause when the page is either focused or moused over.

Page options
------------

Each page inside the pager can be customized by applying the following classes to the ``pager-page`` element:

``default-page``
    Sets the page as the default page for the pager. If not provided, defaults to first ``pager-page`` element.

Pager API
---------

Initializing new pagers
^^^^^^^^^^^^^^^^^^^^^^^

You can initialize new pagers in bulk by calling the ``createPagers`` method::

    Mozilla.Pager.createPagers();

This call will initialize all un-initialized pagers.

You can also initialize a single pager by creating a new ``Mozilla.Pager`` object, passing in the ``.pager`` element as a jQuery object::

    <div class="pager" id="delayed-pager">
        <!-- additional pager markup here -->
    </div>

    <script>
        var delayedPager = new Mozilla.Pager($('#delayed-pager'));
    </script>

Once initialized, the ``pager-initialized`` class is applied to each ``pager`` element.

If a pager does not have an ``id`` specified, the library will provide one during initialization in the form of ``mozilla-pager-X``, where ``X`` represents the new pager's creation order.

Accessing pagers
^^^^^^^^^^^^^^^^

All initialized pagers can be accessed through the ``Mozilla.Pager.pagers`` array::

    var pagers = Mozilla.Pager.pagers;

    // log the id of each pager
    for (var i = 0; i < pagers.length; i++) {
        console.log(pagers[i].id);
    }

You can also find a pager by its ``id`` using the ``Mozilla.Pager.findPagerById()`` function. Returns a ``Mozilla.Pager`` object on success, ``null`` on failure::

    // assume pagers have already been initialized
    var myPager = Mozilla.Pager.findPagerById('my-pager');

Destroying pagers
^^^^^^^^^^^^^^^^^

Pagers can be destroyed by passing the pager's ``id`` to the ``Mozilla.Pagers.destroyPagerById()`` function::

    <div class="pager" id="delayed-pager">
        <!-- additional pager markup here -->
    </div>

    <button id="destroy-pager">Destroy Pager</button>

    <script>
        var delayed_pager = new Mozilla.Pager($('#delayed-pager'));

        $('#destroy-pager').on('click', function(e) {
            Mozilla.Pager.destroyPagerById('delayed-pager');
        });
    </script>

This function removes the pager from the ``Mozilla.Pager.pagers`` array, removes any generated navigational markup, displays all pages in the pager, removes the ``pager-initialized`` class, and unbinds all event listeners within the pager.

IDs and WAI-ARIA attributes added by the library are not removed.

Returns ``true`` on success and ``false`` on failure.

You can destroy *all* pagers on a page using the ``Mozilla.Pager.destroyPagers()`` function, which simply calls ``Mozilla.Pager.destroyPagerById()`` for each existing pager.

Accessing pages
^^^^^^^^^^^^^^^

All pagers have a ``pages`` array containing ``Mozilla.Page`` objects::

    var my_pager = new Mozilla.Pager($('#my-pager'));

    var my_pager_pages = my_pager.pages;

    // log each page in my_pager
    for (var i = 0; i < my_pager_pages.length; i++) {
        console.log(my_pager_pages[i]);
    }

Changing pages
^^^^^^^^^^^^^^

A pager's currently displayed page can be set through a variety of methods:

``nextPageWithAnimation``
    Moves the pager to the next page in the set. Will loop back to the first page if currently on the last page. Optionally takes a numeric ``duration`` (in milliseconts) parameter::

        var my_pager = new Mozilla.Pager($('#my-pager'));

        my_pager.nextPageWithAnimation();

``prevPageWithAnimation``
    Moves the pager to the previous page in the set. Will loop back to the last page if currently on the first page. Optionally takes a numeric ``duration`` (in milliseconds) parameter::

        var my_pager = new Mozilla.Pager($('#my-pager'));

        my_pager.prevPageWithAnimation(400);

``setPage``
    Sets the current page to the passed ``Mozilla.Page`` object::

        var my_pager = new Mozilla.Pager($('#my-pager'));

        var my_pager_pages = my_pager.pages;

        // display the third page
        my_pager.setPage(my_pager_pages[2]);

``setPageWithAnimation``
    Same as ``setPage``, but with fade in/fade out animations. Takes an optional numeric ``duration`` (in milliseconds) parameter::

        var my_pager = new Mozilla.Pager($('#my-pager'));

        var my_pager_pages = my_pager.pages;

        // display the second page
        my_pager.setPageWithAnimation(my_pager_pages[1], 450);

Global Settings
---------------

You can configure some appearance and behavior of the library by supplying custom values for the following. Custom values should generally be set prior to ``$(document).ready()``.

``Mozilla.Pager.PAGE_DURATION``
    Time taken for page to fade in/out from tab and nav interaction. Defaults to ``150`` (milliseconds).

``Mozilla.Pager.PAGE_AUTO_DURATION``
    Time taken for page to fade in/out during auto rotate. Defaults to ``850`` (milliseconds).

``Mozilla.Pager.AUTO_ROTATE_INTERVAL``
    Time page is visible during auto rotate. Defaults to ``7000`` (milliseconds).

``Mozilla.Pager.NEXT_TEXT``
    Sets the text displayed in the `next` link in the generated navigation. Defaults to 'Next'. Note that any new value supplied should be localized (likely using the ``Mozilla.Utils.trans`` function).

``Mozilla.Pager.PREV_TEXT``
    Same as above, but for the `previous` link.

``Mozilla.Pager.HIDDEN_CLASS``
    Sets the CSS class used to hide pages. If overridden, should set ``display: none;`` for ARIA purposes. Defaults to ``hidden``.
