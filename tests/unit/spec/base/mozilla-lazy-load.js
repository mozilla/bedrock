/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon */

describe('mozilla-lazy-load.js', function() {

    'use strict';

    beforeEach(function() {
        window.IntersectionObserver = sinon.stub();
    });

    describe('Mozilla.LazyLoad.init', function() {

        var selector = '.lazy-image-container img';

        afterEach(function(){
            Mozilla.LazyLoad.supportsInsersectionObserver = typeof IntersectionObserver !== 'undefined';
        });

        it('should observe images if IntersectionObserver is supported', function() {
            Mozilla.LazyLoad.supportsInsersectionObserver = true;
            spyOn(Mozilla.LazyLoad, 'observe');
            Mozilla.LazyLoad.init();
            expect(Mozilla.LazyLoad.observe).toHaveBeenCalledWith(selector);
        });

        it('should load all images if IntersectionObserver is not supported', function() {
            Mozilla.LazyLoad.supportsInsersectionObserver = false;
            spyOn(Mozilla.LazyLoad, 'loadAllFallback');
            Mozilla.LazyLoad.init();
            expect(Mozilla.LazyLoad.loadAllFallback).toHaveBeenCalledWith(selector);
        });

        it('should use a custom selecter when provided', function() {
            var customSelector = '.custom-selector img';
            Mozilla.LazyLoad.supportsInsersectionObserver = true;
            spyOn(Mozilla.LazyLoad, 'observe');
            Mozilla.LazyLoad.init(customSelector);
            expect(Mozilla.LazyLoad.observe).toHaveBeenCalledWith(customSelector);
        });

        it('should throw an error if passed an invalid custom selector', function() {
            expect(function() {
                Mozilla.LazyLoad.init({foo: 'bar'});
            }).toThrowError();
        });
    });

    describe('Mozilla.LazyLoad.registerObserver', function() {

        it('should register an IntersectionObserver correctly', function() {
            spyOn(window, 'IntersectionObserver');
            var observer = Mozilla.LazyLoad.registerObserver();
            expect(observer instanceof window.IntersectionObserver).toBeTruthy();
        });
    });

    describe('Mozilla.LazyLoad.observe', function() {

        var $target;

        beforeEach(function() {
            var tpl = '<div class="lazy-image-container">' +
                        '<img class="image1" src="/img/placeholder.png" data-src="/img/foo.png">' +
                        '<img class="image2" src="/img/placeholder.png" data-src="/img/foo.png">' +
                      '</div>';
            $target = $(tpl);
            $target.appendTo($('body'));
        });

        afterEach(function() {
            $target.remove();
        });

        it('should observe elements as expected', function() {
            spyOn(Mozilla.LazyLoad, 'registerObserver').and.returnValue({
                observe: sinon.spy()
            });
            var observer = Mozilla.LazyLoad.observe('.lazy-image-container img');
            expect(observer.observe.calledTwice).toBeTruthy();
        });
    });

    describe('Mozilla.LazyLoad.observerCallback', function() {

        var changes = [
            {
                intersectionRatio: 0,
                target: {
                    src: '/foo/placeholder.png',
                    dataset: {
                        src: '/foo/image1.png',
                        srcset: '/foo/image1.png 2x'
                    },
                    onload: function() {}
                }
            },
            {
                intersectionRatio: 0.1,
                target: {
                    src: '/foo/placeholder.png',
                    dataset: {
                        src: '/foo/image2.png',
                        srcset: '/foo/image2.png 2x'
                    },
                    onload: function() {}
                }
            },
            {
                intersectionRatio: 0,
                target: {
                    src: '/foo/placeholder.png',
                    dataset: {
                        src: '/foo/image3.png',
                        srcset: '/foo/image3.png 2x'
                    },
                    onload: function() {}
                }
            }
        ];

        var observer = { unobserve: function() {} };

        it('should lazy load images only when they intersect', function() {
            spyOn(observer, 'unobserve');
            Mozilla.LazyLoad.observerCallback(changes, observer);
            expect(changes[0].target.src).toEqual('/foo/placeholder.png');
            expect(changes[0].target.srcset).toEqual(undefined);
            expect(changes[2].target.src).toEqual('/foo/placeholder.png');
            expect(changes[2].target.srcset).toEqual(undefined);

            expect(changes[1].target.src).toEqual('/foo/image2.png');
            expect(changes[1].target.srcset).toEqual('/foo/image2.png 2x');
            expect(changes[1].target.onload).toEqual(Mozilla.LazyLoad.onImageLoad);
            expect(observer.unobserve).toHaveBeenCalledWith(changes[1].target);
        });
    });

    describe('Mozilla.LazyLoad.onImageLoad', function() {

        var $img;

        beforeEach(function () {
            var img = '<img src="/img/placeholder.png" data-src="/img/foo.png" data-srcset="/img/foo.png 2x">';
            $img = $(img);
            $img.appendTo($('body'));
        });

        afterEach(function(){
            $img.remove();
        });

        it('should remove the data-src attribute', function() {
            var event = {
                target: $img[0]
            };
            Mozilla.LazyLoad.onImageLoad(event);
            expect($img.attr('data-src')).toBe(undefined);
            expect($img.attr('data-src-set')).toBe(undefined);
        });
    });

    describe('Mozilla.LazyLoad.loadAllFallback', function() {

        var $target;

        beforeEach(function () {
            var tpl = '<div class="observer-list-test">' +
                        '<img class="image1" src="/img/placeholder.png" data-src="/img/foo.png" data-srcset="/img/foo.png 2x">' +
                        '<img class="image2" src="/img/placeholder.png" data-src="/img/foo.png" data-srcset="/img/foo.png 2x">' +
                      '</div>';
            $target = $(tpl);
            $target.appendTo($('body'));
        });

        afterEach(function(){
            $target.remove();
        });

        it('should register an IntersectionObserver correctly', function() {
            var image1 = $target.find('.image1')[0];
            var image2 = $target.find('.image2')[0];

            Mozilla.LazyLoad.loadAllFallback('.observer-list-test img');

            expect(image1.getAttribute('src')).toEqual('/img/foo.png');
            expect(image1.getAttribute('srcset')).toEqual('/img/foo.png 2x');
            expect(image2.getAttribute('srcset')).toEqual('/img/foo.png 2x');
            expect(image2.getAttribute('src')).toEqual('/img/foo.png');
            expect(image1.onload).toEqual(Mozilla.LazyLoad.onImageLoad);
            expect(image2.onload).toEqual(Mozilla.LazyLoad.onImageLoad);
        });
    });
});
