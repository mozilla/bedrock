/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const modalContainers = document.getElementsByClassName('has-modal');
const content = document.querySelector('.mzp-u-modal-content');
const articleArray = document.querySelectorAll('[data-modal-id]');

const modalNextButtonFragment = `<div class="c-modal-next">
        <button type="button" class="c-modal-button-next" title="Next">
            Next
        </button>
    </div>`;

const modalPrevButtonFragment = `<div class="c-modal-prev">
        <button type="button" class="c-modal-button-prev" title="Previous">
            Previous
        </button>
    </div>`;

// Set to true when a listener it set, as to not set it multiple times.
// Resets when the modal is closed.
let kbInit = null;

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
    const modalNextButton = document.querySelector('.c-modal-next');
    const modalPrevButton = document.querySelector('.c-modal-prev');

    modalNextButton.removeEventListener('click', nextModalArticle, false);
    modalPrevButton.removeEventListener('click', prevModalArticle, false);

    modalNextButton.addEventListener('click', nextModalArticle, false);
    modalPrevButton.addEventListener('click', prevModalArticle, false);

    keyboardListenerInit();
}

function getCurrentModalIndex() {
    const modalContent = document.querySelector(
        '.mzp-u-modal-content.mzp-c-modal-overlay-contents'
    );
    const newArticleIndex = parseInt(
        modalContent.getAttribute('data-current-index'),
        10
    );
    return newArticleIndex;
}

function updateModalArticle(index) {
    const modalContent = document.querySelector(
        '.mzp-u-modal-content.mzp-c-modal-overlay-contents'
    );
    const newArticleId = articleArray[index].getAttribute('data-modal-id');
    const newModalContent = document
        .querySelector(`[data-modal-parent="${newArticleId}"]`)
        .cloneNode(true);
    const currentModalContent = modalContent.firstElementChild;

    window.location.hash = newArticleId;

    modalContent.replaceChild(newModalContent, currentModalContent);
    modalContent.setAttribute('data-current-index', index);

    modalInit();
}

function nextModalArticle() {
    let newArticleIndex = getCurrentModalIndex();
    newArticleIndex++;

    // If at the end of the gallery, start over
    if (newArticleIndex === articleArray.length) {
        newArticleIndex = 0;
    }

    updateModalArticle(newArticleIndex);
}

function prevModalArticle() {
    let newArticleIndex = getCurrentModalIndex();
    newArticleIndex--;

    // If at the beginning of the gallery, start over
    if (newArticleIndex < 0) {
        newArticleIndex = articleArray.length - 1;
    }

    updateModalArticle(newArticleIndex);
}

for (let i = 0; i < modalContainers.length; i++) {
    const modalContainer = modalContainers[i];

    modalContainer.setAttribute('aria-role', 'button');
    modalContainer.setAttribute('data-current-index', i);

    modalContainer.addEventListener('click', function (e) {
        e.preventDefault();

        const modalId = this.getAttribute('data-modal-id');
        const currentIndex = parseInt(
            this.getAttribute('data-current-index'),
            10
        );
        const modalContent = document
            .querySelector(`[data-modal-parent="${modalId}"]`)
            .cloneNode(true);
        window.location.hash = modalId;

        modalContent.removeAttribute('id');
        modalContent.setAttribute('aria-role', 'article');

        window.Mzp.Modal.createModal(this, content, {
            allowScroll: false,
            closeText: window.Mozilla.Utils.trans('global-close'),
            onCreate: () => {
                content.appendChild(modalContent);

                content.setAttribute('data-current-index', currentIndex);

                const modalCloseButton =
                    document.querySelector('.mzp-c-modal-close');
                modalCloseButton.insertAdjacentHTML(
                    'beforebegin',
                    modalPrevButtonFragment
                );
                modalCloseButton.insertAdjacentHTML(
                    'beforebegin',
                    modalNextButtonFragment
                );

                // set next/prev listeners
                modalInit();
            },
            onDestroy: () => {
                if (window.history) {
                    window.history.replaceState(
                        '',
                        '',
                        window.location.pathname
                    );
                }

                kbInit = false;

                // Recache the current modal content which may have changed via next/prev buttons
                const modalParent = document.querySelector(
                    '.mzp-u-modal-content.mzp-c-modal-overlay-contents'
                );
                const currentModalContent = modalParent.firstElementChild;

                /**
                 * Ensure focus is returned to opening CTA on modal close.
                 * We have to do some manual DOM walking here as some clickable
                 * parent elements do not normally receive focus programatically.
                 * Issue: https://github.com/mozilla/bedrock/issues/12346
                 */
                const parentId =
                    currentModalContent.getAttribute('data-modal-parent');

                // Try and get the modal parent ID/ element.
                if (parentId) {
                    const parentElement = document.querySelector(
                        `[data-modal-id="${parentId}"]`
                    );

                    // If the modal element contains a link or button,
                    // set focus to the first child instance.
                    const parentCta = parentElement.querySelector('a, button');

                    if (parentCta) {
                        parentCta.focus();
                    }
                }

                modalParent.removeChild(currentModalContent);
            }
        });
    });
}

// trigger modal on page load if hash is present and matches a person with a bio
if (window.location.hash) {
    const target = document.getElementById(window.location.hash.substr(1));

    if (target) {
        // Query by data attribute in the event that not every element may have an ID.
        // Issue https://github.com/mozilla/bedrock/issues/12346
        const link = document.querySelector(`[data-modal-id="${target.id}"]`);

        if (link && link.classList.contains('has-modal')) {
            link.click();
        }
    }
}
