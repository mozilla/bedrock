(function () {
    'use strict';

    var STATCOUNTER_PROJECT_ID = document.getElementsByTagName('html')[0].getAttribute('data-statcounter-project-id');
    var STATCOUNTER_SECURITY_ID = document.getElementsByTagName('html')[0].getAttribute('data-statcounter-security-id');

    // If doNotTrack is not enabled, it is ok to add StatCounter
    // @see https://bugzilla.mozilla.org/show_bug.cgi?id=1217896 for more details
    if (typeof window._dntEnabled === 'function' && !window._dntEnabled() && STATCOUNTER_PROJECT_ID && STATCOUNTER_SECURITY_ID) {
        // Statcounter needs the following vars scoped globally as lowercase, so disable the eslint errors thrown by camelcase and no-unused-vars
        /* eslint-disable camelcase, no-unused-vars */
        var sc_project = window.sc_project = STATCOUNTER_PROJECT_ID;
        var sc_invisible = window.sc_invisible = 1;
        var sc_security = window.sc_security = STATCOUNTER_SECURITY_ID;
        /* eslint-enable camelcase, no-unused-vars */
        var newScriptTag = document.createElement('script');
        var target = document.getElementsByTagName('script')[0];
        newScriptTag.src = 'https://secure.statcounter.com/counter/counter.js';
        target.parentNode.insertBefore(newScriptTag, target);
    }
})();
