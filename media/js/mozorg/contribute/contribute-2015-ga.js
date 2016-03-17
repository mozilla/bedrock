/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    var $inquiryForm = $('#inquiry-form');

    if ($('body').prop('id') === 'landing') {
        // Track user scrolling through each section on the landing page
        $('#landing .section').waypoint(function(direction) {
            if (direction === 'down') {
                var sectionclass = $(this).prop('class');

                window.dataLayer.push({
                    'event': 'scroll-section',
                    'section': sectionclass
                });
            }
        }, { offset: '100%' });
    }

    // Track video plays
    $('a.video-play').on('click', function() {
        var linktype = $(this).data('linktype');
        window.dataLayer.push({
            'event': 'contribute-landing-interactions',
            'browserAction': 'Video Interactions',
            'location': linktype
        });
    });

    // Track category clicks on the signup page
    $('.option input').on('change', function() {
        var category = this.value;
        $inquiryForm.attr('data-contribute-category', category);
        window.dataLayer.push({
            'event': 'contribute-signup-interaction',
            'interaction': 'Category',
            'contributeCategory': category
        });
    });

    // Track category area selections
    $('.area select').on('change', function() {
        var area = this.value;
        $inquiryForm.attr('data-contribute-area', area);
        window.dataLayer.push({
            'event': 'contribute-signup-interaction',
            'interaction': 'Area',
            'contributeArea': area
        });
    });

    // Track signup form submissions
    $inquiryForm.on('submit', function(e) {
        e.preventDefault();
        var newsletterstate;
        if ($('#id_newsletter').is(':checked')) {
            newsletterstate = 'True';
        } else {
            newsletterstate = 'False';
        }

        $(this).off('submit');


        window.dataLayer.push({
            'event': 'contribute-signup-submit',
            'contributeArea': $inquiryForm.attr('data-contribute-area'),
            'countrySelected': $('#id_country option:selected').text()
        });

        $(this).submit();
    });

});
