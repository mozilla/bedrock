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
        // Unbind Submit button to prevent double posting.
        $('#help-form').unbind('submit');

        // Validate that the callback points to one of the allowed domains.
        callback_url = getUrlVars()['callbackurl'];

        trusted_domains = ['^https://reps.mozilla.org/',
                           '^https://reps.allizom.org/',
                           '^https://reps-dev.allizom.org/',
                           '^http://127.0.0.1:8000/'];

        if (callback_url && validate_domain(callback_url, trusted_domains)) {
            // We are synchronously POSTing to callback_url, so that
            // we complete the request before proceeding with POSTing
            // the form. If we do it async a race condition between
            // the two posts takes place, which may result in aborting
            // this POST.
            //
            // Because the POSTing to callback_url can take a second
            // or two, we display the 'submit-wait' div in the place
            // of 'form-content' to let the user know that we are
            // working in the background.
            $('#form-content').hide();
            $('#submit-wait').show();
            $.ajax({
                url: callback_url,
                type: 'POST',
                cache: false,
                async: false
            });
        }
    });

    $('#thank-you').delay(8500).fadeOut('fast', function() {
        $('#form-content').fadeIn('fast');
    });
});
