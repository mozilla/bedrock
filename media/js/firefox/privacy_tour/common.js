/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    var $embedWrapper = $('#fx-anniversary-video-embed-wrapper').detach();
    var $videoModalContent = $('#video-modal-content');
    var $videoButtons = $('#fx-anniversary-video-buttons');

    // move the video out of the widget and into our modal wrapper
    $videoModalContent.append($embedWrapper);

    // add some rings around the play button for ripple animation
    for (var i = 0; i < 3; i++) {
        $videoButtons.append($('<div>').addClass('ripple'));
    }

    // expose to tour.js and no-tour.js
    Mozilla.PrivacyTour = {
        $playButton: $('a.button-play'),
        $ripples: $('.ripple'),

        animateRipples: function(i) {
            if (i < this.$ripples.length) {
                var $ripple = $(this.$ripples[i]);

                $ripple.addClass('animate').on('animationend', function() {
                    $ripple.remove();
                });

                setTimeout(function() {
                    Mozilla.PrivacyTour.animateRipples(i + 1);
                }, 350);
            } else {
                var that = this;
                this.$playButton.addClass('animate').on('animationend', function() {
                    that.$playButton.find('span').addClass('visible');
                });
            }
        },

        animateHeadline: function() {
            $('.main-title').removeClass('tour');
        },

        modalEnabled: false
    };

    Mozilla.FirefoxAnniversaryVideo.init({
        'deferEmbed': true,
        'onPlay': function(button) {
            if (Mozilla.PrivacyTour.modalEnabled) {
                Mozilla.Modal.createModal(button, $videoModalContent, {
                    title: '',
                    onCreate: function() {
                        Mozilla.FirefoxAnniversaryVideo.setOverlayButtons('share-replay');

                        // give the video a bit of time to re-initialize before trying to play
                        setTimeout(function() {
                            Mozilla.FirefoxAnniversaryVideo.playEmbed();
                        }, 600);
                    },
                    onDestroy: function() {
                        Mozilla.FirefoxAnniversaryVideo.hideEmbed();
                    }
                });
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    event: 'video-interaction',
                    interaction: 'click to play',
                    videoTitle: '10th Anniversary'
                });
            } else {
                // ensure video is still accessible if tour has not initialized
                window.location.href = $('a.button-play').attr('href');
            }

        },
        'onComplete': function() {
            // YouTube player loses this callback for some reason when re-initializing after being
            // moved in the DOM. Leaving this here for future reference.
            window.dataLayer.push({
                event: 'video-interaction',
                interaction: 'Finish',
                videoTitle: '10th Anniversary'
            });
        }
    });
})(window.jQuery, window.Mozilla);
