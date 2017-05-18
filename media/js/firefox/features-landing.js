/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var supportsInsersectionObserver = typeof IntersectionObserver !== 'undefined';

    function observerCallback(changes, observer) {
        changes.forEach(function(change) {
            if (change.intersectionRatio > 0) {
                change.target.src = change.target.dataset.src;
                change.target.onload = function() {
                    change.target.removeAttribute('data-src');
                };
                observer.unobserve(change.target);
            }
        });
    }

    function lazyLoad() {
        var observer = new IntersectionObserver(observerCallback);
        var targets = Array.prototype.slice.call(document.querySelectorAll('.features-list-item img'));

        if (targets.length) {
            targets.forEach(function(target) {
                observer.observe(target);
            });
        }
    }

    function loadAll() {
        $('.features-list-item img').each(function() {
            this.src = this.getAttribute('data-src');
            this.onload = function() {
                this.removeAttribute('data-src');
            };
        });
    }

    if (supportsInsersectionObserver) {
        lazyLoad();
    } else {
        loadAll();
    }
})();
