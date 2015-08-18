/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function() {
    'use strict';

    var pager = Mozilla.Pager.pagers[0];
    var $documentRoot = $(document);
    var $firstPager = $('.pager').first();

    // scroll to top of pager when switching tabs so all
    // tab content is visible after switching tabs
    pager.$container.on('changePage', function() {

        // Get the current document scroll position
        var scrollPos = $(document).scrollTop();

        // Get the offset of the top of the pager section
        var pagerTopPos = $firstPager.offset().top;

        // If we're scrolled passed the header, jump back up
        // to the tabs when the tab is switched
        if (scrollPos > pagerTopPos) {
            $documentRoot.scrollTop($firstPager.offset().top);
        }
    });

    // enable sticky tab nagivation
    new Waypoint.Sticky({
        element: $('#button-nav-wrapper')
    });

    // Setup GA tracking for main tabs
    $('#tips-nav-direct a').on('click', function() {
        var thisTabName = $(this).attr('href');

        window.dataLayer.push({
            event: 'privacy-interactions',
            browserAction: thisTabName.substr(1),
            interaction: 'Tab Click'
        });
    });

    // Setup GA tracking for paragraph and list links
    $('.tip-column p a, .tip-column li a').attr({
        'data-element-action': pager.currentPage.id,
        'data-interaction': 'href',
        'data-tracking-flag': 'privacy'

    });

    // Setup GA tracking TED video link
    $('.tip-column p a, .tip-column li a').attr({
        'data-element-action': pager.currentPage.id,
        'data-interaction': 'Why Privacy Matters CTA Btn',
        'data-tracking-flag': 'privacy'
    });

    // Setup GA tracking for next tab buttons
    $('.tip-footer .next a').on('click', function(e) {
        e.preventDefault();
        pager.nextPageWithAnimation();
        window.dataLayer.push({
            event: 'privacy-interactions',
            browserAction: pager.currentPage.id,
            interaction: 'Next'
        });
    });

    // Setup GA tracking for previous tab buttons
    $('.tip-footer .previous a').on('click', function(e) {
        e.preventDefault();
        pager.prevPageWithAnimation();
        window.dataLayer.push({
            event: 'privacy-interactions',
            browserAction: pager.currentPage.id,
            interaction: 'Previous'
        });
    });

});
