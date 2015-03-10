/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    var $main = $('main');
    var $container = $('.tab-panel');

    $('.toggle > ul > li > a').on('click', function (e) {
        e.preventDefault();
        var href = e.target.href;

        // set the min height of the container should the newsletter
        // have been expanded to avoid content jump.
        $container.css('min-height', $container.height());

        if (href.indexOf('send-sms') !== -1) {
            $main.attr('data-active', 'sms');
        } else if (href.indexOf('send-email') !== -1) {
            $main.attr('data-active', 'email');
        }
    });
})(window.jQuery);
