/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-run.js', function() {

    'use strict';

    describe('run', function() {

        afterEach(function() {
            window.site.isModernBrowser = window.site.cutsTheMustard();
        });

        it('should execute callback for modern browsers', function() {
            var obj = {
                callback: function() {} // eslint-disable-line no-empty-function
            };
            window.site.isModernBrowser = true;
            spyOn(obj, 'callback').and.callThrough();
            window.Mozilla.run(obj.callback);
            expect(obj.callback).toHaveBeenCalled();
        });

        it('should not execute callback for legacy browsers', function() {
            var obj = {
                callback: function() {} // eslint-disable-line no-empty-function
            };
            window.site.isModernBrowser = false;
            spyOn(obj, 'callback').and.callThrough();
            window.Mozilla.run(obj.callback);
            expect(obj.callback).not.toHaveBeenCalled();
        });
    });
});
