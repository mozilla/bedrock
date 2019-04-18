/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var variation = document.querySelector('.mzp-c-hero.t-mission').getAttribute('data-variant');

    function setDelay() {
        var delay = {
            backgrounds: null,
            fonts: null,
            images: null,
            text: null,
            ui: null,
        };

        switch(variation) {
        case 'b':
            delay.backgrounds = 0;
            delay.fonts = 1000;
            delay.images = 750;
            delay.text = 0;
            delay.ui = 0;
            break;
        case 'c':
            delay.backgrounds = 750;
            delay.fonts = 2000;
            delay.images = 1500;
            delay.text = 500;
            delay.ui = 500;
            break;
        case 'd':
            delay.backgrounds = 1500;
            delay.fonts = 3000;
            delay.images = 2250;
            delay.text = 1000;
            delay.ui = 1000;
            break;
        case 'e':
            delay.backgrounds = 2250;
            delay.fonts = 4000;
            delay.images = 3000;
            delay.text = 1500;
            delay.ui = 1500;
            break;
        case 'f':
            delay.backgrounds = 3000;
            delay.fonts = 5000;
            delay.images = 3750;
            delay.text = 3000;
            delay.ui = 3000;
            break;
        case 'g':
            delay.backgrounds = 3750;
            delay.fonts = 6000;
            delay.images = 4500;
            delay.text = 3500;
            delay.ui = 3500;
            break;
        case 'h':
            delay.backgrounds = 4500;
            delay.fonts = 7000;
            delay.images = 5250;
            delay.text = 4000;
            delay.ui = 4000;
            break;
        case 'i':
            delay.backgrounds = 5250;
            delay.fonts = 8000;
            delay.images = 6000;
            delay.text = 4500;
            delay.ui = 4500;
            break;
        case 'j':
            delay.backgrounds = 6000;
            delay.fonts = 9000;
            delay.images = 6750;
            delay.text = 5000;
            delay.ui = 5000;
            break;
        default:
            delay.backgrounds = 0;
            delay.fonts = 0;
            delay.images = 0;
            delay.text = 0;
            delay.ui = 0;
        }

        return delay;
    }


    var delay = setDelay();

    setTimeout(function() {
        document.querySelector('body').classList.remove('backgrounds-invisible');
    }, delay.backgrounds);

    setTimeout(function() {
        document.querySelector('body').classList.remove('ui-invisible');
    }, delay.ui);

    setTimeout(function() {
        document.querySelector('body').classList.remove('text-invisible');
    }, delay.text);

    setTimeout(function() {
        // Lazyload images
        Mozilla.LazyLoad.init();
        document.querySelector('body').classList.remove('images-invisible');
    }, delay.images);

    setTimeout(function() {
        document.querySelector('body').classList.remove('fonts-delayed');
    }, delay.fonts);

    window.dataLayer.push({
        'data-ex-name': 'about_page_performance',
        'data-ex-variant': 'v_' + variation
    });
})();
