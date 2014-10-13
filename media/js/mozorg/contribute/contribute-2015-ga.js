/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    // Track clicks in main navigation
    $('#contribute-nav-menu li a').on('click', function() {
        var label = $(this).data('label');
        var page = $('body').prop('id');
        gaTrack(['_trackEvent', 'Contribute Nav Interactions', 'nav click', page, label]);
    });

    // track user scrolling through each section down the page
    $('.section').waypoint(function(direction) {
        if (direction === 'down') {
            var sectionclass = $(this).prop('class');
            gaTrack(['_trackEvent', '/contribute Interactions', 'scroll', sectionclass]);
        }
    }, { offset: '100%' });

    // Track CTA clicks on landing
    $('#landing .cta a').on('click', function() {
        var position = $(this).data('position');
        var label = $(this).data('label');
        gaTrack(['_trackEvent', '/contribute Interactions', position, label]);
    });

    // Track video plays
    $('.video-play').on('click', function() {
        var linktype = $(this).data('linktype');
        gaTrack(['_trackEvent', '/contribute Interactions', 'Video Interactions', linktype]);
    });

    // Track Mozillian story clicks on the landing page
    $('.landing-stories .stories .url').on('click', function(){
        var person = $(this).parents('.person').find('.fn').text();
        gaTrack(['_trackEvent', '/contribute Interactions', 'How Mozillians Help Every Day', person]);
    });

    // Track Mozillian story clicks on story pages
    $('.stories-other .stories .url').on('click', function(){
        var person = $(this).parents('.person').find('.fn').text();
        gaTrack(['_trackEvent', '/contribute/stories/ Interactions', 'Meet a few more Mozillians', person]);
    });

    // Track other actions on landing page
    $('.landing-notready .other-actions a').on('click', function(){
        var label = $(this).data('label');
        gaTrack(['_trackEvent', '/contribute Interactions', 'Not Ready to Dive in Just Yet', label]);
    });

    // Track other actions on confirmation page
    $('#thankyou .other-actions a').on('click', function(){
        var label = $(this).data('label');
        gaTrack(['_trackEvent', '/contribute/thankyou/ Interactions', 'Other Ways to Support Mozilla', label]);
    });

    // Track Mozillians signup CTA on confirmation page
    $('.cta-mozillians a').on('click', function(){
        gaTrack(['_trackEvent', '/contribute/thankyou/ Interactions', 'primary CTA click', 'Yes, Create My Mozillians Account']);
    });
});
