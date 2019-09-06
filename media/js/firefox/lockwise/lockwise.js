(function() {
    'use strict';

    var client = window.Mozilla.Client;
    var version = client._getFirefoxMajorVersion();

    if (client.isMobile) {
        document.querySelector('.for-firefox-70-and-above').remove();
        document.querySelector('.for-firefox-69-and-below').remove();
        document.querySelector('.for-non-firefox-users').remove();
    }
    else if ( !client.isFirefox ){
        document.querySelector('.for-firefox-69-and-below').remove();
        document.querySelector('.for-firefox-70-and-above').remove();
        document.querySelector('.for-non-firefox-users').classList.remove('hidden');
    }
    else if ( client.isFirefox === true && version < '70' ) {
        document.querySelector('.for-firefox-70-and-above').remove();
        document.querySelector('.for-non-firefox-users').remove();
        document.querySelector('.for-firefox-69-and-below').classList.remove('hidden');
    }
    else if ( client.isFirefox === true && version >= '70' ) {
        document.querySelector('.for-firefox-69-and-below').remove();
        document.querySelector('.for-non-firefox-users').remove();
        document.querySelector('.for-firefox-70-and-above').classList.remove('hidden');
        document.querySelector('#lockwise-button').addEventListener('click', function() {
            Mozilla.UITour.showHighlight('logins');
        });
    }
})();