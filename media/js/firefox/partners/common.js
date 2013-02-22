/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function(w, $, enquire, Modernizr, trans) {
    'use strict';

    var _load_mobile = function() {
        w.Modernizr.load([{
            both: MOBILE_JS_FILES,
            complete: function() {
                w.attach_mobile();
            }
        }]);
    };

    if (($.browser.msie && parseInt($.browser.version, 10) < 9)) {
        _load_mobile();
    } else {
        enquire.register("screen and (max-width: 999px)", {
            deferSetup: true,
            setup: function() {
                _load_mobile();
            },
            match: function() {
                // handler must exist
            },
            unmatch: function() {
                closeModal();
                w.detach_mobile();
            }
        }, false).register("screen and (min-width: 1000px)", {
            deferSetup: true,
            setup: function() {
                    Modernizr.load([{
                        both: DESKTOP_JS_FILES,
                        complete: function() {
                            // no action needed?
                        }
                    }]);
            },
            match: function() {
                // handler must exist
                // desktop hooks are added when desktop.js is loaded (in setup above)
            },
            unmatch: function() {
                // rather difficult to unbind all the fancy desktop js. in the interest
                // of time, just reload the page when we get to mobile size.
                // (should be a rare use case)
                w.location.reload();
            }
        }, true).listen();
    }

    // global overlay handler (mobile/desktop)
    var $overlay = $('#overlay');

    w.show_overlay = function(elem) {
        $overlay.find('section').hide();
        $(elem).show();

        var content = $overlay.detach();
        createModal(this, content);

        w.ga_track(elem.replace(/#/, '') + '/');
    };

    $("a.modal").click(function(e) {
        e.preventDefault();
        // Extract the target element's ID from the link's href.
        var elem = $(this).attr('href').replace(/.*?(#.*)/g, '$1');

        w.show_overlay(elem);

        return false;
    });

    // modal functions pilfered from existing MWC landing page

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

        $form.fadeOut('fast', function() {
            $('.sf-form').addClass('completed');
            $('#pageslide').scrollTop(0);
            $('.form-results').fadeIn('fast');
        });

        $.ajax({
            url: $form.attr('action'),
            data: $form.serialize(),
            type: $form.attr('method')
        });

        w.ga_track('form/submit/');
    });

    var path_parts = window.location.pathname.split('/');
    var query_str = window.location.search ? window.location.search + '&' : '?';
    var referrer = path_parts[path_parts.length-2];
    var locale = path_parts[1];
    var last_virtual_page;

    // GA tracking
    w.ga_track = function(virtual_page) {
        if (w._gaq) {
            if (last_virtual_page !== virtual_page) {
                w._gaq.push(['_trackPageview', '/' + locale + '/firefox/partners/' + virtual_page]);

                last_virtual_page = virtual_page;
            }
        }
    };

    // set a cookie
    document.cookie = 'seen_mwc2013=true;expires=Tue, 5 Mar 2013 00:00:01 UTC;path=/';

})(window, window.jQuery, window.enquire, window.Modernizr, window.trans);
