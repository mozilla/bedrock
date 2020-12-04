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

    function showArticle(dir, closeBtn, currentIndex) {

        closeBtn.firstElementChild.click();

        var newArticleIndex = currentIndex;

        if (dir === 'next') {
            newArticleIndex++;
        } else {
            newArticleIndex--;
        }

        var newArticleId = newArticleId = articleArray[newArticleIndex].dataset.modalId;
        var newArticle = document.querySelector('[data-modal-id="' + newArticleId + '"]');

        newArticle.click();
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

                    // Lazy load images in the modal
                    var modalImage = document.querySelector('.mzp-c-modal-overlay-contents .mzp-c-card-image');
                    var srcset = modalImage.getAttribute('data-srcset');

                    if (srcset) {
                        modalImage.srcset = srcset;
                    }

                    modalImage.src = modalImage.getAttribute('data-src');
                    modalImage.removeAttribute('data-src');
                    modalImage.removeAttribute('data-srcset');

                    var modalCloseButton = document.querySelector('.mzp-c-modal-close');
                    modalCloseButton.insertAdjacentHTML('beforebegin', modalNextButtonFragment);
                    modalCloseButton.insertAdjacentHTML('beforebegin', modalPrevButtonFragment);

                    var modalNextButton = document.querySelector('.c-modal-next');
                    var modalPrevButton = document.querySelector('.c-modal-prev');

                    if (currentIndex < 1) {
                        content.parentNode.classList.add('hide-prev');
                    } else if (currentIndex === (articleArray.length - 1)) {
                        content.parentNode.classList.add('hide-next');
                    }
                    else {
                        content.parentNode.classList.remove('hide-prev', 'hide-next');
                    }

                    modalNextButton.addEventListener('click', function(){
                        showArticle('next', modalCloseButton, currentIndex);
                    });
                    modalPrevButton.addEventListener('click', function(){
                        showArticle('prev', modalCloseButton, currentIndex);
                    });
                },
                onDestroy: function() {
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
