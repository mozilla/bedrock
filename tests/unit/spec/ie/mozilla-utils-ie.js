/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global sinon */

describe('mozilla-utils-ie.js', function() {

    'use strict';

    describe('triggerIEDownload', function () {

        it('should open a popup to start the download', function () {
            window.open = sinon.stub();
            Mozilla.UtilsIE.triggerIEDownload('foo');
            expect(window.open.called).toBeTruthy();
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
            spyOn(Mozilla.UtilsIE, 'triggerIEDownload');
            Mozilla.UtilsIE.initDownloadLinks();
            $('.download-link').trigger('click');
            expect(Mozilla.UtilsIE.triggerIEDownload).toHaveBeenCalled();
        });

    });
});
