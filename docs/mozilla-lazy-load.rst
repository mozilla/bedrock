.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _mozillalazyload:

=========================
Mozilla Image Lazy Loader
=========================

``mozilla-lazy-load.js`` is a JavaScript library that will lazy load ``<img>`` elements on a web page as the user scrolls the viewport. It requires support for `Intersection Observer API`_, and will fallback to loading all images on page load in non-supporting browsers.

Usage
-----

Each image to be lazy loaded should match the following HTML structure::

    <div class="lazy-image-container">
        <img class="lazy-image" src="path/to/placeholder.png" data-src="path/to/image.png" data-srcset="path/to/image-high-res.png 2x" alt="">
        <noscript>
            <img class="lazy-image" src="path/to/image.png" srcset="path/to/image-high-res.png 2x" alt="">
        </noscript>
    </div>

This above HTML snippet is also available via a handy Python helper that can be used directly in any bedrock template::

    {{ lazy_img(image_url='path/to/image.png', placeholder_url='path/to/placeholder.png', include_highres_image=True, optional_attributes={'class': 'some-class-name'}) }}

Parameters
~~~~~~~~~~

- ``image_url`` - Path to final image ``src``.
- ``placeholder_url`` - Path to placeholder image for use before final image is loaded. This image should be small in file size, and can be shared between all images on a page that are to be lazy loaded.
- ``include_highres_image`` - A boolean value to indicate a high resolution version of an image is available. When ``True``, the function will automatically look for the image in the ``image_url`` parameter suffixed with `'-high-res'` and switch to it if the display has high pixel density. Defaults to ``False``.
- ``optional_attributes`` - A dictionary of custom HTML attributes you may want to add to an image.

To initialize the lazy loading plugin, in your JS run::

    Mozilla.LazyLoad.init();

Options
~~~~~~~

If you don't want to use the Python helper provided above and instead use your own HTML, you can pass an alternate custom CSS selecter::

    <div class="my-own-lazy-loading-container">
        <img src="path/to/placeholder.png" data-src="path/to/image.png" data-srcset="path/to/image-high-res.png 2x" alt="">
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

.. _Intersection Observer API: https://developer.mozilla.org/docs/Web/API/Intersection_Observer_API
