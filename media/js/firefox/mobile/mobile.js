/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla, $) {
    'use strict';

    var $body = $('body');
    var $mobileDownloadButtons = $('.mobile-download-buttons').remove();
    var $modalContents = $('#modal-wrapper');

    function openModal(e) {
        e.preventDefault();

        var product = $(this).data('product');

        var selectorToHide = (product === 'firefox') ? '.focus' : '.firefox';
        var selectorToShow = (product === 'firefox') ? '.firefox' : '.focus';

        // control styling of modal: blue for firefox, purple for focus
        $body.attr('data-modal-product', product);

        $modalContents.find(selectorToHide).addClass('hidden');
        $modalContents.find(selectorToShow).removeClass('hidden');

        Mozilla.Modal.createModal(this, $modalContents);
    }

    // move app store badges inside modal
    $('#modal-mobile-download-buttons-wrapper').append($mobileDownloadButtons);

    // clicking any download-looking button opens the modal
    $('.get-firefox, .get-focus').attr('role', 'button').on('click', openModal);

    // add class to widget button here to avoid messing with macro markup
    $('#send-to-device button[type="submit"]').addClass('quantum-hollow');

    // anchor 'See more' links should smooth scroll
    $('.see-more').on('click', function(e) {
        e.preventDefault();

        var offset = $(e.target.getAttribute('href')).offset().top;

        Mozilla.smoothScroll({
            top: offset
        });
    });

    // initialize send to device widget
    var form = new Mozilla.SendToDevice();

    form.init();
})(window.Mozilla, window.jQuery);
