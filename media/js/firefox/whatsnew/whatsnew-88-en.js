/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var jingle = function(){
        button.style.fontStyle = 'italic';
        console.log('jingle');
        var audio = new Audio(button.dataset.audio);
        audio.play();
    };

    var button = document.getElementById('outatime');

    button.addEventListener('click', jingle);

})(window.Mozilla);
