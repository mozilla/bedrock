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
        }
    };

    Mozilla.FirefoxAnniversaryVideo.init({
        'deferEmbed': true,
        'onPlay': function(button) {
            Mozilla.Modal.createModal(button, $videoModalContent, {
                title: '',
                onCreate: function() {
                    Mozilla.FirefoxAnniversaryVideo.setOverlayButtons('share-replay');
                    Mozilla.FirefoxAnniversaryVideo.playEmbed();
                },
                onDestroy: function() {
                    Mozilla.FirefoxAnniversaryVideo.hideEmbed();
                }
            });
        }
    });
})(window.jQuery, window.Mozilla);
