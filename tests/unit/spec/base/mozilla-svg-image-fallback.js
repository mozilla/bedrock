/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn */

describe('mozilla-svg-image-fallback.js', function() {

    'use strict';

    var $img;

    beforeEach(function () {
        var tpl = '<img src="/img/foo.svg" data-fallback="true" data-png="/img/foo.png">';
        $img = $(tpl);
        $img.appendTo($('body'));
    });

    afterEach(function(){
        $img.remove();
    });

    it('should replace src with png when svg is not supported', function() {
        spyOn(Mozilla.SVGImage, 'isSupported').and.returnValue(false);
        Mozilla.SVGImage.fallback();
        expect($img.attr('src')).toEqual('/img/foo.png');
    });

    it('should do nothing when svg is supported', function() {
        spyOn(Mozilla.SVGImage, 'isSupported').and.returnValue(true);
        Mozilla.SVGImage.fallback();
        expect($img.attr('src')).toEqual('/img/foo.svg');
    });

});
