/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn */

describe('mozilla-pager.js', function () {

    'use strict';

    describe('Mozilla.Pager instantiation', function () {

        beforeEach(function () {
            $('<div id="pager" class="pager pager-with-nav"><div class="pager-content"><div id="page1" class="pager-page"><p>Page 1</p></div><div id="page2" class="pager-page default-page"><p>Page 2</p></div></div></div>').appendTo('body');
        });

        afterEach(function (){
            Mozilla.Pager.destroyPagers();
            $('#pager').remove();
        });

        it('should create a new pager', function () {
            var pager = new Mozilla.Pager($('#pager'));
            expect(Mozilla.Pager.pagers.length).toEqual(1);
            expect(pager instanceof Mozilla.Pager).toBeTruthy();
        });

        it('pager should have the correct number of pages', function () {
            var pager = new Mozilla.Pager($('#pager'));
            expect(pager.pages.length).toEqual(2);
        });

        it('should show the intended default page', function () {
            var pager = new Mozilla.Pager($('#pager'));
            expect(pager.currentPage.id).toEqual('page2');
        });
    });

    describe('Mozilla.Pager auto rotate', function () {

        beforeEach(function () {
            $('<div id="pager" class="pager pager-auto-rotate pager-with-nav"><div class="pager-content"><div class="pager-page"><p>Page 1</p></div><div class="pager-page"><p>Page 2</p></div></div></div>').appendTo('body');
        });

        afterEach(function (){
            Mozilla.Pager.destroyPagers();
            $('#pager').remove();
        });

        it('should start auto rotate', function () {
            spyOn(Mozilla.Pager.prototype, 'startAutoRotate');
            var pager = new Mozilla.Pager($('#pager'));
            expect(Mozilla.Pager.prototype.startAutoRotate).toHaveBeenCalled();
        });

        it('should stop auto rotate on mouseenter', function () {
            spyOn(Mozilla.Pager.prototype, 'stopAutoRotate');
            var pager = new Mozilla.Pager($('#pager'));
            $('#pager').trigger('mouseenter.' + Mozilla.Pager.EVENT_NAMESPACE);
            expect(Mozilla.Pager.prototype.stopAutoRotate).toHaveBeenCalled();
        });

        it('should start auto rotate on mouseleave', function () {
            spyOn(Mozilla.Pager.prototype, 'startAutoRotate');
            var pager = new Mozilla.Pager($('#pager'));
            $('#pager').trigger('mouseleave.' + Mozilla.Pager.EVENT_NAMESPACE);
            expect(Mozilla.Pager.prototype.startAutoRotate).toHaveBeenCalled();
        });

        it('should stop auto rotate on focusin', function () {
            spyOn(Mozilla.Pager.prototype, 'stopAutoRotate');
            var pager = new Mozilla.Pager($('#pager'));
            $('#pager').trigger('focusin.' + Mozilla.Pager.EVENT_NAMESPACE);
            expect(Mozilla.Pager.prototype.stopAutoRotate).toHaveBeenCalled();
        });

        it('should start auto rotate on focusout', function () {
            spyOn(Mozilla.Pager.prototype, 'startAutoRotate');
            var pager = new Mozilla.Pager($('#pager'));
            $('#pager').trigger('focusout.' + Mozilla.Pager.EVENT_NAMESPACE);
            expect(Mozilla.Pager.prototype.startAutoRotate).toHaveBeenCalled();
        });

    });

    describe('Mozilla.Pager with navigation', function () {

        beforeEach(function () {
            $('<div id="pager" class="pager pager-with-nav"><div class="pager-content"><div class="pager-page"><p>Page 1</p></div><div class="pager-page"><p>Page 2</p></div></div></div>').appendTo('body');
        });

        afterEach(function (){
            Mozilla.Pager.destroyPagers();
            $('#pager').remove();
        });

        it('should create pager navigation', function () {
            spyOn(Mozilla.Pager.prototype, 'drawNav');
            var pager = new Mozilla.Pager($('#pager'));
            var $navButtons = $('#pager').find('.pager-nav button');
            expect(Mozilla.Pager.prototype.drawNav).toHaveBeenCalled();
            expect($navButtons).toBeTruthy();
        });

        it('should navigate to the previous page', function () {
            spyOn(Mozilla.Pager.prototype, 'prevPageWithAnimation');
            spyOn(Mozilla.Pager.prototype, 'stopAutoRotate');
            var pager = new Mozilla.Pager($('#pager'));
            $('.pager-prev').trigger('click');
            expect(Mozilla.Pager.prototype.prevPageWithAnimation).toHaveBeenCalled();
            expect(Mozilla.Pager.prototype.stopAutoRotate).toHaveBeenCalled();
        });

        it('should navigate to the next page', function () {
            spyOn(Mozilla.Pager.prototype, 'nextPageWithAnimation');
            spyOn(Mozilla.Pager.prototype, 'stopAutoRotate');
            var pager = new Mozilla.Pager($('#pager'));
            $('.pager-next').trigger('click');
            expect(Mozilla.Pager.prototype.nextPageWithAnimation).toHaveBeenCalled();
            expect(Mozilla.Pager.prototype.stopAutoRotate).toHaveBeenCalled();
        });

    });

    describe('Mozilla.Pager with tabs', function () {

        beforeEach(function () {
            $('<div id="pager" class="pager pager-auto-rotate pager-with-tabs"><ol class="pager-tabs"><li><a href="#page1">Page 1</a></li><li><a href="#page2">Page 2</a></li></ol><div class="pager-content"><div class="pager-page"><p>Page 1</p></div><div class="pager-page"><p>Page 2</p></div></div></div>').appendTo('body');
        });

        afterEach(function (){
            Mozilla.Pager.destroyPagers();
            $('#pager').remove();
        });

        it('should change page when tab is clicked', function () {
            spyOn(Mozilla.Pager.prototype, 'setPageWithAnimation');
            spyOn(Mozilla.Pager.prototype, 'stopAutoRotate');
            var pager = new Mozilla.Pager($('#pager'));
            $('.pager-tabs li:last-child a').trigger('click');
            expect(Mozilla.Pager.prototype.setPageWithAnimation).toHaveBeenCalled();
            expect(Mozilla.Pager.prototype.stopAutoRotate).toHaveBeenCalled();
        });

    });

    describe('Mozilla.Pager multiple pagers', function () {

        beforeEach(function () {
            $('<div id="pager1" class="pager pager-with-tabs"><ol class="pager-tabs"><li><a href="#page1">Page 1</a></li><li><a href="#page2">Page 2</a></li></ol><div class="pager-content"><div class="pager-page"><p>Page 1</p></div><div class="pager-page"><p>Page 2</p></div></div></div>').appendTo('body');
            $('<div id="pager2" class="pager pager-with-tabs"><ol class="pager-tabs"><li><a href="#page1">Page 1</a></li><li><a href="#page2">Page 2</a></li></ol><div class="pager-content"><div class="pager-page"><p>Page 1</p></div><div class="pager-page"><p>Page 2</p></div></div></div>').appendTo('body');
        });

        afterEach(function (){
            Mozilla.Pager.destroyPagers();
            $('#pager1').remove();
            $('#pager2').remove();
        });

        describe('createPagers', function () {

            it('should should create multiple pagers', function () {
                Mozilla.Pager.createPagers();
                expect(Mozilla.Pager.pagers.length === 2).toBeTruthy();
            });

            it('should should only create new pagers if not already initialized', function () {
                var pager = new Mozilla.Pager($('#pager1'));
                Mozilla.Pager.createPagers();
                expect(Mozilla.Pager.pagers.length === 2).toBeTruthy();
            });

            it('should only should create pagers with `pager-auto-init` class', function () {
                $('#pager1').addClass('pager-auto-init');
                Mozilla.Pager.createPagers(true);
                expect(Mozilla.Pager.pagers.length === 1).toBeTruthy();
            });
        });

        describe('findPagerById', function () {

            it('should return an instance of Mozilla.Pager', function () {
                Mozilla.Pager.createPagers();
                var pager = Mozilla.Pager.findPagerById('pager1');
                expect(pager instanceof Mozilla.Pager).toBeTruthy();
            });

            it('should return a falsy value if not found', function () {
                Mozilla.Pager.createPagers();
                var pager = Mozilla.Pager.findPagerById('pager3');
                expect(pager).toBeFalsy();
            });

        });

        describe('destroyPagers', function () {

            it('should destroy all pager instances', function () {
                Mozilla.Pager.createPagers();
                expect(Mozilla.Pager.pagers.length === 2).toBeTruthy();
                Mozilla.Pager.destroyPagers();
                expect(Mozilla.Pager.pagers.length === 0).toBeTruthy();
            });
        });

        describe('destroyPagerById', function () {

            it('should return `true` when pager is destroyed', function () {
                Mozilla.Pager.createPagers();
                expect(Mozilla.Pager.pagers.length === 2).toBeTruthy();
                var destroyedPager = Mozilla.Pager.destroyPagerById('pager2');
                expect(Mozilla.Pager.pagers.length === 1).toBeTruthy();
                expect(destroyedPager).toBeTruthy();
            });

            it('should return `false` when pager is not destroyed', function () {
                Mozilla.Pager.createPagers();
                expect(Mozilla.Pager.pagers.length === 2).toBeTruthy();
                var pager = Mozilla.Pager.findPagerById('pager3');
                expect(pager).toBeFalsy();
                expect(Mozilla.Pager.pagers.length === 2).toBeTruthy();
            });

            it('should call `updateHashMonitor` when pager is destroyed', function () {
                Mozilla.Pager.createPagers();
                spyOn(Mozilla.Pager, 'updateHashMonitor');
                Mozilla.Pager.destroyPagerById('pager2');
                expect(Mozilla.Pager.updateHashMonitor).toHaveBeenCalled();
            });
        });

    });

    describe('Mozilla.Pager history', function () {

        beforeEach(function () {
            $('<div id="pager" class="pager pager-with-tabs"><ol class="pager-tabs"><li><a href="#page1">Page 1</a></li><li><a href="#page2">Page 2</a></li></ol><div class="pager-content"><div class="pager-page"><p>Page 1</p></div><div class="pager-page"><p>Page 2</p></div></div></div>').appendTo('body');
        });

        afterEach(function () {
            Mozilla.Pager.destroyPagers();
            $('#pager').remove();
            window.location.hash = '';
        });

        it('should monitor hash changes', function () {
            spyOn(Mozilla.Pager, 'initHashMonitor');
            Mozilla.Pager.createPagers();
            expect(Mozilla.Pager.initHashMonitor).toHaveBeenCalled();
            expect(Mozilla.Pager.monitoringHash).toBeTruthy();
        });

        it('should update pager when page loads with a hash', function () {
            window.location.hash = 'page2';
            spyOn(Mozilla.Pager.prototype, 'setStateFromPath');
            Mozilla.Pager.createPagers();
            expect(Mozilla.Pager.prototype.setStateFromPath).toHaveBeenCalled();
        });

        describe('Mozilla.Pager checkLocation', function() {

            beforeEach(function (done) {
                spyOn(Mozilla.Pager, 'checkLocation');
                Mozilla.Pager.createPagers();
                window.location.hash = 'page2';
                setTimeout(function() {
                    done();
                }, 200);
            });

            it('should update pager when hash changes', function (done) {
                expect(Mozilla.Pager.checkLocation).toHaveBeenCalled();
                done();
            });
        });

        it('should not monitor hash changes if pager has `pager-no-history` class', function () {
            $('#pager').addClass('pager-no-history');
            spyOn(Mozilla.Pager, 'initHashMonitor');
            Mozilla.Pager.createPagers();
            expect(Mozilla.Pager.initHashMonitor).not.toHaveBeenCalled();
            expect(Mozilla.Pager.monitoringHash).toBeFalsy();
        });

    });

});
