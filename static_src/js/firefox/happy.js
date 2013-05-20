/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {
var isFirefox = (/\sFirefox/.test(window.navigator.userAgent));
var moving = true;

function grow()
{
    moving = true;
    $('#old-fx img').animate({'margin-left': '100px'}, 2000);
    $('#new-fx img').animate(
        {'margin-left': '430px'},
        2000,
        'swing',
        function() { moving = false; }
    );
}

function reset()
{
    $('#bars img').css('margin-left', 0);
}

if (isFirefox) {

    grow();

    $('#fx').click(function(){
        if (!moving) {
            reset();
            grow();
        }
    });

} else {

    $('#fx').hide();

    var $nonfx       = $('#non-fx');
    var $detected    = $('#detected');
    var $notdetected = $('#notdetected');

    var isSafari = /Safari/.test(window.navigator.userAgent);
    var isChrome = /Chrome/.test(window.navigator.userAgent);
    var isIE     = /MSIE/.test(window.navigator.userAgent);

    if (isChrome) {
        $detected.text(
            $detected.text().replace(/%BROWSER%/, 'Google Chrome')
        );
        $notdetected.hide();
    } else if (isSafari) {
        $detected.text(
            $detected.text().replace(/%BROWSER%/, 'Safari')
        );
        $notdetected.hide();
    } else if (isIE) {
        $detected.text(
            $detected.text().replace(/%BROWSER%/, 'Internet Explorer')
        );
        $notdetected.hide();
    } else {
        $detected.hide();
    }

    $nonfx.show();
}

});
