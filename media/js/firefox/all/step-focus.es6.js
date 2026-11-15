/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Each step is a full page load, which sends screen reader and keyboard users
// back to the top. Move focus to the step they need to complete next instead.
const StepFocus = {};

StepFocus.isStepNavigation = (referrer, origin) => {
    if (!referrer) {
        return false;
    }

    try {
        const url = new URL(referrer);
        return (
            url.origin === origin &&
            url.pathname.indexOf('/firefox/all/') !== -1
        );
    } catch (e) {
        return false;
    }
};

// The referrer survives a reload or back/forward, where the browser already
// puts the visitor back where they were, so only act on a new navigation.
StepFocus.isNewNavigation = () => {
    try {
        const entry = window.performance.getEntriesByType('navigation')[0];
        return !entry || entry.type === 'navigate';
    } catch (e) {
        return true;
    }
};

StepFocus.getCurrentStep = () => {
    const steps = document.querySelectorAll(
        '.c-steps .c-step-name:not(.t-step-disabled)'
    );
    return steps.length ? steps[steps.length - 1] : null;
};

StepFocus.focusCurrentStep = () => {
    const step = StepFocus.getCurrentStep();

    if (!step) {
        return false;
    }

    const rect = step.getBoundingClientRect();

    if (rect.top < 0 || rect.bottom > window.innerHeight) {
        step.scrollIntoView();
    }

    step.focus({ preventScroll: true });
    return document.activeElement === step;
};

StepFocus.init = () => {
    if (
        StepFocus.isNewNavigation() &&
        StepFocus.isStepNavigation(document.referrer, window.location.origin)
    ) {
        StepFocus.focusCurrentStep();
    }
};

export default StepFocus;
