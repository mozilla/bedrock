/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {
    function getUrlVars() {
        // Function to read URL Get variables.
        // from http://papermashup.com/read-url-get-variables-withjavascript/
        var vars = {};
        window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
            vars[key] = value;
        });
        return vars;
    }

    function validate_domain(url, trusted_domains) {
        // Function to validate that callback url points
        // to a trusted domain.
        for (var domain in trusted_domains) {
            var regex = new RegExp(trusted_domains[domain]);
            if (regex.test(url)) {
                return true;
            }
        }
        return false;
    }

    var $opportunities = $('#opportunities');
    function scrollTo($el) {
        var top = $el.offset().top;
        $("html:not(:animated),body:not(:animated)").animate(
            { scrollTop: top - 20 },
            100
        );
    }

    var pager = Mozilla.Pager.rootPagers[0];

    $('#interest-header').click(function(e) {
        e.preventDefault();
        pager.setPageWithAnimation(pager.pagesById['interest']);
        scrollTo($opportunities);
    });

    $('#location-header').click(function(e) {
        e.preventDefault();
        pager.setPageWithAnimation(pager.pagesById['location']);
        scrollTo($opportunities);
    });

    $('#time-header').click(function(e) {
        e.preventDefault();
        pager.setPageWithAnimation(pager.pagesById['time']);
        scrollTo($opportunities);
    });

    $('#help-form').submit(function(e) {
        // This function submits the 'help-form' and -if applicable-
        // pings using POST the callbackurl.
        //
        // We send requests serialy and make sure the POSTing to
        // callbackurl completes before we POST the form.

        $(this).unbind('submit');

        e.preventDefault();

        callback_url = getUrlVars()['callbackurl'];

        trusted_domains = ['^https://reps.mozilla.org/',
                           '^https://reps.allizom.org/',
                           '^https://reps-dev.allizom.org/',
                           '^http://127.0.0.1:8000/'];

        if (callback_url && validate_domain(callback_url, trusted_domains)) {
            $('#form-content').hide();
            $('#submit-wait').show();

            $.post(callback_url).complete(function() {
                $('#help-form').submit();
            });
        }
        else {
            $(this).submit();
        }
    });

    $('#thank-you').delay(8500).fadeOut('fast', function() {
        $('#form-content').fadeIn('fast');
    });
});
