/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    function syncAnimation () {
        var $syncAnim = $('.sync-anim');
        var $laptop = $syncAnim.find('.laptop');
        var $laptopScreen = $laptop.find('.inner');
        var $phone = $syncAnim.find('.phone');
        var $arrows = $laptop.find('.arrows');

        $syncAnim.addClass('on');

        $arrows.one('webkitAnimationStart MSAnimationStart animationstart', function () {
            $laptopScreen.addClass('faded');
        });

        $arrows.one('webkitAnimationEnd MSAnimationEnd animationend', function () {
            $laptopScreen.removeClass('faded');
        });

        $phone.one('webkitAnimationEnd MSAnimationEnd animationend', '.passwords', function () {
            $syncAnim.addClass('complete');
        });
    }

    setTimeout(syncAnimation, 1000);

})(window.jQuery);
