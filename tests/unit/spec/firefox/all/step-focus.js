/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import StepFocus from '../../../../../media/js/firefox/all/step-focus.es6';

describe('step-focus.es6.js', function () {
    const origin = 'https://www.mozilla.org';

    describe('isStepNavigation()', function () {
        it('should be true when coming from another step on the same site', function () {
            expect(
                StepFocus.isStepNavigation(
                    `${origin}/en-US/firefox/all/desktop-release/`,
                    origin
                )
            ).toBeTrue();
            expect(
                StepFocus.isStepNavigation(
                    `${origin}/de/firefox/all/desktop-release/win64/`,
                    origin
                )
            ).toBeTrue();
        });

        it('should be false without a referrer', function () {
            expect(StepFocus.isStepNavigation('', origin)).toBeFalse();
        });

        it('should be false when coming from another page on the same site', function () {
            expect(
                StepFocus.isStepNavigation(`${origin}/en-US/firefox/`, origin)
            ).toBeFalse();
        });

        it('should be false when coming from another site', function () {
            expect(
                StepFocus.isStepNavigation(
                    'https://www.firefox.com/en-US/firefox/all/desktop-release/',
                    origin
                )
            ).toBeFalse();
        });

        it('should be false when the referrer is not a valid URL', function () {
            expect(StepFocus.isStepNavigation('not a url', origin)).toBeFalse();
        });
    });

    describe('focusCurrentStep()', function () {
        let steps;

        function render(disabledSteps) {
            const headings = [1, 2, 3, 4]
                .map((n) => {
                    const disabled = n > 4 - disabledSteps;
                    const className = disabled
                        ? 'c-step-name t-step-disabled'
                        : 'c-step-name';
                    return `<h2 tabindex="-1" class="${className}" id="step-${n}">Step ${n}</h2>`;
                })
                .join('');

            steps = document.createElement('div');
            steps.className = 'c-steps';
            steps.innerHTML = headings;
            document.body.appendChild(steps);
        }

        function inView(heading) {
            spyOn(heading, 'getBoundingClientRect').and.returnValue({
                top: 10,
                bottom: 40
            });
        }

        afterEach(function () {
            steps.parentNode.removeChild(steps);
        });

        it('should focus the last step that is not disabled', function () {
            render(2);
            const heading = document.getElementById('step-2');
            inView(heading);

            expect(StepFocus.focusCurrentStep()).toBeTrue();
            expect(document.activeElement).toBe(heading);
        });

        it('should focus the download step once every choice is made', function () {
            render(0);
            const heading = document.getElementById('step-4');
            inView(heading);

            expect(StepFocus.focusCurrentStep()).toBeTrue();
            expect(document.activeElement).toBe(heading);
        });

        it('should not scroll when the step is already in view', function () {
            render(1);
            const heading = document.getElementById('step-3');
            inView(heading);
            spyOn(heading, 'scrollIntoView');

            StepFocus.focusCurrentStep();
            expect(heading.scrollIntoView).not.toHaveBeenCalled();
        });

        it('should scroll a step below the fold into view', function () {
            render(1);
            const heading = document.getElementById('step-3');
            spyOn(heading, 'getBoundingClientRect').and.returnValue({
                top: window.innerHeight + 100,
                bottom: window.innerHeight + 130
            });
            spyOn(heading, 'scrollIntoView');

            StepFocus.focusCurrentStep();
            expect(heading.scrollIntoView).toHaveBeenCalled();
            expect(document.activeElement).toBe(heading);
        });

        it('should scroll a step cut off by the bottom edge into view', function () {
            render(1);
            const heading = document.getElementById('step-3');
            spyOn(heading, 'getBoundingClientRect').and.returnValue({
                top: window.innerHeight - 10,
                bottom: window.innerHeight + 20
            });
            spyOn(heading, 'scrollIntoView');

            StepFocus.focusCurrentStep();
            expect(heading.scrollIntoView).toHaveBeenCalled();
        });

        it('should scroll a step above the viewport into view', function () {
            render(1);
            const heading = document.getElementById('step-3');
            spyOn(heading, 'getBoundingClientRect').and.returnValue({
                top: -50,
                bottom: -20
            });
            spyOn(heading, 'scrollIntoView');

            StepFocus.focusCurrentStep();
            expect(heading.scrollIntoView).toHaveBeenCalled();
        });

        it('should do nothing when there are no steps', function () {
            steps = document.createElement('div');
            document.body.appendChild(steps);
            const before = document.activeElement;

            expect(StepFocus.focusCurrentStep()).toBeFalse();
            expect(document.activeElement).toBe(before);
        });
    });

    describe('isNewNavigation()', function () {
        it('should be true when the page was reached by following a link', function () {
            spyOn(window.performance, 'getEntriesByType').and.returnValue([
                { type: 'navigate' }
            ]);
            expect(StepFocus.isNewNavigation()).toBeTrue();
        });

        it('should be false on a reload', function () {
            spyOn(window.performance, 'getEntriesByType').and.returnValue([
                { type: 'reload' }
            ]);
            expect(StepFocus.isNewNavigation()).toBeFalse();
        });

        it('should be false on back/forward navigation', function () {
            spyOn(window.performance, 'getEntriesByType').and.returnValue([
                { type: 'back_forward' }
            ]);
            expect(StepFocus.isNewNavigation()).toBeFalse();
        });

        it('should be true when the browser has no navigation entry', function () {
            spyOn(window.performance, 'getEntriesByType').and.returnValue([]);
            expect(StepFocus.isNewNavigation()).toBeTrue();
        });

        it('should be true when the navigation timing API throws', function () {
            spyOn(window.performance, 'getEntriesByType').and.throwError(
                'unsupported'
            );
            expect(StepFocus.isNewNavigation()).toBeTrue();
        });
    });

    describe('init()', function () {
        it('should leave focus alone on a direct visit', function () {
            spyOn(StepFocus, 'isNewNavigation').and.returnValue(true);
            spyOn(StepFocus, 'isStepNavigation').and.returnValue(false);
            spyOn(StepFocus, 'focusCurrentStep');

            StepFocus.init();
            expect(StepFocus.focusCurrentStep).not.toHaveBeenCalled();
        });

        it('should leave focus alone on a reload or back/forward', function () {
            spyOn(StepFocus, 'isNewNavigation').and.returnValue(false);
            spyOn(StepFocus, 'isStepNavigation').and.returnValue(true);
            spyOn(StepFocus, 'focusCurrentStep');

            StepFocus.init();
            expect(StepFocus.focusCurrentStep).not.toHaveBeenCalled();
        });

        it('should focus the current step when coming from another step', function () {
            spyOn(StepFocus, 'isNewNavigation').and.returnValue(true);
            spyOn(StepFocus, 'isStepNavigation').and.returnValue(true);
            spyOn(StepFocus, 'focusCurrentStep');

            StepFocus.init();
            expect(StepFocus.isStepNavigation).toHaveBeenCalledWith(
                document.referrer,
                window.location.origin
            );
            expect(StepFocus.focusCurrentStep).toHaveBeenCalled();
        });
    });
});
