/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


(function() {
    'use strict';

    var openText = document.getElementById('strings').getAttribute('data-details-open-text');
    var closeText = document.getElementById('strings').getAttribute('data-details-close-text');
    var buttons;

    window.Mzp.Details.init('.format-headings .privacy-body section section > h3');
    window.Mzp.Details.init('.format-paragraphs .summary');

    buttons = document.querySelectorAll('.is-summary button');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].setAttribute('data-open', openText);
        buttons[i].setAttribute('data-close', closeText);
    }
    
    var cookieButton = document.querySelector('#user-choices button');
    var cookieText = document.getElementById('expand-formatparagraphssummary-2');
    
    if (window.location.hash === '#cookies') {
        if (cookieButton && cookieText) {
            cookieButton.setAttribute('aria-expanded', 'true');
            cookieText.classList.remove('is-closed');
            cookieText.setAttribute('aria-hidden', 'false');
        }
    }
})();
