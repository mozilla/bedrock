.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _mozillaaccordion:

=================
Mozilla Accordion
=================

`mozilla-accordion.js` converts a section of markup into a vertically expanding/collapsing list.

**`mozilla-accordion.js` requires jQuery 1.11.0 or later, and only supports IE 8 and above. Older versions of IE are ignored.**

Each accordion requires the following HTML elements/structure:

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

Accordion Options
-----------------

``accordion-auto-init``
    Instructs the library to initialize the accordion on ``$(document).ready()``.

Persistence
-----------

If ``sessionStorage`` is available, the library will remember the open/closed state of each section on subsequent page loads.

Accordion API
-------------

Initializing new accordions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can initialize new accordions in bulk by calling the ``createAccordions`` method::

    Mozilla.Accordion.createAccordions();

This call will initialize all un-initialized accordions.

You can also initialize a single accordion by creating a new ``Mozilla.Accordion`` object, passing a reference to the ``accordion`` element::

    <div class="accordion" id="delayed-accordion">
        <!-- additional accordion markup here -->
    </div>

    <script>
        var delayedAccordion = new Mozilla.Accordion($('#delayed-accordion'));
    </script>

Programmatically created accordions may be passed a second argument containing additional configuration settings. This argument should be an object literal, and currently supports the following named keys:

``onExpand``
    A callback function that will execute when each section in the accordion expands. Will be passed the expanding ``Section`` object as an argument.

``onCollapse``
    A callback function that will execute when each section in the accordion collapses. Will be passed the collapsing ``Section`` object as an argument.

For example::

    <div class="accordion" id="delayed-accordion">
        <!-- additional accordion markup here -->
    </div>

    <script>
        var opts = {
            onExpand: function(section) {
                console.log('Expanding a section...');
            },
            onCollapse: function(section) {
                console.log('Collapsing a section...');
            }
        };

        var delayedAccordion = new Mozilla.Accordion($('#delayed-accordion'), opts);
    </script>

Once initialized, the ``accordion-initialized`` class is applied to each ``accordion`` element.

If an accordion does not have an ``id`` specified, the library will provide one during initialization in the form of ``mozilla-accordion-X``, where ``X`` represents the new accordion's creation order.

Accessing accordions
^^^^^^^^^^^^^^^^^^^^

All initialized accordions can be accessed through the ``Mozilla.Accordion.accordions`` array::

    var accordions = Mozilla.Accordion.accordions;

    // log the id of each accordion
    for (var i = 0; i < accordions.length; i++) {
        console.log(accordions[i].id);
    }

You can also find an accordion by its ``id`` using the ``Mozilla.Accordion.findAccordionById()`` function. Returns a ``Mozilla.Accordion`` object on success, ``null`` on failure::

    // assume pagers have already been initialized
    var myAccordion = Mozilla.Accordion.findAccordionById('my-accordion');

Destroying accordions
^^^^^^^^^^^^^^^^^^^^^

Accordions can be destroyed by passing the accordion's ``id`` to the ``Mozilla.Accordion.destroyAccordionById()`` function::

    <div class="accordion" id="delayed-accordion">
        <!-- additional accordion markup here -->
    </div>

    <button id="destroy-accordion">Destroy Accordion</button>

    <script>
        var delayed_accordion = new Mozilla.Accordion($('#delayed-accordion'));

        $('#destroy-accordion').on('click', function(e) {
            Mozilla.Accordion.destroyAccordionById('delayed-accordion');
        });
    </script>

This function removes the accordion from the ``Mozilla.Accordion.accordions`` array, displays all sections in the accordion, removes the ``accordion-initialized`` class, removes all WAI-ARIA attributes, and unbinds all event listeners within the accordion.

IDs added by the library are not removed.

Returns ``true`` on success and ``false`` on failure.

You can destroy *all* accordions on a page using the ``Mozilla.Accordion.destroyAccordions()`` function, which simply calls ``Mozilla.Accordion.destroyAccordionById()`` for each existing accordion.

Note that just before an accordion is destroyed, its state is saved in ``sessionStorage`` (if available).

Section properties
^^^^^^^^^^^^^^^^^^

Each ``Section`` in an accordion has the following properties:

``$header``
    A jQuery object referencing the ``data-accordion-role="tab"`` element for the ``Section``.
``$panel``
    A jQuery object referencing the ``data-accordion-role="tabpanel"`` element for the ``Section``.
``title``
    The name of the section based on the ``$header`` text. Simply a shortcut to ``$header.text()``.

Accessing sections
^^^^^^^^^^^^^^^^^^

All accordions have a ``sections`` array containing ``Section`` objects::

    var my_accordion = new Mozilla.Accordion($('#my-accordion'));

    var my_accordion_sections = my_accordion.sections;

    // log each section's title in my_accordion
    for (var i = 0; i < my_accordion_sections.length; i++) {
        console.log(my_accordion_sections[i].title);
    }

Global Settings
---------------

You can configure some appearance and behavior of the library by supplying custom values for the following. Custom values should generally be set prior to ``$(document).ready()``.

``Mozilla.Accordion.globalOnExpand``
    A callback function to be fired every time any section in any pager is expanded. Will be passed the expanding ``Section`` object as an argument.

``Mozilla.Accordion.globalOnCollapse``
    A callback function to be fired every time any section in any pager is collapsed. Will be passed the collapsing ``Section`` object as an argument.

Styling
-------

Include ``mozilla-accordion.less`` for default styling, complete with open/closed icons.

Add the ``zebra`` class to your ``accordion`` container element for striped sections.
