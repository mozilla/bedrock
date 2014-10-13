/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function () {
    'use strict';

    // Track clicks in main navigation
    $('#contribute-nav-menu li a').on('click', function(e) {
        var label = $(this).data('label');
        var page = $('body').prop('id');
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Contribute Nav Interactions ', 'nav click - ' + page, label]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Contribute Nav Interactions ', 'nav click - ' + page, label], callback);
        }
    });

    if ($('body').prop('id') === 'landing') {
        // Track user scrolling through each section on the landing page
        $('#landing .section').waypoint(function(direction) {
            if (direction === 'down') {
                var sectionclass = $(this).prop('class');
                gaTrack(['_trackEvent', 'Contribute Landing Interactions', 'scroll', sectionclass]);
            }
        }, { offset: '100%' });

        // Track CTA clicks on landing
        $('#landing .cta a').on('click', function(e) {
            var position = $(this).data('position');
            var label = $(this).data('label');
            var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
            var href = this.href;
            var callback = function() {
                window.location = href;
            };

            if (newTab) {
                gaTrack(['_trackEvent', 'Contribute Landing Interactions', position, label]);
            } else {
                e.preventDefault();
                gaTrack(['_trackEvent', 'Contribute Landing Interactions', position, label], callback);
            }
        });
    }

    // Track video plays
    $('a.video-play').on('click', function() {
        var linktype = $(this).data('linktype');
        gaTrack(['_trackEvent', 'Contribute Landing Interactions', 'Video Interactions', linktype]);
    });

    // Track Mozillian story clicks on the landing page
    $('.landing-stories .person .url').on('click', function(e) {
        var person = $(this).parents('.person').find('.fn').text();
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Contribute Landing Interactions', 'How Mozillians Help Every Day', person]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Contribute Landing Interactions', 'How Mozillians Help Every Day', person], callback);
        }
    });

    // Track Mozillian story clicks on story pages
    $('.stories-other .person .url').on('click', function(e) {
        var person = $(this).parents('.person').find('.fn').text();
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Mozillian Stories Interactions', 'Meet a few more Mozillians', person]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Mozillian Stories Interactions', 'Meet a few more Mozillians', person], callback);
        }
    });

    // Track Twitter hashtag clicks on story pages
    $('.stories-other .section-tagline a').on('click', function(e) {
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Mozillian Stories Interactions', 'twitter search link', '#IAmAMozillian']);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Mozillian Stories Interactions', 'twitter search link', '#IAmAMozillian'], callback);
        }
    });

    // Track Mozillian personal links
    $('.story-links a').on('click', function(e) {
        var person = $('.story-title .name').text();
        var link = $(this).prop('class');
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Mozillian Stories Interactions', 'social button click', person + ' - ' + link]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Mozillian Stories Interactions', 'social button click', person + ' - ' + link], callback);
        }
    });

    // Track other actions on landing page
    $('.landing-notready .other-actions a').on('click', function(e) {
        var label = $(this).data('label');
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Contribute Landing Interactions', 'Not Ready to Dive in Just Yet', label]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Contribute Landing Interactions', 'Not Ready to Dive in Just Yet', label], callback);
        }
    });

    // Track other actions on confirmation page
    $('#thankyou .other-actions a').on('click', function(e) {
        var label = $(this).data('label');
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Contribute Confirmation Interactions', 'Other Ways to Support Mozilla', label]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Contribute Confirmation Interactions', 'Other Ways to Support Mozilla', label], callback);
        }
    });

    // Track Mozillians signup CTA on confirmation page
    $('.cta-mozillians a').on('click', function(e) {
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Contribute Confirmation Interactions', 'Mozillians CTA click', 'Yes, Create My Mozillians Account']);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Contribute Confirmation Interactions', 'Mozillians CTA click', 'Yes, Create My Mozillians Account'], callback);
        }
    });

    // Track event links in the list
    $('.events-table .event-name a').on('click', function(e) {
        var eventname = $(this).text();
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Contribute Events Interactions', 'event link click', eventname]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Contribute Events Interactions', 'event link click', eventname], callback);
        }
    });

    // Track event links in the footer
    $('.contrib-extra .event-link').on('click', function(e) {
        var page = $('body').prop('id');
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Contribute Interactions', 'Contribute Extra Links at Bottom - ' + page, href]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Contribute Interactions', 'Contribute Extra Links at Bottom - ' + page, href], callback);
        }
    });

    // Track 'all events' link in the footer
    $('.contrib-extra .events-all a').on('click', function(e) {
        var page = $('body').prop('id');
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Contribute Interactions', 'Contribute Extra Links at Bottom - ' + page, 'See All Events']);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Contribute Interactions', 'Contribute Extra Links at Bottom - ' + page, 'See All Events'], callback);
        }
    });

    // Track external links in the footer
    $('.extra-links a').on('click', function(e){
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;
        var callback = function() {
            window.location = href;
        };

        if (newTab) {
            gaTrack(['_trackEvent', 'Contribute Interactions', 'Contribute Extra Links at Bottom', href]);
        } else {
            e.preventDefault();
            gaTrack(['_trackEvent', 'Contribute Interactions', 'Contribute Extra Links at Bottom', href], callback);
        }
    });

    // Track category clicks on the signup page
    $('.option input').on('change', function() {
        gaTrack(['_trackEvent', 'Contribute Signup Interactions', 'Category - ' + this.value, 'SELECTED']);
    });

    // Track category area selections
    $('.area select').on('change', function() {
        gaTrack(['_trackEvent', 'Contribute Signup Interactions', 'Area - ' + this.value]);
    });

    // Track signup form submissions
    $('#inquiry-form').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var newsletterstate;

        if ($('#id_newsletter').is(':checked')) {
            newsletterstate = 'True';
        } else {
            newsletterstate = 'False';
        }

        form.off('submit');
        gaTrack(['_setCustomVar',13,'Contribute Signup Form - Main Area of Contribution', form.find('input[name="category"]').val(), 3]);
        gaTrack(['_setCustomVar',14,'Contribute Signup Form Form - Contribution Drop-Down Value', form.find('.area:visible select').val(), 3]);
        gaTrack(['_setCustomVar',15,'Contribute Signup Form Form - Sign Up for Newsletter', newsletterstate, 3]);
        gaTrack(['_trackEvent', 'Contribute Signup Form Interactions', 'successful submit', 'Start Contributing'], function() {
            form.submit();
        });
    });

});
