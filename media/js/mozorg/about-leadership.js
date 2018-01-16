/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Mozilla) {
    'use strict';

    var ltr = document.dir === 'ltr';
    var utils = Mozilla.Utils;

    // Set up the modal navigation
    var navModal = function(direction) {
        var $origin = $('.modal-origin').removeClass('modal-origin');
        var personId;

        if (direction === 1) {
            $origin = $origin.next().length ? $origin.next()
                                            : $origin.siblings(':first');
            personId = $origin.attr('id');
        } else {
            $origin = $origin.prev().length ? $origin.prev()
                                            : $origin.siblings(':last');
            personId = $origin.attr('id');
        }

        $('#modal').attr('aria-labelledby', personId).trigger('focus');
        $('#modal .overlay-contents').replaceWith($origin.clone().attr('tabindex', '0').addClass('overlay-contents'));
        $('#modal header h1').text($origin.find('.fn').text());

        $origin.addClass('modal-origin');
    };

    // Set up the modal
    $('.has-bio').each(function() {
        var $this = $(this);
        var modalTitle = '<h1>' + $this.find('.fn').text() + '</h1>';

        $this.attr({
            'tabindex': '0'
        }).on('click', function() {

            Mozilla.Modal.createModal(this, $this.clone().removeAttr('id'), {
                title: modalTitle,
                'onCreate': function() {
                    var $nav = $('<nav role="presentation"></nav>').insertBefore('#modal-close');

                    $('<button class="next" aria-controls="modal"></button>')
                        .text(utils.trans('global-next')).appendTo($nav);
                    $('<button class="prev" aria-controls="modal">prev</button>')
                        .text(utils.trans('global-previous')).appendTo($nav);

                    $nav.on('click', 'button', function() {
                        var $this = $(this);

                        navModal($this.hasClass('prev') ? -1 : 1);
                    });
                }
            });

        }).on('keydown', function(event) {
            if (event.keyCode === 13) { // Enter
                $this.trigger('click');
            }
        });

    });

    // Set up keyboard shortcuts for the modal
    $(document).on('keydown', '#modal', function(event) {
        var direction = 0;

        switch (event.keyCode) {
        case 37: // Left arrow
            direction = ltr ? -1 : 1;
            break;
        case 38: // Up arrow
            direction = -1;
            break;
        case 39: // Right arrow
            direction = ltr ? 1 : -1;
            break;
        case 40: // Down arrow
            direction = 1;
            break;
        }

        if (direction) {
            event.preventDefault();
            navModal(direction);
        }
    });

    // trigger modal on page load if hash is present and matches a person with a bio
    if (window.location.hash) {
        var $target = $(window.location.hash);

        if ($target.length && $target.hasClass('vcard has-bio')) {
            $target.trigger('click');
        }
    }

})(window.jQuery, window.Mozilla);
