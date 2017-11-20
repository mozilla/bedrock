/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn */

describe('mozilla-utils.js', function() {

    'use strict';

    describe('triggerIEDownload', function () {

        beforeEach(function() {
            window.site.platform = 'windows';
        });

        afterEach(function() {
            window.site.platform = 'other';
        });

        it('should open a popup for IE < 9', function () {
            var userAgent = 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)';
            window.open = sinon.stub();
            Mozilla.UtilsIE8.triggerIEDownload('foo', userAgent);
            expect(window.open.called).toBeTruthy();
        });

        it('should not open a popup for IE 9', function () {
            var userAgent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)';
            window.open = sinon.stub();
            Mozilla.UtilsIE8.triggerIEDownload('foo', userAgent);
            expect(window.open.called).not.toBeTruthy();
        });

        it('should not open a popup for other browsers', function () {
            var userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36';
            window.open = sinon.stub();
            Mozilla.UtilsIE8.triggerIEDownload('foo', userAgent);
            expect(window.open.called).not.toBeTruthy();
        });

    });

    describe('initDownloadLinks', function () {

        /* Append an HTML fixture to the document body
         * for each test in the scope of this suite */
        beforeEach(function () {
            $('<a class="download-link" data-direct-link="bar">foo</a>').appendTo('body');
        });

        /* Then after each test remove the fixture */
        afterEach(function() {
            $('.download-link').remove();
        });

        it('should call triggerIEDownload when clicked', function () {
            spyOn(Mozilla.UtilsIE8, 'triggerIEDownload');
            Mozilla.UtilsIE8.initDownloadLinks();
            $('.download-link').trigger('click');
            expect(Mozilla.UtilsIE8.triggerIEDownload).toHaveBeenCalled();
        });

    });
});
