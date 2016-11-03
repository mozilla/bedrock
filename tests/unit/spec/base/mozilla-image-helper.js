/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect */

describe('mozilla-image-helper.js', function() {

    'use strict';

    describe('Mozilla.ImageHelper.initPlatformImages', function() {

        var $img;

        beforeEach(function () {
            var tpl = '<img class="platform-img js" src=""' +
                            'data-processed="false"' +
                            'data-src-windows="/img/browser-windows.png"' +
                            'data-src-windows-high-res="/img/browser-windows-high-res.png"' +
                            'data-src-mac="/img/browser-mac.png"' +
                            'data-src-mac-high-res="/img/browser-mac-high-res.png"' +
                            'data-src-linux="/img/browser-linux.png"' +
                            'data-src-linux-high-res="/img/browser-linux-high-res.png"' +
                            'data-src-android="/img/browser-android.png"' +
                            'data-src-android-high-res="/img/browser-android-high-res.png"' +
                            'data-src-ios="/img/browser-ios.png"' +
                            'data-src-ios-high-res="/img/browser-ios-high-res.png">';

            window.site.platform = 'other';
            $img = $(tpl);
            $img.appendTo($('body'));
        });

        afterEach(function(){
            window.site.platform = null;
            $img.remove();
        });

        it('should display Windows platform image', function() {
            window.site.platform = 'windows';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('/img/browser-windows.png');
            expect($img.hasClass('windows')).toBeTruthy();
        });

        it('should display Mac platform image', function() {
            window.site.platform = 'osx';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('/img/browser-mac.png');
            expect($img.hasClass('osx')).toBeTruthy();
        });

        it('should display Linux platform image', function() {
            window.site.platform = 'linux';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('/img/browser-linux.png');
            expect($img.hasClass('linux')).toBeTruthy();
        });

        it('should display iOS platform image', function() {
            window.site.platform = 'ios';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('/img/browser-ios.png');
            expect($img.hasClass('ios')).toBeTruthy();
        });

        it('should display Android platform image', function() {
            window.site.platform = 'android';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('/img/browser-android.png');
            expect($img.hasClass('android')).toBeTruthy();
        });

        it('should fall back to Windows if no appropriate platform image is found', function () {
            var tpl = '<img class="platform-img js" src=""' +
                            'data-processed="false"' +
                            'data-src-windows="/img/browser-windows.png"' +
                            'data-src-windows-high-res="/img/browser-windows-high-res.png"' +
                            'data-src-mac="/img/browser-mac.png"' +
                            'data-src-mac-high-res="/img/browser-mac-high-res.png">';
            $img.remove();
            $img = $(tpl);
            $img.appendTo($('body'));
            window.site.platform = 'linux';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('/img/browser-windows.png');
            expect($img.hasClass('linux')).toBeTruthy();
        });
    });

    describe('High Resolution Platform Images', function () {

        var $img;

        beforeEach(function () {
            var tpl = '<img class="platform-img js" src=""' +
                            'data-high-res="true"' +
                            'data-processed="false"' +
                            'data-src-windows="/img/browser-windows.png"' +
                            'data-src-windows-high-res="/img/browser-windows-high-res.png"' +
                            'data-src-mac="/img/browser-mac.png"' +
                            'data-src-mac-high-res="/img/browser-mac-high-res.png">';
            window.site.platform = 'windows';
            $img = $(tpl);
            $img.appendTo($('body'));
        });

        afterEach(function(){
            window.site.platform = null;
            $img.remove();
        });

        it('should add srcset attribute when data-high-res is true', function () {
            window.site.platform = 'osx';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('/img/browser-mac.png');
            expect($img.attr('srcset')).toEqual('/img/browser-mac-high-res.png 1.5x');
            expect($img.hasClass('osx')).toBeTruthy();
        });

        it('should not add srcset when data-high-res is not present', function () {
            $img.removeAttr('data-high-res');

            window.site.platform = 'osx';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('/img/browser-mac.png');
            expect($img[0].hasAttribute('srcset')).toBeFalsy();
            expect($img.hasClass('osx')).toBeTruthy();
        });

        it('should not add srcset when high res platform path is not present', function () {
            $img.removeAttr('data-src-mac-high-res');

            window.site.platform = 'osx';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('/img/browser-mac.png');
            expect($img[0].hasAttribute('srcset')).toBeFalsy();
            expect($img.hasClass('osx')).toBeTruthy();
        });

        it('should fall back to Windows high res if no appropriate platform image is found', function () {
            $img.removeAttr('data-src-mac');

            window.site.platform = 'osx';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('/img/browser-windows.png');
            expect($img.attr('srcset')).toEqual('/img/browser-windows-high-res.png 1.5x');
            expect($img.hasClass('osx')).toBeTruthy();
        });
    });

});
