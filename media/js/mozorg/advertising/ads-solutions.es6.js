/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import EmblaCarousel from 'embla-carousel';

const modalWrappers = document.querySelectorAll('.modal-wrapper');

modalWrappers.forEach((wrapperEl) => {
    const trigger = wrapperEl.querySelector('.modal-trigger');
    const content = wrapperEl.querySelector('.mzp-u-modal-content');

    if (trigger && content) {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            window.MzpModal.createModal(trigger, content);
        });
    }
});

const emblaNodes = document.querySelectorAll('.carousel');
const options = { loop: false };

const addDotBtnsAndClickHandlers = (emblaApi, dotsNode) => {
    let dotNodes = [];

    const addDotBtnsWithClickHandlers = () => {
        dotsNode.innerHTML = emblaApi
            .scrollSnapList()
            .map(() => '<button class="dot" type="button"></button>')
            .join('');

        const scrollTo = (index) => {
            emblaApi.scrollTo(index);
        };

        dotNodes = Array.from(dotsNode.querySelectorAll('.dot'));
        dotNodes.forEach((dotNode, index) => {
            dotNode.addEventListener('click', () => scrollTo(index), false);
        });
    };

    const toggleDotBtnsActive = () => {
        const previous = emblaApi.previousScrollSnap();
        const selected = emblaApi.selectedScrollSnap();
        dotNodes[previous].classList.remove('dot-selected');
        dotNodes[selected].classList.add('dot-selected');
    };

    emblaApi
        .on('init', addDotBtnsWithClickHandlers)
        .on('reInit', addDotBtnsWithClickHandlers)
        .on('init', toggleDotBtnsActive)
        .on('reInit', toggleDotBtnsActive)
        .on('select', toggleDotBtnsActive);

    return () => {
        dotsNode.innerHTML = '';
    };
};

const updateSelectedSnapDisplay = (emblaApi, snapDisplay) => {
    const updateSnapDisplay = (emblaApi) => {
        const selectedSnap = emblaApi.selectedScrollSnap();
        const snapCount = emblaApi.scrollSnapList().length;
        snapDisplay.innerHTML = `${selectedSnap + 1} / ${snapCount}`;
    };

    emblaApi.on('select', updateSnapDisplay).on('reInit', updateSnapDisplay);

    updateSnapDisplay(emblaApi);
};

// Toggle caption visibility based on Embla's selected slide.
const toggleSlideCaptions = (emblaApi, rootNode) => {
    // Note: we query caption elements from the DOM each update; no
    // cached snapCount is required here.

    // Find the nearest ancestor that contains caption elements. Captions
    // are often outside the .carousel element (e.g. sibling modal caption
    // containers). Walk up the DOM until we find an ancestor that
    // contains [data-slide-caption] nodes, or fall back to document.
    let captionRoot = rootNode;
    while (captionRoot && captionRoot !== document.body) {
        if (
            captionRoot.querySelector &&
            captionRoot.querySelector('[data-slide-caption]')
        ) {
            break;
        }
        captionRoot = captionRoot.parentElement;
    }
    if (!captionRoot || captionRoot === document.body) {
        captionRoot = document;
    }

    const update = () => {
        const idx = emblaApi.selectedScrollSnap();
        // Query the live DOM for caption elements and toggle per-element.
        const all = Array.from(
            captionRoot.querySelectorAll('[data-slide-caption]')
        );
        all.forEach((el) => {
            const val = parseInt(el.getAttribute('data-slide-caption'), 10);
            if (Number.isNaN(val)) return;
            if (val - 1 === idx) {
                el.classList.remove('is-hidden');
            } else {
                el.classList.add('is-hidden');
            }
        });
    };

    emblaApi.on('init', update).on('select', update).on('reInit', update);

    // initialize visibility
    update();

    return () => {
        const all = Array.from(
            captionRoot.querySelectorAll('[data-slide-caption]')
        );
        all.forEach((el) => el.classList.remove('is-hidden'));
    };
};

emblaNodes.forEach((node) => {
    const viewport = node.querySelector('.carousel-viewport');
    const emblaApi = EmblaCarousel(viewport, options);

    const prevButton = node.querySelector('.carousel-prev');
    const nextButton = node.querySelector('.carousel-next');

    if (prevButton && nextButton) {
        // Call Embla methods inside wrappers so the click event isn't passed
        // as an argument to the Embla API methods.
        prevButton.addEventListener(
            'click',
            () => emblaApi.scrollPrev(),
            false
        );
        nextButton.addEventListener(
            'click',
            () => emblaApi.scrollNext(),
            false
        );
    }

    const carouselDots = node.querySelector('.carousel-dots');
    const snapDisplay = node.querySelector('.carousel-snap-display');

    if (carouselDots) {
        addDotBtnsAndClickHandlers(emblaApi, carouselDots);
    }

    if (snapDisplay) {
        updateSelectedSnapDisplay(emblaApi, snapDisplay);
    }

    // Wire up caption toggling for this carousel instance
    toggleSlideCaptions(emblaApi, node);
});
