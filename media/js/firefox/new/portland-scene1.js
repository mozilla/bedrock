/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    // use custom adjust link for Android/iOS
    // each portland variation has a custom link
    $('.portland').find('.os_android .download-link, .os_ios .download-link').attr('href', 'https://app.adjust.com/4mnnhn?campaign=city_portland_2018&adgroup=website_xv_portland&creative=non-profit');
    $('.portland-fast').find('.os_android .download-link, .os_ios .download-link').attr('href', 'https://app.adjust.com/4mnnhn?campaign=city_portland_2018&adgroup=website_xv_portland&creative=fast');
    $('.portland-safe').find('.os_android .download-link, .os_ios .download-link').attr('href', 'https://app.adjust.com/4mnnhn?campaign=city_portland_2018&adgroup=website_xv_portland&creative=private');

    $('.portland.forgood').find('.os_android .download-link, .os_ios .download-link').attr('href', 'https://app.adjust.com/4mnnhn?campaign=national&adgroup=landingpage&creative=xv_forgood');
    $('.portland-fast.fast').find('.os_android .download-link, .os_ios .download-link').attr('href', 'https://app.adjust.com/4mnnhn?campaign=national&adgroup=landingpage&creative=xv_fast');
    $('.portland-safe.safe').find('.os_android .download-link, .os_ios .download-link').attr('href', 'https://app.adjust.com/4mnnhn?campaign=national&adgroup=landingpage&creative=xv_safe');
})(window.jQuery);
