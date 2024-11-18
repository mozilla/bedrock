/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

var MzpModal = require('@mozilla-protocol/core/protocol/js/modal');
var MzpSideMenu = require('@mozilla-protocol/core/protocol/js/sidemenu');

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
        bio.setAttribute('role', 'button');
        bio.setAttribute('tabindex', '0');

        bio.addEventListener('click', function (e) {
            e.preventDefault();
            var modalContent = this.cloneNode(true);
            modalContent.removeAttribute('id');
            modalContent.setAttribute('role', 'article');

            MzpModal.createModal(e.target, content, {
                closeText: window.Mozilla.Utils.trans('global-close'),
                onCreate: function () {
                    content.appendChild(modalContent);
                    modalContent.focus();
                },
                onDestroy: function () {
                    modalContent.parentNode.removeChild(modalContent);
                }
            });
        });

        bio.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (this === document.activeElement) this.click();
            }
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

    MzpSideMenu.init();
})(window.Mozilla);
