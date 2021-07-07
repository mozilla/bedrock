/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global sinon */

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
            //spyOn(window, 'IntersectionObserver');
            var observer = Mozilla.LazyLoad.registerObserver();
            expect(observer instanceof window.IntersectionObserver).toBeTruthy();
        });
    });

    describe('Mozilla.LazyLoad.observe', function() {

        beforeEach(function() {
            var tpl = '<div class="lazy-image-container">' +
                        '<img class="image1" src="/img/placeholder.png" data-src="/img/foo.png">' +
                        '<img class="image2" src="/img/placeholder.png" data-src="/img/foo.png">' +
                      '</div>';
            document.body.insertAdjacentHTML('beforeend', tpl);
        });

        afterEach(function() {
            var content = document.querySelector('.lazy-image-container');
            content.parentNode.removeChild(content);
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
                    onload: function() {} // eslint-disable-line no-empty-function
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
                    onload: function() {} // eslint-disable-line no-empty-function
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
                    onload: function() {} // eslint-disable-line no-empty-function
                }
            }
        ];

        var observer = {
            unobserve: function() {} // eslint-disable-line no-empty-function
        };

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

        beforeEach(function () {
            var img = '<img class="test-image" src="/img/placeholder.png" data-src="/img/foo.png" data-srcset="/img/foo.png 2x">';
            document.body.insertAdjacentHTML('beforeend', img);
        });

        afterEach(function(){
            var content = document.querySelector('.test-image');
            content.parentNode.removeChild(content);
        });

        it('should remove the data-src attribute', function() {
            var img = document.querySelector('.test-image');
            var event = {
                target: img
            };
            Mozilla.LazyLoad.onImageLoad(event);
            expect(img.getAttribute('data-src')).toBe(null);
            expect(img.getAttribute('data-src-set')).toBe(null);
        });
    });

    describe('Mozilla.LazyLoad.loadAllFallback', function() {

        beforeEach(function () {
            var tpl = '<div class="observer-list-test">' +
                        '<img class="image1" src="/img/placeholder.png" data-src="/img/foo.png" data-srcset="/img/foo.png 2x">' +
                        '<img class="image2" src="/img/placeholder.png" data-src="/img/foo.png" data-srcset="/img/foo.png 2x">' +
                      '</div>';
            document.body.insertAdjacentHTML('beforeend', tpl);
        });

        afterEach(function(){
            var content = document.querySelector('.observer-list-test');
            content.parentNode.removeChild(content);
        });

        it('should register an IntersectionObserver correctly', function() {
            var image1 = document.querySelector('.observer-list-test .image1');
            var image2 = document.querySelector('.observer-list-test .image2');

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
