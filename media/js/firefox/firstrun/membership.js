/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    var client = Mozilla.Client;
    var _supportsWebAnimations = 'animate' in document.createElement('div');
    var _supportsPromises = 'Promise' in window;
    var cutsTheMustard = _supportsWebAnimations && _supportsPromises;
    var $slideShow = $('.carousel');
    var button = document.querySelectorAll('.path-selector ul > li > button');
    var step1 = document.querySelector('.step-1');
    var step2 = document.querySelector('.step-2');
    var laterLink = document.querySelector('a.later');

    function initSlideShow() {
        $slideShow.cycle({
            fx: 'scrollHorz',
            log: false,
            slides: '> .carousel-item',
            pager: '> .carousel-pager',
            pauseOnHover: true,
            speed: 620,
            timeout: 6000,
            delay: 5000
        });

        $slideShow.on('cycle-pager-activated', function(event, opts) {
            var slide;
            switch(opts.currSlide) {
            case 0:
                slide = 'Independence';
                break;
            case 1:
                slide = 'Privacy';
                break;
            case 2:
                slide = 'Technology';
                break;
            }

            if (slide) {
                window.dataLayer.push({
                    'event': 'in-page-interaction',
                    'eAction': 'Carousel',
                    'eLabel': slide
                });
            }
        });
    }

    function initAccountsForm() {
        if (client.isFirefoxDesktop) {
            // initialize FxA iframe form
            client.getFirefoxDetails(function(data) {
                Mozilla.FxaIframe.init({
                    distribution: data.distribution,
                    gaEventName: 'firstrun-fxa'
                });
            });
        }
    }

    // replaces utm_campaign param in FxA iframe data-src with data-id value from button click.
    function updateUTMParam(id) {
        var utmCampaign = id ? encodeURIComponent(id) : 'fxa-embedded-form';
        var iframe = document.getElementById('fxa');
        var dataSrc = iframe.dataset.src;
        iframe.dataset.src = dataSrc.replace('utm_campaign=fxa-embedded-form', 'utm_campaign=' + utmCampaign);
    }

    // animates page to step2 and loads the FxA sign up form.
    function goToStep2() {

        // fancy transision requires Web Animations and Promise support.
        if (cutsTheMustard) {
            fadeOutStep1().then(function() {
                // destroy slider on step-1 as no longer needed.
                $slideShow.cycle('destroy');
                // fade in step 2.
                fadeInStep2().then(initAccountsForm).catch(function(reason) {
                    throw new Error(reason);
                });
            }).catch(function(reason) {
                throw new Error(reason);
            });
        }
        // fallback to simple non-animated transition.
        else {
            step1.classList.add('hidden');
            $slideShow.cycle('destroy');

            step2.classList.remove('hidden');
            initAccountsForm();
        }
    }

    function onButtonClick(e) {
        e.preventDefault();
        updateUTMParam(e.target.dataset.id);
        unbindEvents();
        goToStep2();

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'Button Click',
            'eLabel': e.target.dataset.label
        });
    }

    function onButtonMouseOver(e) {
        $slideShow.cycle('pause'); //pause auto-running slideshow
        $slideShow.cycle('goto', e.target.dataset.index); //go to specific path
    }

    function onButtonMouseOut() {
        $slideShow.cycle('resume'); //resume auto-running slideshow
    }

    function onLaterLinkClick() {
        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'Link Click',
            'eLabel': 'Skip this step'
        });
    }

    function bindEvents() {
        for (var i = 0; i < button.length; i++) {
            button[i].addEventListener('mouseover', onButtonMouseOver, false);
            button[i].addEventListener('mouseout', onButtonMouseOut, false);
            button[i].addEventListener('click', onButtonClick, false);
        }

        laterLink.addEventListener('click', onLaterLinkClick, false);
    }

    function unbindEvents() {
        for (var i = 0; i < button.length; i++) {
            button[i].removeEventListener('mouseover', onButtonMouseOver, false);
            button[i].removeEventListener('mouseout', onButtonMouseOut, false);
            button[i].removeEventListener('click', onButtonClick, false);
        }

        laterLink.removeEventListener('click', onLaterLinkClick, false);
    }

    function animateElement(selector, keyframes, options) {
        return new Promise(function(resolve, reject) {
            var element = document.querySelector(selector);

            if (element) {
                var animation = element.animate(keyframes, options);
                animation.onfinish = function() {
                    resolve(true);
                };
            } else {
                reject('animateElement: Element for selector "' + selector +  '" not found.');
            }
        });
    }

    function fadeOutStep1() {
        return new Promise(function(resolve, reject) {
            var keyframes = [
                { opacity: 1 },
                { opacity: 0 }
            ];

            var options = {
                duration: 200,
                fill: 'forwards',
                easing: 'ease-out',
            };

            animateElement('.step-1', keyframes, options).then(function() {
                step1.classList.add('hidden');
                resolve(true);
            }).catch(function(reason) {
                reject(reason);
            });
        });
    }

    function fadeInStep2() {
        return new Promise(function(resolve, reject) {
            var keyframes = [
                { opacity: 0 },
                { opacity: 1 }
            ];

            var options = {
                duration: 200,
                fill: 'forwards',
                easing: 'ease-in',
            };

            step2.classList.remove('hidden');

            animateElement('.step-2', keyframes, options).then(function() {
                resolve(true);
            }).catch(function(reason) {
                reject(reason);
            });
        });
    }

    initSlideShow();
    bindEvents();

})(window.Mozilla);
