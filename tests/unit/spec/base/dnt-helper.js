/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, it, expect, _dntEnabled */

describe('dnt-helper.js', function() {

    'use strict';

    describe('_dntEnabled', function () {

        it('should return true for Fx41 on Mac with DNT set to true', function () {
            var dnt = 1;
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0';
            expect(_dntEnabled(dnt, ua)).toBe(true);
        });

        it('should return false for Fx41 on Win7 with DNT set to false', function () {
            var dnt = 0;
            var ua = 'Mozilla/5.0 (Windows NT 6.1; rv:41.0) Gecko/20100101 Firefox/41.0';
            expect(_dntEnabled(dnt, ua)).toBe(false);
        });

        // this test is required because of bug 887703
        it('should return false for Fx28 on Mac with DNT set to true', function () {
            var dnt = 1;
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:28.0) Gecko/20100101 Firefox/28.0';
            expect(_dntEnabled(dnt, ua)).toBe(false);
        });

        it('should return false for Fx 41 with DNT set to false', function () {
            var dnt = 0;
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0';
            expect(_dntEnabled(dnt, ua)).toBe(false);
        });

        it('should return false for IE on Win8 with DNT set to true', function () {
            var dnt = 1;
            var ua = 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)';
            expect(_dntEnabled(dnt, ua)).toBe(false);
        });

        it('should return true for Edge on Win10 with DNT set to true', function () {
            var dnt = 1;
            var ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240';
            expect(_dntEnabled(dnt, ua)).toBe(true);
        });

        it('should return false for Edge on Win10 with DNT set to false', function () {
            var dnt = 0;
            var ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240';
            expect(_dntEnabled(dnt, ua)).toBe(false);
        });

        it('should return false for IE11 on Win10 with DNT set to false', function () {
            var dnt = 0;
            var ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko';
            expect(_dntEnabled(dnt, ua)).toBe(false);
        });

        it('should return true for IE11 on Win10 with DNT set to true', function () {
            var dnt = 1;
            var ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko';
            expect(_dntEnabled(dnt, ua)).toBe(true);
        });

        it('should return false for IE11 on Win8.1 with DNT set to true', function () {
            var dnt = 1;
            var ua = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko';
            expect(_dntEnabled(dnt, ua)).toBe(false);
        });

        it('should return false for IE7 on Windows Vista with DNT set to undefined', function () {
            var dnt;
            var ua = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)';
            expect(_dntEnabled(dnt, ua)).toBe(false);
        });

        it('should return false for Chrome on Mac with DNT set to false', function () {
            var dnt = 0;
            var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36';
            expect(_dntEnabled(dnt, ua)).toBe(false);
        });

    });

});
