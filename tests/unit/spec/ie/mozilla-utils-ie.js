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

    describe('initDownloadLinks (regular download button)', function () {

        beforeEach(function () {
            var link = '<a class="download-link" data-direct-link="test-download-url">Download</a>';
            document.body.insertAdjacentHTML('beforeend', link);
        });

        afterEach(function() {
            document.querySelectorAll('.download-link').forEach(function(e)  {
                e.parentNode.removeChild(e);
            });
        });

        it('should call triggerIEDownload when clicked', function () {
            spyOn(Mozilla.UtilsIE, 'triggerIEDownload');
            Mozilla.UtilsIE.initDownloadLinks();
            document.querySelector('.download-link').click();
            expect(Mozilla.UtilsIE.triggerIEDownload).toHaveBeenCalledWith('test-download-url');
        });
    });

    describe('initDownloadLinks (/thanks download button)', function () {

        beforeEach(function () {
            var link = '<div class="c-button-download-thanks"><a data-direct-link="test-download-url">Download</a></div>';
            document.body.insertAdjacentHTML('beforeend', link);
        });

        afterEach(function() {
            document.querySelectorAll('.c-button-download-thanks').forEach(function(e)  {
                e.parentNode.removeChild(e);
            });
        });

        it('should call triggerIEDownload when clicked', function () {
            spyOn(Mozilla.UtilsIE, 'triggerIEDownload');
            Mozilla.UtilsIE.initDownloadLinks();
            document.querySelector('.c-button-download-thanks > a').click();
            expect(Mozilla.UtilsIE.triggerIEDownload).toHaveBeenCalledWith('test-download-url');
        });
    });
});
