/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function() {
    'use strict';

    var LazyLoad = {};
    var _selector;

    function featureDetect() {
        return 'IntersectionObserver' in window &&
               'IntersectionObserverEntry' in window &&
               'intersectionRatio' in window.IntersectionObserverEntry.prototype;
    }

    LazyLoad.supportsInsersectionObserver = featureDetect();

    /**
     * Callback iterates list of observables & lazy loads elements that intersect.
     * @param changes (Array) - IntersectionObserverEntry objects.
     * @param observer (Object) - IntersectionObserver instance.
     */
    LazyLoad.observerCallback = function(changes, observer) {
        changes.forEach(function(change) {
            if (change.intersectionRatio > 0) {

                if (change.target.dataset.srcset) {
                    change.target.srcset = change.target.dataset.srcset;
                }

                change.target.src = change.target.dataset.src;

                change.target.onload = LazyLoad.onImageLoad;
                observer.unobserve(change.target);
            }
        });
    };

    /**
     * Instantiates a new instance of IntersectionObserver and registers callback
     * for intersection events.
     * @return (Object) IntersectionObserver instance.
     */
    LazyLoad.registerObserver = function() {
        return new IntersectionObserver(LazyLoad.observerCallback);
    };

    /**
     * Observes a list of images using IntersectionObserver.
     * @param _selector (String) - CSS selector for target images e.g. '.list-item img'.
     * @return observe (Object) IntersectionObserver instance.
     */
    LazyLoad.observe = function(_selector) {
        var observer = LazyLoad.registerObserver();
        var targets = Array.prototype.slice.call(document.querySelectorAll(_selector));

        if (targets.length) {
            targets.forEach(function(target) {
                observer.observe(target);
            });
        }

        return observer;
    };

    /**
     * Fallback for older browser by simply loading all images upon page load.
     * @param _selector (String) - CSS selector for target images e.g. '.list-item img'.
     */
    LazyLoad.loadAllFallback = function(_selector) {
        $(_selector).each(function() {
            var srcset = this.getAttribute('data-srcset');

            if (srcset) {
                this.srcset = srcset;
            }

            this.src = this.getAttribute('data-src');
            this.onload = LazyLoad.onImageLoad;
        });
    };

    /**
     * Removes data-src attribute upon lazy loading of an image. This is useful
     * as it provides a CSS styling hook to allow images to fade-in.
     */
    LazyLoad.onImageLoad = function(e) {
        e.target.removeAttribute('data-src');
        e.target.removeAttribute('data-srcset');
    };

    /**
     * Initiates LazyLoad via feature detecting support for IntersectioObserver.
     * @param _selector (String) - CSS selector for target images e.g. '.list-item img'.
     */
    LazyLoad.init = function(selector) {

        // Allow passing custom selector if required.
        _selector = selector || '.lazy-image-container img';

        if (typeof _selector !== 'string') {
            throw new Error('Mozilla.LazyLoad.init: custom selector is not a string');
        }

        if (LazyLoad.supportsInsersectionObserver) {
            LazyLoad.observe(_selector);
        } else {
            LazyLoad.loadAllFallback(_selector);
        }
    };

    window.Mozilla.LazyLoad = LazyLoad;
})();
