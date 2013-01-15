// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

(function($, trans) {
    'use strict';
    
    var $window = $(window);
    var $document = $(document);
    var $body = $('body');
    
    $("#mwc-countdown").mozcountdown({
        dayText : trans('daytext'),
        daysText : trans('daystext'),
        hoursText : trans('hourstext'),
        minutesText : trans('minutestext'),
        secondsText : trans('secondstext'),
        displayZeroDays : true,
        oneDayClass : 'one-day'
    });
    
    // Load content in a full-page modal
    $("a.modal").click(function(e) {
        e.preventDefault();
        // Extract the target element's ID from the link's href.
        var elem = $(this).attr('href').replace(/.*?(#.*)/g, '$1');
        var content = $(elem).clone();
        createModal(this, content);
    });
    
    // Create a full-page overlay and append the content
    function createModal(origin, content) {
        // Clear existing modal, if necessary,
        $('#modal').remove();
        $('.modalOrigin').removeClass('modalOrigin');

        // Create new modal
        var html = (
            '<div id="modal">' +
            '  <div class="inner">' +
            '    <button type="button" class="close">' +
            '      ' + trans('close') +
            '    </button>' +
            '  </div>' +
            '</div>'
        );

        // Add it to the page.
        $('body').addClass("noscroll").append(html);
        $("#modal .inner").append(content);
        $(origin).addClass('modalOrigin');
    }

    function closeModal() {
        $('#modal').remove();
        $('body').removeClass('noscroll');
        $('.modalOrigin').focus().remove('modalOrigin');
    }

    // Close modal on clicking close button or background.
    $document.on('click', '#modal .close', closeModal);
    $document.on('click', "#modal, #modal .inner", closeModal);

    // Close on escape
    $document.on('keyup', function(e) {
        if (e.keyCode === 27) { // esc
            closeModal();
        }
    });
    
    // Load external links in new tab/window
    $('a[rel="external"]').click( function(e) {
        e.preventDefault();
        window.open(this.href);
    });
    
})(jQuery, trans);
