/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
 
// eslint-disable-next-line 
function goBack(){
    'use strict';
    window.history.back();
}

(function conditionallyHideBackButton(){ // Hides back button if there is no previous page to go back to.
    'use strict';
    if (window.history.length > 1) {
        var div = document.getElementById('go-back');
        div.classList.remove('hide-back');
    }
}());