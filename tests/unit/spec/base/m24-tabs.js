/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import M24Tabs from '../../../../media/js/base/protocol/m24-tabs.es6';

describe('m24-tabs.es6.js', function () {
    let tabOne;
    let tabTwo;
    let panelOne;
    let panelTwo;

    beforeEach(function () {
        const content = `<div class="m24-c-tabs m24-c-tabs-is-basic" id="test-tabs">
            <ul class="m24-c-tabs-list">
                <li class="m24-c-tabs-item"><a class="m24-c-tabs-link" id="panel-one-tab" href="#panel-one">One</a></li>
                <li class="m24-c-tabs-item"><a class="m24-c-tabs-link" id="panel-two-tab" href="#panel-two">Two</a></li>
            </ul>
            <section id="panel-one" class="m24-c-tabs-panel">Panel one content</section>
            <section id="panel-two" class="m24-c-tabs-panel">Panel two content</section>
        </div>`;
        document.body.insertAdjacentHTML('beforeend', content);

        tabOne = document.getElementById('panel-one-tab');
        tabTwo = document.getElementById('panel-two-tab');
        panelOne = document.getElementById('panel-one');
        panelTwo = document.getElementById('panel-two');

        spyOn(M24Tabs, 'isSupported').and.returnValue(true);

        // stub out google tag manager
        window.dataLayer = sinon.stub();
        window.dataLayer.push = sinon.stub();
    });

    afterEach(function () {
        M24Tabs.destroy('#test-tabs');
        document.getElementById('test-tabs').remove();
        window.history.replaceState(
            null,
            '',
            window.location.pathname + window.location.search
        );
    });

    describe('init()', function () {
        it('should do nothing if unsupported', function () {
            M24Tabs.isSupported.and.returnValue(false);
            M24Tabs.init('#test-tabs');
            expect(
                document.querySelector('.m24-c-tabs-list').getAttribute('role')
            ).toBeNull();
        });

        it('should set ARIA roles/relationships and select the first tab', function () {
            M24Tabs.init('#test-tabs');

            expect(
                document.querySelector('.m24-c-tabs-list').getAttribute('role')
            ).toEqual('tablist');
            expect(tabOne.getAttribute('role')).toEqual('tab');
            expect(tabOne.getAttribute('aria-controls')).toEqual('panel-one');
            expect(panelOne.getAttribute('role')).toEqual('tabpanel');
            expect(panelOne.getAttribute('aria-labelledby')).toEqual(
                'panel-one-tab'
            );
            expect(panelOne.getAttribute('tabindex')).toEqual('0');
            expect(
                tabOne.closest('.m24-c-tabs-item').getAttribute('role')
            ).toEqual('presentation');

            expect(tabOne.getAttribute('aria-selected')).toEqual('true');
            expect(tabOne.getAttribute('tabindex')).toEqual('0');
            expect(panelOne.hidden).toBeFalse();

            expect(tabTwo.getAttribute('aria-selected')).toEqual('false');
            expect(tabTwo.getAttribute('tabindex')).toEqual('-1');
            expect(panelTwo.hidden).toBeTrue();
        });

        it('should swap the container from basic to enhanced', function () {
            const container = document.getElementById('test-tabs');
            M24Tabs.init('#test-tabs');
            expect(
                container.classList.contains('m24-c-tabs-is-basic')
            ).toBeFalse();
            expect(
                container.classList.contains('m24-c-tabs-is-enhanced')
            ).toBeTrue();
        });

        it('should select the tab matching location.hash, if any', function () {
            window.history.replaceState(null, '', '#panel-two');
            M24Tabs.init('#test-tabs');
            expect(tabTwo.getAttribute('aria-selected')).toEqual('true');
            expect(panelTwo.hidden).toBeFalse();
            expect(panelOne.hidden).toBeTrue();
        });

        it('should not run init twice on the same container', function () {
            M24Tabs.init('#test-tabs');
            spyOn(M24Tabs, 'bindEvents');
            M24Tabs.init('#test-tabs');
            expect(M24Tabs.bindEvents).not.toHaveBeenCalled();
        });

        it('should not rewrite the URL for the automatic initial selection', function () {
            spyOn(window.history, 'replaceState');
            M24Tabs.init('#test-tabs');
            expect(window.history.replaceState).not.toHaveBeenCalled();
        });

        it('should not log a GA4 event for the automatic initial selection', function () {
            M24Tabs.init('#test-tabs');
            expect(window.dataLayer.push.called).toBeFalse();
        });

        it('should not call onTabChange for the automatic initial selection', function () {
            const onTabChange = jasmine.createSpy('onTabChange');
            M24Tabs.init('#test-tabs', { onTabChange: onTabChange });
            expect(onTabChange).not.toHaveBeenCalled();
        });

        it('should not add tabindex to a panel that already has focusable content', function () {
            document.getElementById('test-tabs').remove();

            document.body.insertAdjacentHTML(
                'beforeend',
                `<div class="m24-c-tabs m24-c-tabs-is-basic" id="test-tabs">
                    <ul class="m24-c-tabs-list">
                        <li class="m24-c-tabs-item"><a class="m24-c-tabs-link" id="panel-one-tab" href="#panel-one">One</a></li>
                    </ul>
                    <section id="panel-one" class="m24-c-tabs-panel"><a href="#">A link</a></section>
                </div>`
            );
            panelOne = document.getElementById('panel-one');

            M24Tabs.init('#test-tabs');

            expect(panelOne.getAttribute('tabindex')).toBeNull();
        });
    });

    describe('select() via click', function () {
        beforeEach(function () {
            M24Tabs.init('#test-tabs');
        });

        it('should switch the selected tab and panel', function () {
            tabTwo.click();

            expect(tabTwo.getAttribute('aria-selected')).toEqual('true');
            expect(tabTwo.getAttribute('tabindex')).toEqual('0');
            expect(panelTwo.hidden).toBeFalse();

            expect(tabOne.getAttribute('aria-selected')).toEqual('false');
            expect(tabOne.getAttribute('tabindex')).toEqual('-1');
            expect(panelOne.hidden).toBeTrue();
        });

        it('should update the URL hash without adding a history entry', function () {
            spyOn(window.history, 'replaceState').and.callThrough();
            tabTwo.click();
            expect(window.history.replaceState).toHaveBeenCalledWith(
                null,
                '',
                jasmine.stringMatching(/#panel-two$/)
            );
        });

        it('should log a GA4 widget_action event', function () {
            tabTwo.click();
            expect(
                window.dataLayer.push.calledWith({
                    event: 'widget_action',
                    type: 'tabs',
                    action: 'change',
                    name: 'Two'
                })
            ).toBeTrue();
        });
    });

    describe('select() via click, with onTabChange configured', function () {
        it('should call onTabChange on a real interaction, unlike on init', function () {
            const onTabChange = jasmine.createSpy('onTabChange');
            M24Tabs.init('#test-tabs', { onTabChange: onTabChange });
            expect(onTabChange).not.toHaveBeenCalled();

            tabTwo.click();
            expect(onTabChange).toHaveBeenCalledWith(tabTwo);
        });
    });

    describe('onTabKeyDown()', function () {
        let e;

        beforeEach(function () {
            M24Tabs.init('#test-tabs');
            e = {
                currentTarget: tabOne,
                preventDefault: jasmine.createSpy('preventDefault'),
                stopPropagation: jasmine.createSpy('stopPropagation')
            };
        });

        it('should move to the next tab on ArrowRight, wrapping at the end', function () {
            e.key = 'ArrowRight';
            M24Tabs.onTabKeyDown(e);
            expect(tabTwo.getAttribute('aria-selected')).toEqual('true');

            e.currentTarget = tabTwo;
            M24Tabs.onTabKeyDown(e);
            expect(tabOne.getAttribute('aria-selected')).toEqual('true');
        });

        it('should move to the previous tab on ArrowLeft, wrapping at the start', function () {
            e.key = 'ArrowLeft';
            M24Tabs.onTabKeyDown(e);
            expect(tabTwo.getAttribute('aria-selected')).toEqual('true');
        });

        it('should jump to the last tab on End and first tab on Home', function () {
            e.key = 'End';
            M24Tabs.onTabKeyDown(e);
            expect(tabTwo.getAttribute('aria-selected')).toEqual('true');

            e.key = 'Home';
            e.currentTarget = tabTwo;
            M24Tabs.onTabKeyDown(e);
            expect(tabOne.getAttribute('aria-selected')).toEqual('true');
        });

        it('should not react to, or trap, unrelated keys such as Tab or ArrowDown', function () {
            spyOn(M24Tabs, 'select');

            e.key = 'Tab';
            M24Tabs.onTabKeyDown(e);

            e.key = 'ArrowDown';
            M24Tabs.onTabKeyDown(e);

            expect(M24Tabs.select).not.toHaveBeenCalled();
            expect(e.preventDefault).not.toHaveBeenCalled();
        });
    });

    describe('destroy()', function () {
        it('should restore the basic (no-JS) state and show every panel', function () {
            const container = document.getElementById('test-tabs');
            M24Tabs.init('#test-tabs');

            M24Tabs.destroy('#test-tabs');

            expect(
                container.classList.contains('m24-c-tabs-is-basic')
            ).toBeTrue();
            expect(
                container.classList.contains('m24-c-tabs-is-enhanced')
            ).toBeFalse();
            expect(panelOne.hidden).toBeFalse();
            expect(panelTwo.hidden).toBeFalse();
            expect(
                document.querySelector('.m24-c-tabs-list').getAttribute('role')
            ).toBeNull();
            expect(panelOne.getAttribute('tabindex')).toBeNull();
            expect(
                tabOne.closest('.m24-c-tabs-item').getAttribute('role')
            ).toBeNull();
            expect(tabOne.getAttribute('aria-controls')).toBeNull();
            expect(panelOne.getAttribute('aria-labelledby')).toBeNull();
        });
    });
});
