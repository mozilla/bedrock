/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // var $modalWrapper = $('.email-privacy');
    // var $modalLink = $('.email-privacy-link');

    // $modalLink.on('click', function(e) {
    //     e.preventDefault();
    //     Mozilla.Modal.createModal(this, $modalWrapper, {
    //         title: $(this).text()
    //     });

    //     window.dataLayer.push({
    //         'event': 'in-page-interaction',
    //         'eAction': 'link click',
    //         'eLabel': 'How will Mozilla use my email?'
    //     });
    // });

    var content = document.querySelector('.mzp-u-modal-content');
    var trigger = document.querySelector('.email-privacy-link');
    var title = document.querySelector('.email-privacy h3');
    var strings = document.getElementById('strings');

    trigger.addEventListener('click', function(e) {
        e.preventDefault();
        Mozilla.Modal.createModal(e.target, content, {
            title: title.innerHTML,
            className: 'mzp-t-firefox',
            closeText: strings.dataset.close
        });

        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'link click',
            'eLabel': 'How will Mozilla use my email?'
        });
    }, false);

})();
