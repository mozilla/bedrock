/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function(w, $, enquire, Modernizr, trans) {
    'use strict';

    enquire.register("screen and (max-width: 759px)", {
        deferSetup: true,
        setup: function() {
            Modernizr.load([{
                both: [ '/media/js/firefox/partners/mobile.js' ],
                complete: function() {
                    //alert("mobile");
                    w.attach_mobile();
                }
            }]);
        },
        match: function() {
            //alert("mobile match!");
            // handler must exist
        },
        unmatch: function() {
            w.detach_mobile();
        }
    }, false).register("screen and (min-width: 760px)", {
        deferSetup: true, // don't run setup until mq matches
        setup: function() {
            //if (!($.browser.msie && parseInt($.browser.version, 10) >= 9)) {
                Modernizr.load([{
                    both: [ '/media/js/libs/jquery.pageslide.min.js', '/media/js/libs/tweenmax.min.js', '/media/js/libs/superscrollorama.js', '/media/js/libs/jquery.spritely-0.6.1.js', '/media/js/firefox/partners/desktop.js' ],
                    complete: function() {
                        //alert("desktop");
                        // no action needed?
                    }
                }]);
            //}
        },
        match: function() {
            //alert("desktop match!");
            // TODO: attach desktop hooks
        },
        unmatch: function() {
            // TODO: detach desktop hooks
            w.location.reload();

            // currently no way of unbinding superscrollorama stuff (wut!?)
            // however, only desktop users should ever go from desktop to mobile, so...it's ok?
        }
    // true param here forces non-mq browsers to match this rule, so, i don't think we need a polyfill
    }, true).listen();

    // global overlay handler (mobile/desktop)
    var $overlay = $('#overlay');

    w.show_overlay = function(elem) {
        $overlay.find('section').hide();
        $(elem).show();

        var content = $overlay.detach();
        createModal(this, content);
    };

    $("a.modal").click(function(e) {
        e.preventDefault();
        // Extract the target element's ID from the link's href.
        var elem = $(this).attr('href').replace(/.*?(#.*)/g, '$1');

        w.show_overlay(elem);

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

    // ajax-ify form
    $('#sf-form').on('submit', function(e) {
        e.preventDefault();

        var $form = $(this);

        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: $form.serialize(),
            success: function(data, status, xhr) {
                $form.fadeOut('fast', function() {
                    $('.sf-form').addClass('completed');
                    $('#pageslide').scrollTop(0);
                    $('.form-results').fadeIn('fast');
                });
            }
        });
    });
})(window, window.jQuery, window.enquire, window.Modernizr, window.trans);
