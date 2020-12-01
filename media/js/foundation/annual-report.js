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

    var modalNextButtonFragment =
        '<div class="c-modal-next">' +
        '    <button type="button" class="c-modal-button-next" title="Next">' +
        '        Next' +
        '    </button>' +
        '</div>';

    var articleArray = document.querySelectorAll('[data-modal-id]');

    function showNextArticle(closeBtn, currentArticleId) {
        closeBtn.firstElementChild.click();

        var currentArticle = document.querySelector('[data-modal-id="' + currentArticleId + '"]');
        var nextArticleId = articleArray[currentArticle.dataset.currentIndex++].dataset.modalId;
        var nextArticle = document.querySelector('[data-modal-id="' + nextArticleId + '"]');

        nextArticle.click();
    }

    for (var i = 0; i < modalContainers.length; i++) {
        var modalContainer = modalContainers[i];
        modalContainer.setAttribute('aria-role', 'button');

        modalContainer.dataset.currentIndex = i;

        modalContainer.addEventListener('click', function(e) {
            e.preventDefault();

            var modalId = this.dataset.modalId;
            var modalContent = document.querySelector('[data-modal-parent="' + modalId + '"]').cloneNode(true);
            window.location.hash = modalId;

            modalContent.removeAttribute('id');
            modalContent.setAttribute('aria-role', 'article');

            Mzp.Modal.createModal(e.target, content, {
                allowScroll: false,
                closeText: window.Mozilla.Utils.trans('global-close'),
                onCreate: function() {
                    content.appendChild(modalContent);

                    var modalCloseButton = document.querySelector('.mzp-c-modal-close');
                    modalCloseButton.insertAdjacentHTML('beforebegin', modalNextButtonFragment);

                    var modalNextButton = document.querySelector('.c-modal-next');

                    modalNextButton.addEventListener('click', function(){
                        showNextArticle(modalCloseButton, modalId);
                    });
                },
                onDestroy: function() {
                    console.log('onDestroy');
                    if (window.history) {
                        window.history.replaceState('', '', window.location.pathname);
                    }
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
