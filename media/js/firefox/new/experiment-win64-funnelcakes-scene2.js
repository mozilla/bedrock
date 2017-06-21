(function() {
    'use strict';

    // update dl link for windows to point to win64
    // same selector from canonical scene2.js
    var $platformLink = $('#download-button-wrapper-desktop .download-list .os_win .download-link');

    if ($platformLink.length) {
        // the bouncer URL needed for the win64 funnelcake is the same as the
        // win32 funnelcake, but with os=win replaced with os=win64, e.g.
        // https://download.mozilla.org/?product=firefox-stub-f106&os=win64&lang={accepted-lang}
        var newHref = $platformLink.attr('href').replace('os=win&', 'os=win64&');
        $platformLink.attr('href', newHref);
    }
})();
