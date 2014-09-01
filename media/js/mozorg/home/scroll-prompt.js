/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

 // create namespace
if (typeof Mozilla == 'undefined') {
    var Mozilla = {};
}

$(function () {
    'use strict';

    // create namespace
    if (typeof Mozilla.Homepage == 'undefined') {
        Mozilla.Homepage = {};
    }

    var $window = $(window);
    var $scrollPrompt = $('#scroll-prompt');
    var $promoGrid = $('.promo-grid');
    var promptTimeout;

    function destroyScrollPrompt() {
        clearTimeout(promptTimeout);
        $window.off('scroll.prompt', scroll);
        $scrollPrompt.off('click', scrollToPromos);
        $scrollPrompt.stop().fadeOut();
    }

    function scrollToPromos() {
        destroyScrollPrompt();

        $('html, body').animate({
            scrollTop: $promoGrid.offset().top + 302
        }, 1000);
    }

    function initScrollPrompt() {
        var windowWidth = $window.innerWidth();
        var isMediumViewport = (windowWidth > 660) && (windowWidth <= 1300);

        // only show the prompt on medium sized viewports if the user
        // does not start to scroll for after 5 seconds.
        if (isMediumViewport && !$window.scrollTop() > 0) {
            promptTimeout = setTimeout(function () {
                if (!$window.scrollTop() > 0) {
                    $scrollPrompt.fadeIn();
                    $scrollPrompt.on('click', scrollToPromos);
                    $window.one('scroll.prompt', destroyScrollPrompt);
                    // track that the scroll prompt has been show in GA
                    gaTrack(['_trackEvent', 'Homepage Interactions', 'scroll prompt']);
                }
            }, 4000);
        }
    }

    // this function will be called via Optimizely as part of a test
    // to see if the prompt encourages people on smaller viewports
    // to scroll down the promos.
    Mozilla.Homepage.initScrollPrompt = initScrollPrompt;
});
