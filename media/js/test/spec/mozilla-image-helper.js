/*
 * For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-image-helper.js', function() {

    describe('Mozilla.ImageHelper.initPlatformImages', function() {

        beforeEach(function () {
            window.site = {
                platform: 'other'
            };
            $('<img class="platform-img js" data-processed="false" data-src="browser.png" data-additional-platforms="android ios">').appendTo('body');
        });

        afterEach(function(){
            window.site.platform = null;
            $('.platform-img').remove();
        });

        it('should display default image for Windows', function() {
            window.site.platform = 'windows';
            Mozilla.ImageHelper.initPlatformImages();
            expect($('.platform-img').attr('src')).toEqual('browser.png');
            expect($('.platform-img').hasClass('windows')).toBeTruthy();
        });

        it('should display Mac platform image', function() {
            window.site.platform = 'osx';
            Mozilla.ImageHelper.initPlatformImages();
            expect($('.platform-img').attr('src')).toEqual('browser-mac.png');
            expect($('.platform-img').hasClass('osx')).toBeTruthy();
        });

        it('should display Linux platform image', function() {
            window.site.platform = 'linux';
            Mozilla.ImageHelper.initPlatformImages();
            expect($('.platform-img').attr('src')).toEqual('browser-linux.png');
            expect($('.platform-img').hasClass('linux')).toBeTruthy();
        });

        it('should display iOS platform image', function() {
            window.site.platform = 'ios';
            Mozilla.ImageHelper.initPlatformImages();
            expect($('.platform-img').attr('src')).toEqual('browser-ios.png');
            expect($('.platform-img').hasClass('ios')).toBeTruthy();
        });

        it('should display Android platform image', function() {
            window.site.platform = 'android';
            Mozilla.ImageHelper.initPlatformImages();
            expect($('.platform-img').attr('src')).toEqual('browser-android.png');
            expect($('.platform-img').hasClass('android')).toBeTruthy();
        });

        it('should flag that image src has been processed', function () {
            var $img = $('.platform-img');
            window.site.platform = 'windows';
            expect($img.attr('data-processed')).toEqual('false');
            Mozilla.ImageHelper.initPlatformImages();
            expect($img.attr('data-processed')).toEqual('true');
        });

        describe('high-res platform images', function () {

            var stub;

            beforeEach(function () {
                window.site = {
                    platform: 'other'
                };
                $('<img id="high-res-img" class="platform-img js" data-processed="false" data-high-res="true" data-src="browser.png" data-additional-platforms="android ios">').appendTo('body');
            });

            afterEach(function(){
                Mozilla.ImageHelper.isHighDpi.restore();
                window.site.platform = null;
                $('#high-res-img').remove();
            });

            it('should update image url for high-res devices', function () {
                stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi', function () {
                    return true;
                });
                window.site.platform = 'osx';
                Mozilla.ImageHelper.initPlatformImages();
                expect($('#high-res-img').attr('src')).toEqual('browser-mac-high-res.png');
                expect($('#high-res-img').hasClass('osx')).toBeTruthy();
            });

            it('should not update image url for low-res devices', function () {
                stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi', function () {
                    return false;
                });
                window.site.platform = 'osx';
                Mozilla.ImageHelper.initPlatformImages();
                expect($('#high-res-img').attr('src')).toEqual('browser-mac.png');
                expect($('#high-res-img').hasClass('osx')).toBeTruthy();
            });
        });
    });

    describe('Mozilla.ImageHelper.initHighResImages', function() {

        var stub;

        beforeEach(function () {
            $('<img id="high-res-img" class="js" data-processed="false" data-src="browser.png" data-high-res="true">').appendTo('body');
        });

        afterEach(function(){
            Mozilla.ImageHelper.isHighDpi.restore();
            $('#high-res-img').remove();
        });

        it('should update image url for high-res devices', function() {
            stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi', function () {
                return true;
            });
            Mozilla.ImageHelper.initHighResImages();
            expect($('#high-res-img').attr('src')).toEqual('browser-high-res.png');
        });

        it('should not update image url for low-res devices', function () {
            stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi', function () {
                return false;
            });
            Mozilla.ImageHelper.initHighResImages();
            expect($('#high-res-img').attr('src')).toEqual('browser.png');
        });

        it('should flag that image src has been processed', function () {
            var $img = $('#high-res-img');
            stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi', function () {
                return true;
            });
            expect($img.attr('data-processed')).toEqual('false');
            Mozilla.ImageHelper.initHighResImages();
            expect($img.attr('data-processed')).toEqual('true');
        });

        it('should not change the src of an image that is already processed', function () {
            var $img = $('#high-res-img');
            stub = sinon.stub(Mozilla.ImageHelper, 'isHighDpi', function () {
                return true;
            });
            $img.attr('src', 'foo.png');
            $img.attr('data-processed', 'true');
            Mozilla.ImageHelper.initHighResImages();
            expect($img.attr('src')).toEqual('foo.png');
        });
    });

});
