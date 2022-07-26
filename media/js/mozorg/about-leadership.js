/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function () {
    'use strict';

    var bios = document.getElementsByClassName('has-bio');
    var content = document.querySelector('.mzp-u-modal-content');

    for (var i = 0; i < bios.length; i++) {
        var bio = bios[i];
        bio.setAttribute('aria-role', 'button');

        bio.addEventListener('click', function (e) {
            e.preventDefault();
            var modalContent = this.cloneNode(true);
            modalContent.removeAttribute('id');
            modalContent.setAttribute('aria-role', 'article');

            Mzp.Modal.createModal(e.target, content, {
                closeText: window.Mozilla.Utils.trans('global-close'),
                onCreate: function () {
                    content.appendChild(modalContent);
                },
                onDestroy: function () {
                    modalContent.parentNode.removeChild(modalContent);
                }
            });
        });
    }

    function getHash() {
        var hash = window.location.hash;
        if (hash.indexOf('#') > -1) {
            hash = hash.split('#')[1];
        }

        return hash;
    }

    // trigger modal on page load if hash is present and matches a person with a bio
    if (window.location.hash) {
        var hash = getHash();
        var target = document.getElementById(hash);

        if (target && target.classList.contains('has-bio')) {
            target.click();
        }
    }
})(window.Mozilla);
