/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.4/introduction
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-utils.js', function() {
    'use strict';

    describe('trans', function () {
        var stringDiv;

        beforeEach(function () {
            stringDiv = '<div id="strings" data-global-close="Close" ' +
            'data-global-next="Next" ' +
            'data-global-previous="Previous"> ' +
            '</div>';

            var container = document.createElement('div');
            container.innerHTML = stringDiv;
            $(container).appendTo('body');
        });

        afterEach(function() {
            $(stringDiv).remove();
        });

        it('should correctly return translation value', function () {
            var translation = Mozilla.Utils.trans('global-next');
            expect(translation === 'Next');
        });
    });

    describe('initMobileDownloadLinks', function () {

        var $link;

        afterEach(function(){
            window.site.platform = 'other';
            $link.remove();
        });

        it('should set a URL with the market scheme on Android', function () {
            window.site.platform = 'android';
            $link = $('<a class="download-link" href="https://play.google.com/store/apps/details?id=org.mozilla.firefox">foo</a>').appendTo('body');
            Mozilla.Utils.initMobileDownloadLinks();
            expect($link.attr('href')).toEqual('market://details?id=org.mozilla.firefox');
        });
    });

    describe('maybeSwitchToChinaRepackImages', function() {

        var $img;
        var defaultSrc = '/img/placeholder.png';
        var partnerASrc = '/img/foo.png';

        beforeEach(function () {
            $img = $([
                '<img src="' + defaultSrc +
                '" data-partnera-link="' + partnerASrc +
                '">download</a>'
            ].join()).appendTo('body');
        });

        afterEach(function() {
            $img.remove();
        });

        it('should use specified image for certain distributions', function () {
            Mozilla.Utils.maybeSwitchToChinaRepackImages({
                distribution: 'PartnerA'
            });
            expect($img[0].src).toContain(partnerASrc);
        });

        it('should use default image for other distributions', function () {
            Mozilla.Utils.maybeSwitchToChinaRepackImages({
                distribution: 'PartnerB'
            });
            expect($img[0].src).toContain(defaultSrc);
        });

    });
});
