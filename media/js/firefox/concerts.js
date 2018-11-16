(function(Mozilla) {
    'use strict';

    var stateStorageKey = 'fxaOauthState';
    var verifiedStorageKey = 'fxaOauthVerified';
    var cookieDays = 1;

    var className;
    var state;

    /*
        This function initiates the OAuth process.

        It looks for a state key stored in a cookie, and, if not found, generates a new
        key and places it in a cookie.

        The state value is then set in the form and on the direct link URL.

        Next, we retrieve metrics information from an asynchronous FxA call. When this
        call completes, the submit button on the form is enabled.
    */
    function initOauth() {
        var fxaFormWrapper = document.getElementById('fxa-form-wrapper');
        var metricsFlowEndpoint = fxaFormWrapper.getAttribute('data-fxa-metrics-endpoint');
        var flowIdField = document.getElementById('flow_id');
        var flowBeginTimeField = document.getElementById('flow_begin_time');
        var stateField = document.getElementById('state');
        var submit = document.getElementById('submit');
        var fxaSignIn = document.getElementById('fxa-sign-in');

        // check for an existing state value in a cookie
        if (Mozilla.Cookies.hasItem(stateStorageKey)) {
            state = Mozilla.Cookies.getItem(stateStorageKey);
        } else {
            // generate a state token and put it in a cookie

            // the suffix below is superfluous for now, but will help us identify
            // different OAuth flows in the future
            state = Math.random() + '_concert_q42018';

            var d = new Date();
            d.setTime(d.getTime() + (cookieDays * 24 * 60 * 60 * 1000));
            Mozilla.Cookies.setItem(stateStorageKey, state, d.toUTCString(), '/');
        }

        // put state value in form & append to sign-in link
        stateField.value = state;
        fxaSignIn.href += '&state=' + state;

        // get metrics flow stuff from FxA
        fetchTokens(metricsFlowEndpoint);

        // get tokens from FxA for analytics purposes
        // copied from base/mozilla-fxa-form.js
        function fetchTokens(destURL) {
            // add required params to the token fetch request
            destURL += '?utm_campaign=firefox-concert-series-q4-2018&utm_source=mozilla.org';

            fetch(destURL).then(function(resp) {
                return resp.json();
            }).then(function(r) {
                flowIdField.value = r.flowId;
                flowBeginTimeField.value = r.flowBeginTime;
            }).catch(function() {
                // silently fail, leaving flow_id and flow_begin_time as default empty value
            }).finally(function() {
                submit.disabled = false;
            });
        }
    }

    // update class based on cookie state so we can show/hide the appropriate content

    // if user has a verified cookie, we can skip the OAuth flow
    if (Mozilla.Cookies.hasItem(verifiedStorageKey)) {
        className = 'verified';
    } else {
        className = 'form';
        initOauth();
    }

    // apply className determined above to show proper content
    document.documentElement.className += ' ' + className;
})(window.Mozilla);
