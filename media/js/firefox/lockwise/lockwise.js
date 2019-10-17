(function() {
    'use strict';

    var client = window.Mozilla.Client;
    var version = client._getFirefoxMajorVersion();

    var firefox70 = document.querySelector('.for-firefox-70-and-above');
    var firefox69 = document.querySelector('.for-firefox-69-and-below');
    var nonFirefox = document.querySelector('.for-non-firefox-users');

    if (client.isMobile) {
        firefox70.parentNode.removeChild(firefox70);
        firefox69.parentNode.removeChild(firefox69);
        nonFirefox.parentNode.removeChild(nonFirefox);
    }
    else if (!client.isFirefox) {
        firefox69.parentNode.removeChild(firefox69);
        firefox70.parentNode.removeChild(firefox70);
        nonFirefox.classList.remove('hidden');
    }
    else if (client.isFirefox && version < '70') {
        firefox70.parentNode.removeChild(firefox70);
        nonFirefox.parentNode.removeChild(nonFirefox);
        firefox69.classList.remove('hidden');
    }
    else if (client.isFirefox && version >= '70') {
        firefox69.parentNode.removeChild(firefox69);
        nonFirefox.parentNode.removeChild(nonFirefox);
        firefox70.classList.remove('hidden');

        document.querySelector('#lockwise-button').addEventListener('click', function() {
            Mozilla.UITour.showHighlight('logins');
        });
    }
})();
