(function(Mozilla) {
    'use strict';

    var stateStorageKey = 'fxaOauthState';
    var verifiedStorageKey = 'fxaOauthVerified';
    var cookieDays = 1;

    var className;
    var state;


    function initOauth() {
        var fxaFormWrapper = document.getElementById('fxa-form-wrapper');
        var metricsFlowEndpoint = fxaFormWrapper.getAttribute('data-fxa-metrics-endpoint');
        var flowIdField = document.getElementById('flow_id');
        var flowBeginTimeField = document.getElementById('flow_begin_time');
        var stateField = document.getElementById('state');
        var submit = document.getElementById('submit');
        var fxaSignIn = document.getElementById('fxa-sign-in');

        if (Mozilla.Cookies.hasItem(stateStorageKey)) {
            state = Mozilla.Cookies.getItem(stateStorageKey);
        } else {
            // generate a state token and put it in sessionStorage
            state = Math.random() + '_concert_q42018';

            var d = new Date();
            d.setTime(d.getTime() + (cookieDays * 24 * 60 * 60 * 1000));
            Mozilla.Cookies.setItem(stateStorageKey, state, d.toUTCString(), '/');
        }

        // put state value in form & append to sign-in link
        stateField.value = state;
        fxaSignIn.href += '&state=' + state;

        // get flow stuff from FxA
        fetchTokens(metricsFlowEndpoint);

        // get tokens from FxA for analytics purposes
        // copied from base/mozilla-fxa-form.js
        function fetchTokens(destURL) {
            // add required params to the token fetch request
            destURL += '?utm_campaign=concert&utm_source=mozilla.org';

            fetch(destURL).then(function (resp) {
                return resp.json();
            }).then(function (r) {
                flowIdField.value = r.flowId;
                flowBeginTimeField.value = r.flowBeginTime;
            }).catch(function () {
                // silently fail, leaving flow_id and flow_begin_time as default empty value
            }).finally(function () {
                submit.disabled = false;
            });
        }
    }

    // update class based on cookie state
    // (this will use a CSS hook to show/hide the appropriate content)
    if (Mozilla.Cookies.hasItem(verifiedStorageKey)) {
        className = 'verified';
    } else {
        className = 'form';
        initOauth();
    }

    // apply className determined above to show proper content
    document.documentElement.className += ' ' + className;
})(window.Mozilla);
