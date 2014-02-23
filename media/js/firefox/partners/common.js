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

    $("a.modal").click(function(e) {
        e.preventDefault();

        // Extract the target element's ID from the link's href.
        var target_id = $(this).attr('href').replace(/.*?(#.*)/g, '$1');
        var $elem = $(target_id);

        // Move overlay title into modal header (save vertical space)
        var opts = {};
        var $overlay_title = $elem.find('.overlay-title:first');

        if ($overlay_title.length > 0) {
            opts.title = $overlay_title.text();
        }

        // special callback for the map
        if (target_id === '#map' && typeof(window.scrollMwcMap) === 'function') {
            opts.onCreate = window.scrollMwcMap;
        }

        Mozilla.Modal.createModal(this, $elem, opts);

        return false;
    });

    // ajax-ify form
    $('#sf-form').on('submit', function(e) {
        e.preventDefault();

        var $form = $(this);

        $.ajax({
            url: $form.attr('action'),
            data: $form.serialize(),
            type: $form.attr('method'),
            success: function() {
                $form.fadeOut('fast', function() {
                    $('.sf-form').addClass('completed');
                    $('#pageslide').scrollTop(0);
                    $('.form-results').fadeIn('fast');
                });
            },
            error: function(xhr, status, error) {
                // grab json string from server and convert to JSON obj
                var json = $.parseJSON(xhr.responseText);
                Mozilla.FormHelper.displayErrors(json.errors, $form);
            }
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
                window._gaq.push(['_trackPageview', '/' + locale + '/firefox/partners/' + virtual_page]);

                last_virtual_page = virtual_page;
            }
        }
    };

    // Load external links in new tab/window
    $('a[rel="external"]').click(function(e){
        e.preventDefault();
        var opts = $(this).data('windowOpts');
        if (opts) {
            window.open(this.href, '_blank', $(this).data('windowOpts'));
        } else {
            window.open(this.href);
        }
    });

    // set a cookie
    document.cookie = 'seen_mwc2014=true;expires=Tue, 4 Mar 2014 00:00:01 UTC;path=/';
})(window, window.jQuery, window.enquire, window.Modernizr, window.trans);
