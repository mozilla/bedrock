.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _mozillalazyload:

=========================
Mozilla Image Lazy Loader
=========================

``mozilla-lazy-load.js`` is a JavaScript library that will lazy load ``<img>`` elements on a web page as the user scrolls the viewport. It requires support for `Intersection Observer API`_, and will fallback to loading all images on page load in non-supporting browsers.**

Usage
-----

Each image to be lazy loaded requires the following HTML structure::

    <div class="lazy-image-container">
        <img src="path/to/placeholder.png" data-src="path/to/image.png" alt="">
        <noscript>
            <img src="path/to/image.png" alt="">
        </noscript>
    </div>

This HTML snippet is also available via a handy macro that can be imported into any bedrock template::

    {% from "macros.html" import lazy_image with context %}

The macro can then be used like so in a template like so::

    {{ lazy_image('path/to/image.png', 'path/to/placeholder.png') }}

To initialize the lazy loading plugin, in your JS run::

    Mozilla.LazyLoad.init();

Options
~~~~~~~

If you don't want to use the macro provided above and instead use your own HTML, you can pass an alternate custom CSS selecter::

    <div class="my-own-lazy-loading-container">
        <img src="path/to/placeholder.png" data-src="path/to/image.png" alt="">
        <noscript>
            <img src="path/to/image.png" alt="">
        </noscript>
    </div>

    Mozilla.LazyLoad.init('.my-own-lazy-loading-container');

This will instantiate the plugin to observe intersection of elements using the DOM elements matching the selector provided.

Fading in images
----------------

By default the lazy load plugin will simply swap in images as they load. To add a little extra visual flourish, you can add a custom fade-in effect using CSS::

    .lazy-image-container img {
        display: block;
        opacity: 1;
        transition: opacity 0.3s;
    }

    .lazy-image-container img[data-src] {
        opacity: 0;
        display: none;
    }

This works because the plugin removes the ``data-src`` attribute as each image lazy loads.

Examples
--------

You can view a live example by navigating to ``/firefox/features/`` and scrolling down the page.

.. _Intersection Observer API: https://developer.mozilla.org/docs/Web/API/Intersection_Observer_API
