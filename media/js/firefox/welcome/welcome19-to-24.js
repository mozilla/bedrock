/* eslint-disable no-console */

(function () {
    'use strict';

    const firefoxReleaseCTA = document.getElementById('update-firefox');
    const firefoxEsrCTA = document.getElementById('update-firefox-esr');

    Mozilla.UITour.getConfiguration('appinfo', function (details) {
        if (details.defaultUpdateChannel === 'esr') {
            firefoxEsrCTA.style.display = 'block';
            firefoxReleaseCTA.style.display = 'none';
        }
    });
})();
