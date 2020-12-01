/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    var modalContainers = document.getElementsByClassName('has-modal');
    var content = document.querySelector('.mzp-u-modal-content');

    for (var i = 0; i < modalContainers.length; i++) {
        var modalContainer = modalContainers[i];
        modalContainer.setAttribute('aria-role', 'button');

        modalContainer.addEventListener('click', function(e) {
            e.preventDefault();

            var modalId = this.dataset.modalId;
            var modalContent = document.querySelector('[data-modal-parent="' + modalId + '"]').cloneNode(true);
            window.location.hash = modalId;

            modalContent.removeAttribute('id');
            modalContent.setAttribute('aria-role', 'article');

            Mzp.Modal.createModal(e.target, content, {
                closeText: window.Mozilla.Utils.trans('global-close'),
                onCreate: function() {
                    content.appendChild(modalContent);
                },
                onDestroy: function() {
                    if (window.history) {
                        window.history.replaceState('', '', window.location.pathname);
                    }
                    // window.location.href = window.location.href.replace(/#.*$/, '#');

                    modalContent.parentNode.removeChild(modalContent);
                }
            });
        });
    }

    // trigger modal on page load if hash is present and matches a person with a bio
    if (window.location.hash) {
        var target = document.getElementById(window.location.hash.substr(1));

        if (target && target.classList.contains('has-modal')) {
            target.click();
        }
    }

})(window.Mozilla);
