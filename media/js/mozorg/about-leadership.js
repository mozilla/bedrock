/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

var MzpModal = require('@mozilla-protocol/core/protocol/js/modal');

// temporary a11y patch needs to be pack ported to protocol: https://github.com/mozilla/protocol/issues/999
var MzpSideMenu = require('../base/protocol/sidemenu.es6');

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

        // set aria roles on opening bio link and make focusable.
        bio.setAttribute('role', 'button');
        bio.setAttribute('aria-controls', 'leadership-modal');
        bio.setAttribute('aria-expanded', 'false');
        bio.setAttribute('tabindex', '0');

        bio.addEventListener('click', function (e) {
            e.preventDefault();
            var openingLink = this;
            var modalContent = openingLink.cloneNode(true);

            // remove superfluous attributes from cloned node when in modal.
            modalContent.removeAttribute('id');
            modalContent.removeAttribute('role');
            modalContent.removeAttribute('aria-controls');
            modalContent.removeAttribute('aria-expanded');
            modalContent.removeAttribute('tabindex');

            // set opening button expanded state to true
            openingLink.setAttribute('aria-expanded', 'true');

            MzpModal.createModal(openingLink, content, {
                closeText: window.Mozilla.Utils.trans('global-close'),
                onCreate: function () {
                    content.appendChild(modalContent);
                    modalContent.focus();
                },
                onDestroy: function () {
                    modalContent.parentNode.removeChild(modalContent);
                    openingLink.setAttribute('aria-expanded', 'false');
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
