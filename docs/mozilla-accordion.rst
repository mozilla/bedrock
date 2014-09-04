.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _mozillaaccordion:

=================
Mozilla Accordion
=================

`mozilla-accordion.js` converts a section of markup into a vertically expanding/collapsing list. Each accordion requires the following HTML elements/structure:

- An accordion container element with the class ``accordion``, which contains,
    - Multiple section containing elements (commonly ``<section>`` tags), each which contain,
        - Any element with a ``data-accordion-role`` attribute set to ``tab`` (commonly an ``<h[1-6]>`` tag)
        - Any element with a ``data-accordion-role`` attribute set to ``tabpanel`` (commonly a ``<div>`` tag)

A very basic example might look like::

    <div class="accordion">
        <section>
            <h2 data-accordion-role="tab">Section 1</h2>
            <div data-accordion-role="tabpanel">
                Section 1 content that will be displayed when the above heading is clicked.
            </div>
        </section>

        <section>
            <h2 data-accordion-role="tab">Section 2</h2>
            <div data-accordion-role="tabpanel">
                Section 2 content that will be displayed when the above heading is clicked.
            </div>
        </section>
    </div>

In the above example, the ``<h2>`` elements are given click handlers that toggle the open/closed state of the sibling ``<div>``.

Note that the ``tab`` and ``tabpanel`` elements must be siblings, and must be direct descendants of the section container.

Styling
-------

Include ``mozilla-accordion.less`` for default styling, complete with open/closed icons.

Add the ``zebra`` class to your ``accordion`` container element for striped sections.

Persistence
-----------

If ``sessionStorage`` is available, the library will remember the open/closed state of each section on subsequent page loads.

Analytics
---------

The library will automatically send a Google Analytics event each time a user clicks to expand or collapse a section.

Examples
--------

You can view simple examples by navigating to ``/styleguide/docs/mozilla-accordion/`` in your local development environment (not available in production).
