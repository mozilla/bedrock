/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* eslint no-unused-vars: [2, { "varsIgnorePattern": "accordion" }] */

describe('mozilla-accordion.js', function () {

    'use strict';

    beforeEach(function () {
        // turn off animation effects so we can test post expand/collapse states
        jQuery.fx.off = true;

        var accordionMarkup =
            '<div id="accordion1" class="accordion">' +
                '<section>' +
                    '<h2 data-accordion-role="tab">Section 1</h2>' +
                    '<div data-accordion-role="tabpanel"><p>Section 1 contents.</p></div>' +
                '</section>' +
                '<section>' +
                    '<h2 data-accordion-role="tab">Section 2</h2>' +
                    '<div data-accordion-role="tabpanel"><p>Section 2 contents.</p></div>' +
                '</section>' +
                '<section>' +
                    '<h2 data-accordion-role="tab">Section 3</h2>' +
                    '<div data-accordion-role="tabpanel"><p>Section 3 contents.</p></div>' +
                '</section>' +
            '</div>' +
            '<div id="accordion2" class="accordion">' +
                '<section>' +
                    '<h2 data-accordion-role="tab">Section 1</h2>' +
                    '<div data-accordion-role="tabpanel"><p>Section 1 contents.</p></div>' +
                '</section>' +
                '<section>' +
                    '<h2 data-accordion-role="tab">Section 2</h2>' +
                    '<div data-accordion-role="tabpanel"><p>Section 2 contents.</p></div>' +
                '</section>' +
                '<section>' +
                    '<h2 data-accordion-role="tab">Section 3</h2>' +
                    '<div data-accordion-role="tabpanel"><p>Section 3 contents.</p></div>' +
                '</section>' +
            '</div>';

        $(accordionMarkup).appendTo('body');
    });

    afterEach(function () {
        Mozilla.Accordion.destroyAccordions();
        $('.accordion').remove();

        // turn animations back on
        jQuery.fx.off = false;

        // make sure to wipe out any saveState data
        sessionStorage.clear();
    });

    describe('Mozilla.Accordion instantiation and destruction', function () {

        it('should create a new accordion', function () {
            var accordion = new Mozilla.Accordion($('#accordion1'));

            expect(Mozilla.Accordion.accordions.length).toEqual(1);
            expect(accordion instanceof Mozilla.Accordion).toBeTruthy();
        });

        it('should instantiate all accordions', function() {
            Mozilla.Accordion.createAccordions();

            expect(Mozilla.Accordion.accordions.length).toEqual(2);
        });

        it('should find an accordion by ID', function() {
            var accordion = new Mozilla.Accordion($('#accordion1'));

            var found = Mozilla.Accordion.findAccordionById('accordion1');

            expect(found).toBeTruthy();
        });

        it('should have the correct number of sections', function () {
            var accordion = new Mozilla.Accordion($('#accordion1'));

            expect(accordion.sections.length).toEqual(3);
        });

        it('should monitor beforeUnload with an active accordion', function() {
            var accordion = new Mozilla.Accordion($('#accordion1'));

            expect(Mozilla.Accordion.monitoringBeforeUnload).toBeTruthy();
        });

        it('should destroy the accordion', function() {
            var accordion = new Mozilla.Accordion($('#accordion1'));
            var destroyed = Mozilla.Accordion.destroyAccordionById('accordion1');

            expect(destroyed).toBeTruthy();
            expect(Mozilla.Accordion.accordions.length).toEqual(0);
        });

        it('should destroy 1 of 2 accordions and continue to monitor beforeUnload', function() {
            var accordion1 = new Mozilla.Accordion($('#accordion1'));
            var accordion2 = new Mozilla.Accordion($('#accordion2'));

            Mozilla.Accordion.destroyAccordionById('accordion1');

            expect(Mozilla.Accordion.accordions.length).toEqual(1);
            expect(Mozilla.Accordion.monitoringBeforeUnload).toBeTruthy();
        });

        it('should destroy all accordions and stop monitoring beforeUnload', function() {
            var accordion1 = new Mozilla.Accordion($('#accordion1'));
            var accordion2 = new Mozilla.Accordion($('#accordion2'));

            Mozilla.Accordion.destroyAccordions();

            expect(Mozilla.Accordion.accordions.length).toEqual(0);
            expect(Mozilla.Accordion.monitoringBeforeUnload).toBeFalsy();
        });
    });

    describe('Mozilla.Accordion saveState', function() {

        it('should save the expanded state', function() {
            var accordion = new Mozilla.Accordion($('#accordion1'));

            // open the first section
            accordion.sections[0].$header.trigger('click');

            // destroy the accordion
            Mozilla.Accordion.destroyAccordionById('accordion1');

            // re-create the same accordion
            accordion = new Mozilla.Accordion($('#accordion1'));

            // make sure the first section is automatically expanded
            expect(accordion.sections[0].expanded).toBeTruthy();
        });
    });

    describe('Mozilla.Accordion expand/collapse', function () {

        var expandReturn;
        var collapseReturn;
        var accordionOptions = {
            onExpand: function(section) {
                expandReturn = section.title;
            },
            onCollapse: function(section) {
                collapseReturn = section.title;
            }
        };

        it('should expand and collapse the first section', function () {
            var accordion = new Mozilla.Accordion($('#accordion1'));

            var firstSection = accordion.sections[0];

            var $firstHeading = firstSection.$header;
            var $firstPanel = firstSection.$panel;

            $firstHeading.trigger('click');

            expect($firstHeading.attr('aria-expanded')).toEqual('true');
            expect($firstPanel.attr('aria-hidden')).toEqual('false');
            expect(firstSection.expanded).toBeTruthy();

            $firstHeading.trigger('click');

            expect($firstHeading.attr('aria-expanded')).toEqual('false');
            expect($firstPanel.attr('aria-hidden')).toEqual('true');
            expect(firstSection.expanded).toBeFalsy();
        });

        it('should execute expand and collapse callbacks', function() {
            var accordion = new Mozilla.Accordion($('#accordion1'), accordionOptions);

            var $firstHeading = accordion.sections[0].$header;

            spyOn(accordion, 'onExpand').and.callThrough();
            spyOn(accordion, 'onCollapse').and.callThrough();

            $firstHeading.trigger('click');
            expect(accordion.onExpand).toHaveBeenCalled();
            expect(expandReturn).toEqual(accordion.sections[0].title);

            $firstHeading.trigger('click');
            expect(accordion.onCollapse).toHaveBeenCalled();
            expect(collapseReturn).toEqual(accordion.sections[0].title);
        });

        it('should execute global expand and collapse callbacks', function() {
            var expandReturn;
            var collapseReturn;

            Mozilla.Accordion.globalOnExpand = function(section) {
                expandReturn = section.title;
            };

            Mozilla.Accordion.globalOnCollapse = function(section) {
                collapseReturn = section.title;
            };

            spyOn(Mozilla.Accordion, 'globalOnExpand').and.callThrough();
            spyOn(Mozilla.Accordion, 'globalOnCollapse').and.callThrough();

            var accordion = new Mozilla.Accordion($('#accordion1'));
            var $secondHeading = accordion.sections[1].$header;

            $secondHeading.trigger('click');
            expect(Mozilla.Accordion.globalOnExpand).toHaveBeenCalled();
            expect(expandReturn).toEqual(accordion.sections[1].title);

            $secondHeading.trigger('click');
            expect(Mozilla.Accordion.globalOnCollapse).toHaveBeenCalled();
            expect(collapseReturn).toEqual(accordion.sections[1].title);

            Mozilla.Accordion.globalOnExpand = null;
            Mozilla.Accordion.globalOnCollapse = null;
        });
    });
});
