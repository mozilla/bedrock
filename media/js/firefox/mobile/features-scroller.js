/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// this is a modified fork of /js/firefox/quantum/features-scroller.js

(function (Mozilla, Waypoint) {
    'use strict';

    var features = document.querySelectorAll('.features-scroller-content > .feature-content');
    var featureWaypoints = [];
    var navs;

    // Basic feature detect for JS support.
    function cutsTheMustard() {
        return 'querySelector' in document &&
               'querySelectorAll' in document &&
               'addEventListener' in window &&
               'classList' in document.createElement('div') &&
               typeof window.matchMedia !== 'undefined';
    }

    // Returns an elements position offset from the top of the page.
    function findPosition(obj) {
        var top = 0;
        do {
            top += obj.offsetTop;
            obj = obj.offsetParent;
        } while (obj);

        return top;
    }

    function scrollToFeature(e) {
        e.preventDefault();
        var targetName = e.target.getAttribute('href').replace(/#/, '');
        var targetElem = document.getElementById(targetName);

        if (targetElem) {
            Mozilla.smoothScroll({
                top: findPosition(targetElem)
            });
        }
    }

    function setActiveFeature(id, parent) {
        var currentElem = document.querySelector('#' + parent + ' .features-scroller-nav a.current');
        var el = document.querySelector('#' + parent + ' .features-scroller-nav a[href="#' + id + '"]');

        if (currentElem) {
            currentElem.classList.remove('current');
        }

        if (el) {
            el.classList.add('current');

            // data-current attribute provides a styling hook for the CSS faux scroll bar.
            for (var i = 0; i < navs.length; i++) {
                if (navs[i].getAttribute('data-section') === parent) {
                    navs[i].setAttribute('data-current', id);
                    break;
                }
            }
        }
    }

    function trackGAScroll(el) {
        var label = el.getAttribute('data-ga-label');

        if (label) {
            // remove attributes so we only track scroll for each element once.
            el.removeAttribute('data-ga-label');

            window.dataLayer.push({
                'eAction': 'scroll',
                'eLabel': label,
                'event': 'non-interaction'
            });
        }
    }

    function scrollToPrevFeature(e) {
        var parent = e.target.getAttribute('data-section');
        var currentElem = document.querySelector('#' + parent + ' .features-scroller-nav a.current');

        if (currentElem) {
            var prevElem = currentElem.parentNode.previousElementSibling;

            if (prevElem) {
                prevElem.firstChild.click();
            }
        }
    }

    function scrollToNextFeature(e) {
        var parent = e.target.getAttribute('data-section');
        var currentElem = document.querySelector('#' + parent + ' .features-scroller-nav a.current');

        if (currentElem) {
            var nextElem = currentElem.parentNode.nextElementSibling;

            if (nextElem) {
                nextElem.firstChild.click();
            }
        }
    }

    function initNavigation() {
        var navLinks = document.querySelectorAll('.features-scroller-nav a');
        var prevButtons = document.querySelectorAll('.features-scroller-nav .previous');
        var nextButtons = document.querySelectorAll('.features-scroller-nav .next');

        var i;

        for (i = 0; i < navLinks.length; i++) {
            navLinks[i].addEventListener('click', scrollToFeature, false);
        }

        for (i = 0; i < prevButtons.length; i++) {
            prevButtons[i].addEventListener('click', scrollToPrevFeature, false);
        }

        for (i = 0; i < nextButtons.length; i++) {
            nextButtons[i].addEventListener('click', scrollToNextFeature, false);
        }
    }

    function initWaypoints() {
        for (var i = 0; i < features.length; i++) {
            featureWaypoints.push(new Waypoint({
                element: features[i],
                handler: function(direction) {
                    // select the feature associated with this waypoint
                    if (direction === 'down') {
                        setActiveFeature(this.element.id, this.element.getAttribute('data-section'));
                        trackGAScroll(this.element);
                    // going up!
                    } else {
                        // if there's a feature above this waypoint, select it
                        if (this.options.index > 0) {
                            var prevFeature = features[this.options.index - 1];
                            setActiveFeature(prevFeature.id, prevFeature.getAttribute('data-section'));
                        }
                    }
                },
                offset: '50%',
                index: i
            }));
        }
    }

    function destroyWaypoints() {
        if (featureWaypoints.length > 0) {
            featureWaypoints.forEach(function(waypoint) {
                waypoint.destroy();
            });
            featureWaypoints = [];
        }
    }

    function initMediaQueries() {
        var desktopWidth;

        desktopWidth = matchMedia('(min-width: 1000px)');

        if (desktopWidth.matches) {
            initWaypoints();
        }

        desktopWidth.addListener(function(mq) {
            if (mq.matches) {
                initWaypoints();
            } else {
                destroyWaypoints();
            }
        });
    }

    if (cutsTheMustard()) {
        navs = document.querySelectorAll('.features-scroller-nav');

        initMediaQueries();
        initNavigation();
    }

})(window.Mozilla, window.Waypoint);
