/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function(w, $, enquire, Modernizr, trans) {
    'use strict';

    // tablet is good enough for full experience?
    enquire.register("screen and (min-width: 760px)", {
        deferSetup: true, // don't run setup until mq matches
        setup: function() {
            Modernizr.load([{
                both: [ '/media/js/libs/jquery.pageslide.min.js', '/media/js/libs/tweenmax.min.js', '/media/js/libs/superscrollorama.js', '/media/js/libs/jquery.spritely-0.6.1.js', '/media/js/firefox/partners/desktop.js' ],
                complete: function() {
                    // no action needed?
                }
            }]);
        },
        match: function() {
            // TODO: attach desktop hooks
        },
        unmatch: function() {
            // TODO: detach desktop hooks

            // currently no way of unbinding superscrollorama stuff (wut!?)
            // however, only desktop users should ever go from desktop to mobile, so...it's ok?
        }
    // true param here forces non-mq browsers to match this rule, so, i don't think we need a polyfill
    }, true).register("screen and (max-width: 759px)", {
        deferSetup: true,
        setup: function() {
            Modernizr.load([{
                both: [ '/media/js/firefox/partners/mobile.js' ],
                complete: function() {
                    w.attach_mobile();
                }
            }]);
        },
        match: function() {
            // handler must exist
        },
        unmatch: function() {
            w.detach_mobile();
        }
    }, false).listen();

    // global overlay handler (mobile/desktop)
    var $overlay = $('#overlay');

    $("a.modal").click(function(e) {
        e.preventDefault();
        // Extract the target element's ID from the link's href.
        var elem = $(this).attr('href').replace(/.*?(#.*)/g, '$1');

        $overlay.find('section').hide();
        $(elem).show();

        var content = $overlay.detach();
        createModal(this, content);

        return false;
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

        $('#modal #overlay').fadeIn('fast');

        $(origin).addClass('modalOrigin');
    }

    function closeModal() {
        $('#modal').fadeOut('fast', function() {
            $overlay.hide();
            var content = $overlay.detach();
            $('#overlay-container').append(content);
            $(this).remove();
        });
        $('body').removeClass('noscroll');
        $('.modalOrigin').focus().remove('modalOrigin');
    }

    // Close modal on clicking close button or background.
    $(w.document).on('click', '#modal .close', closeModal);

    // Close on escape
    $(w.document).on('keyup', function(e) {
        if (e.keyCode === 27) { // esc
            closeModal();
        }
    });
})(window, window.jQuery, window.enquire, window.Modernizr, window.trans);
