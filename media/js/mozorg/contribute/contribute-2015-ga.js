/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    // Track clicks in main navigation
    $('#contribute-nav-menu li a').attr('data-element-location', 'nav');

    if ($('body').prop('id') === 'landing') {
        // Track user scrolling through each section on the landing page
        $('#landing .section').waypoint(function(direction) {
            if (direction === 'down') {
                var sectionclass = $(this).prop('class');
                window.dataLayer.push({event: 'scroll-tracking', section: sectionclass});
            }
        }, { offset: '100%' });

        // Track CTA clicks on landing
        $('#landing .cta a').each(function() {
            var $this = $(this);
            var position = $this.data('position');
            var label = $this.data('label');

            $this.attr({
                'data-element-location': label,
                'data-element-action': position,
                'data-tracking-flag': 'contribute-landing'
            });
        });
    }

    // Track video plays
    $('a.video-play').on('click', function() {
        var linktype = $(this).data('linktype');
        window.dataLayer.push({
            event: 'contribute-landing-interactions',
            browserAction: 'Video Interactions',
            location: linktype
        });
    });

    // Track Mozillian story clicks on the landing page
    $('.landing-stories .person .url').each(function() {
        var person = $(this).parents('.person').find('.fn').text();

        $(this).attr({
            'data-element-location': person,
            'data-element-action': 'How Mozillians Help Every Day',
            'data-tracking-flag': 'contribute-landing'
        });
    });

    // Track Mozillian story clicks on story pages
    $('.stories-other .person .url').each(function() {
        var person = $(this).parents('.person').find('.fn').text();

        $(this).attr({
            'data-element-location': person,
            'data-element-action': 'Meet a few more Mozillians',
            'data-tracking-flag': 'mozillians'
        });
    });

    // Track Twitter hashtag clicks on story pages
    $('.stories-other .section-tagline a').attr({
        'data-element-action': 'twitter search link',
        'data-element-location': '#IAmAMozillian',
        'data-tracking-flag': 'mozillians'
    });

    // Track Mozillian personal links
    $('.story-links a').each(function() {
        var person = $('.story-title .name').text();
        var link = $(this).prop('class');

        $(this).attr({
            'data-element-location': person + ' - ' + link,
            'data-element-action': 'social button click',
            'data-tracking-flag': 'mozillians'
        });
    });

    // Track other actions on landing page
    $('.landing-notready .other-actions a').attr('data-element-location', 'not ready');

    // Track other actions on confirmation page
    $('#thankyou .other-actions a').each(function() {
        var $this = $(this);

        var label = $this.data('label');

        $this.attr({
            'data-element-location': 'Other Ways to Support Mozilla',
            'data-element-action': label,
            'data-tracking-flag': 'contribute-confirmation'
        });
    });

    // Track Mozillians signup CTA on confirmation page
    $('.cta-mozillians a').attr({
        'data-element-location': 'Mozillians CTA click',
        'data-element-action': 'Yes, Create My Mozillians Account',
        'data-tracking-flag': 'contribute-confirmation'
    });

    // Track event links in the list
    $('.events-table .event-name a').attr('data-link-type', 'event');

    // Track event links in the footer
    $('.contrib-extra .event-link').attr('data-element-location', 'bottom');

    // Track 'all events' link in the footer
    $('.contrib-extra .events-all a').attr({
        'data-element-location': 'bottom',
        'data-element-action': 'See All Events'
    });

    // Track external links in the footer
    $('.extra-links a').attr('data-element-location', 'bottom');

    // Track category clicks on the signup page
    $('.option input').on('change', function() {
        var category = this.value;
        $('#inquiry-form').attr('data-contribute-category', category);
        window.dataLayer.push({
            event: 'contribute-signup-interaction',
            interaction: 'Category',
            contributeCategory: this.value
        });
    });

    // Track category area selections
    $('.area select').on('change', function() {
        var area = this.value;
        $('#inquiry-form').attr('data-contribute-area', area);
        window.dataLayer.push({
            event: 'contribute-signup-interaction',
            interaction: 'Area',
            contributeArea: area
        });
    });

    // Track signup form submissions
    $('#inquiry-form').on('submit', function(e) {
        e.preventDefault();
        var newsletterstate;
        if ($('#id_newsletter').is(':checked')) {
            newsletterstate = 'True';
        } else {
            newsletterstate = 'False';
        }

        $(this).off('submit');

        window.dataLayer.push({
            event: 'contribute-submit',
            newsletterSignup: newsletterstate
        });

        $(this).submit();
    });

});
