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

emblaNodes.forEach((node) => {
    const viewport = node.querySelector('.carousel-viewport');
    const emblaApi = EmblaCarousel(viewport, options);

    const prevButton = node.querySelector('.carousel-prev');
    const nextButton = node.querySelector('.carousel-next');

    if (prevButton && nextButton) {
        prevButton.addEventListener('click', emblaApi.scrollPrev, false);
        nextButton.addEventListener('click', emblaApi.scrollNext, false);
    }

    const carouselDots = node.querySelector('.carousel-dots');

    if (carouselDots) {
        addDotBtnsAndClickHandlers(emblaApi, carouselDots);
    }
});
