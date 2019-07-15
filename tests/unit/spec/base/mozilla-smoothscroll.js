/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.3/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, it, expect */

describe('mozilla-smoothscroll.js', function () {

    'use strict';

    describe('Mozilla.smoothScroll scrolling', function () {

        it('should use window.scrollTo when native smooth scrolling is supported', function () {
            spyOn(window, 'scrollTo');

            Mozilla.smoothScroll({
                top: 200,
                unitTest: 'native'
            });

            expect(window.scrollTo).toHaveBeenCalledWith({
                behavior: 'smooth',
                top: 200,
                left: 0
            });
        });

        it('should use jQuery fallback when smooth scrolling is not supported', function () {
            spyOn(window, 'scrollTo');
            spyOn($.fn, 'animate');

            Mozilla.smoothScroll({
                top: 200,
                unitTest: 'jQuery'
            });

            expect(window.scrollTo).not.toHaveBeenCalled();
            expect($.fn.animate).toHaveBeenCalledWith({
                scrollTop: 200,
                scrollLeft: 0
            }, 400);
        });

        it('should use legacy window.scrollTo when neither smooth scrolling nor jQuery are available', function () {
            // take away jQuery for a minute
            var jQueryBack = window.jQuery;
            window.jQuery = undefined;

            spyOn(window, 'scrollTo');

            Mozilla.smoothScroll({
                top: 200,
                unitTest: 'fallback'
            });

            expect(window.scrollTo).toHaveBeenCalledWith(200, 0);

            // bring jQuery back
            window.jQuery = jQueryBack;
        });
    });
});
