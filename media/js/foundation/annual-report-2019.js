/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    // Lazyload images
    Mozilla.LazyLoad.init();

    var modalContainers = document.getElementsByClassName('has-modal');
    var content = document.querySelector('.mzp-u-modal-content');

    var modalNextButtonFragment =
        '<div class="c-modal-next">' +
        '    <button type="button" class="c-modal-button-next" title="Next">' +
        '        Next' +
        '    </button>' +
        '</div>';

    var modalPrevButtonFragment =
        '<div class="c-modal-prev">' +
        '    <button type="button" class="c-modal-button-prev" title="Previous">' +
        '        Previous' +
        '    </button>' +
        '</div>';

    var articleArray = document.querySelectorAll('[data-modal-id]');

    // Set to true when a listener it set, as to not set it multiple times.
    // Resets when the modal is closed.
    var kbInit = null;

    function keyboardListenerInit() {

        if (kbInit) {
            return;
            // Turn Off
        }

        document.addEventListener('keyup', keyboardNextPrev, false);


        kbInit = true;
    }

    function keyboardNextPrev(event) {
        if (!kbInit) {
            return;
        }

        switch (event.keyCode) {
        case 37: // Left arrow
            prevModalArticle();
            break;
        case 38: // Up arrow
            prevModalArticle();
            break;
        case 39: // Right arrow
            nextModalArticle();
            break;
        case 40: // Down arrow
            nextModalArticle();
            break;
        }

    }

    function modalInit() {
        // Lazy load images in the modal
        var modalImage = document.querySelector('.mzp-c-modal-overlay-contents .mzp-c-card-image');

        if (modalImage) {
            var srcset = modalImage.getAttribute('data-srcset');

            if (srcset) {
                modalImage.srcset = srcset;
            }

            modalImage.src = modalImage.getAttribute('data-src');
            modalImage.removeAttribute('data-src');
            modalImage.removeAttribute('data-srcset');
        }

        var modalNextButton = document.querySelector('.c-modal-next');
        var modalPrevButton = document.querySelector('.c-modal-prev');

        modalNextButton.removeEventListener('click', nextModalArticle, false);
        modalPrevButton.removeEventListener('click', prevModalArticle, false);

        modalNextButton.addEventListener('click', nextModalArticle, false);
        modalPrevButton.addEventListener('click', prevModalArticle, false);

        keyboardListenerInit();

    }

    function getCurrentModalIndex(){
        var modalContent = document.querySelector('.mzp-u-modal-content.mzp-c-modal-overlay-contents');
        var newArticleIndex = parseInt(modalContent.dataset.currentIndex, 10);
        return newArticleIndex;
    }

    function updateModalArticle(index) {
        var modalContent = document.querySelector('.mzp-u-modal-content.mzp-c-modal-overlay-contents');
        var newArticleId = newArticleId = articleArray[index].dataset.modalId;
        var newModalContent = document.querySelector('[data-modal-parent="' + newArticleId + '"]').cloneNode(true);
        var currentModalContent = modalContent.firstElementChild;

        modalContent.replaceChild(newModalContent, currentModalContent);
        modalContent.dataset.currentIndex = index;

        modalInit();
    }

    function nextModalArticle() {
        var newArticleIndex = getCurrentModalIndex();
        newArticleIndex++;

        // If at the end of the gallery, start over
        if (newArticleIndex === (articleArray.length)) {
            newArticleIndex = 0;
        }

        updateModalArticle(newArticleIndex);
    }

    function prevModalArticle() {
        var newArticleIndex = getCurrentModalIndex();
        newArticleIndex--;

        // If at the beginning of the gallery, start over
        if (newArticleIndex < 0) {
            newArticleIndex = articleArray.length - 1;
        }

        updateModalArticle(newArticleIndex);
    }

    for (var i = 0; i < modalContainers.length; i++) {
        var modalContainer = modalContainers[i];
        modalContainer.setAttribute('aria-role', 'button');

        modalContainer.dataset.currentIndex = i;

        modalContainer.addEventListener('click', function(e) {
            e.preventDefault();

            var modalId = this.dataset.modalId;
            var currentIndex = parseInt(this.dataset.currentIndex, 10);
            var modalContent = document.querySelector('[data-modal-parent="' + modalId + '"]').cloneNode(true);
            window.location.hash = modalId;

            modalContent.removeAttribute('id');
            modalContent.setAttribute('aria-role', 'article');

            Mzp.Modal.createModal(this, content, {
                allowScroll: false,
                closeText: window.Mozilla.Utils.trans('global-close'),
                onCreate: function() {
                    content.appendChild(modalContent);

                    content.dataset.currentIndex = currentIndex;

                    var modalCloseButton = document.querySelector('.mzp-c-modal-close');
                    modalCloseButton.insertAdjacentHTML('beforebegin', modalNextButtonFragment);
                    modalCloseButton.insertAdjacentHTML('beforebegin', modalPrevButtonFragment);

                    // Lazy load images in the modal and set next/prev listeners
                    modalInit();

                },
                onDestroy: function() {
                    if (window.history) {
                        window.history.replaceState('', '', window.location.pathname);
                    }

                    kbInit = false;

                    // Recache the current modal content which may have changed via next/prev buttons
                    var modalParent = document.querySelector('.mzp-u-modal-content.mzp-c-modal-overlay-contents');
                    var currentModalContent = modalParent.firstElementChild;

                    modalParent.removeChild(currentModalContent);
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
