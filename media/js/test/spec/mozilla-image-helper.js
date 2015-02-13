/*
 * For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-image-helper.js', function() {

    describe('Mozilla.ImageHelper.initPlatformImages', function() {

        var stub;
        var $img;

        beforeEach(function () {
            var tpl = '<img class="platform-img js" src=""' +
                            'data-processed="false"' +
                            'data-src-windows="browser-windows.png"' +
                            'data-src-windows-high-res="browser-windows-high-res.png"' +
                            'data-src-mac="browser-mac.png"' +
                            'data-src-mac-high-res="browser-mac-high-res.png"' +
                            'data-src-linux="browser-linux.png"' +
                            'data-src-linux-high-res="browser-linux-high-res.png"' +
                            'data-src-android="browser-android.png"' +
                            'data-src-android-high-res="browser-android-high-res.png"' +
                            'data-src-ios="browser-ios.png"' +
                            'data-src-ios-high-res="browser-ios-high-res.png">';

            stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi').returns(false);
            window.site = {
                platform: 'other'
            };
            $img = $(tpl);
            $img.appendTo($('body'));
        });

        afterEach(function(){
            Mozilla.ImageHelper.isHighDpi.restore();
            window.site.platform = null;
            $img.remove();
        });

        it('should display Windows platform image', function() {
            window.site.platform = 'windows';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('browser-windows.png');
            expect($img.hasClass('windows')).toBeTruthy();
        });

        it('should display Mac platform image', function() {
            window.site.platform = 'osx';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('browser-mac.png');
            expect($img.hasClass('osx')).toBeTruthy();
        });

        it('should display Linux platform image', function() {
            window.site.platform = 'linux';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('browser-linux.png');
            expect($img.hasClass('linux')).toBeTruthy();
        });

        it('should display iOS platform image', function() {
            window.site.platform = 'ios';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('browser-ios.png');
            expect($img.hasClass('ios')).toBeTruthy();
        });

        it('should display Android platform image', function() {
            window.site.platform = 'android';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('browser-android.png');
            expect($img.hasClass('android')).toBeTruthy();
        });

        it('should flag when a platform image been processed', function () {
            window.site.platform = 'windows';
            expect($img.attr('data-processed')).toEqual('false');
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('data-processed')).toEqual('true');
        });

        it('should fall back to Windows if no appropriate platform image is found', function () {
            var tpl = '<img class="platform-img js" src=""' +
                            'data-processed="false"' +
                            'data-src-windows="browser-windows.png"' +
                            'data-src-windows-high-res="browser-windows-high-res.png"' +
                            'data-src-mac="browser-mac.png"' +
                            'data-src-mac-high-res="browser-mac-high-res.png">';
            $img.remove();
            $img = $(tpl);
            $img.appendTo($('body'));
            window.site.platform = 'linux';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('browser-windows.png');
            expect($img.hasClass('linux')).toBeTruthy();
        });
    });

    describe('High Resolution Platform Images', function () {

        var stub;
        var $img;

        beforeEach(function () {
            var tpl = '<img class="platform-img js" src=""' +
                            'data-high-res="true"' +
                            'data-processed="false"' +
                            'data-src-windows="browser-windows.png"' +
                            'data-src-windows-high-res="browser-windows-high-res.png"' +
                            'data-src-mac="browser-mac.png"' +
                            'data-src-mac-high-res="browser-mac-high-res.png">';
            window.site = {
                platform: 'windows'
            };
            $img = $(tpl);
            $img.appendTo($('body'));
        });

        afterEach(function(){
            Mozilla.ImageHelper.isHighDpi.restore();
            window.site.platform = null;
            $img.remove();
        });

        it('should update platform image url for high resolution devices', function () {
            stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi').returns(true);
            window.site.platform = 'osx';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('browser-mac-high-res.png');
            expect($img.hasClass('osx')).toBeTruthy();
        });

        it('should not update platform image url for low resolution devices', function () {
            stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi').returns(false);
            window.site.platform = 'osx';
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('src')).toEqual('browser-mac.png');
            expect($img.hasClass('osx')).toBeTruthy();
        });
    });

    describe('Mozilla.ImageHelper.initHighResImages', function() {

        var stub;
        var $img;

        beforeEach(function () {
            var tpl = '<img class="js" src=""' +
                            'data-high-res="true"' +
                            'data-processed="false"' +
                            'data-src="low-res.png"' +
                            'data-high-res-src="high-res.png">';
            $img = $(tpl);
            $img.appendTo('body');
        });

        afterEach(function(){
            Mozilla.ImageHelper.isHighDpi.restore();
            $img.remove();
        });

        it('should update image url for high resolution devices', function() {
            stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi').returns(true);
            Mozilla.ImageHelper.initHighResImages();
            expect($img.attr('src')).toEqual('high-res.png');
        });

        it('should not update image url for low resolution devices', function () {
            stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi').returns(false);
            Mozilla.ImageHelper.initHighResImages();
            expect($img.attr('src')).toEqual('low-res.png');
        });

        it('should flag when an image has been processed', function () {
            stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi').returns(true);
            expect($img.attr('data-processed')).toEqual('false');
            Mozilla.ImageHelper.initHighResImages();
            expect($img.attr('data-processed')).toEqual('true');
        });

        it('should not change the src of an image that is already processed', function () {
            stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi').returns(true);
            $img.attr('src', 'foo.png');
            $img.attr('data-processed', 'true');
            Mozilla.ImageHelper.initHighResImages();
            expect($img.attr('src')).toEqual('foo.png');
        });
    });

});
