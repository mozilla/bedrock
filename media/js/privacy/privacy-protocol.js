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
})();
