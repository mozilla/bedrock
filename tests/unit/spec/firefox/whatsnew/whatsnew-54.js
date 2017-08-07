/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect */

describe('whatsnew/whatsnew-54.js', function() {
    'use strict';

    describe('getStoreURL', function() {
        it('should return valid App Store URL for defined country code', function() {
            var newURL = Mozilla.WNP54.getStoreURL('fr', 'ios');
            expect(newURL.length).toBeGreaterThan(0);
        });

        it('should return valid Play Store URL for defined country code', function() {
            var newURL = Mozilla.WNP54.getStoreURL('jp', 'android');
            expect(newURL.length).toBeGreaterThan(0);
        });

        it('should return false for undefined country codes', function() {
            var newAppStoreURL = Mozilla.WNP54.getStoreURL('xx', 'ios');
            var newPlayStoreURL = Mozilla.WNP54.getStoreURL('xx', 'android');

            expect(newAppStoreURL).toBeFalsy();
            expect(newPlayStoreURL).toBeFalsy();
        });

        it('should return false for us country code', function() {
            var newAppStoreURL = Mozilla.WNP54.getStoreURL('us', 'ios');
            var newPlayStoreURL = Mozilla.WNP54.getStoreURL('us', 'android');

            expect(newAppStoreURL).toBeFalsy();
            expect(newPlayStoreURL).toBeFalsy();
        });
    });

    describe('updateStoreLinks', function() {
        beforeEach(function() {
            var $appStoreLink = '<a id="appStoreLink" href="default">App Store</a>';
            var $playStoreLink = '<a id="playStoreLink" href="default">Play Store</a>';

            $('body').append($appStoreLink).append($playStoreLink);
        });

        afterEach(function() {
            $('#appStoreLink').remove();
            $('#playStoreLink').remove();
        });

        it('should update App Store link for defined country code', function() {
            Mozilla.WNP54.updateStoreLinks('fr');

            expect($('#appStoreLink').attr('href')).not.toEqual('default');
            expect($('#playStoreLink').attr('href')).not.toEqual('default');
        });

        it('should not update store links for unknown country code', function() {
            Mozilla.WNP54.updateStoreLinks('xx');

            expect($('#appStoreLink').attr('href')).toEqual('default');
            expect($('#playStoreLink').attr('href')).toEqual('default');
        });

        it('should not update store links for us', function() {
            Mozilla.WNP54.updateStoreLinks('us');

            expect($('#appStoreLink').attr('href')).toEqual('default');
            expect($('#playStoreLink').attr('href')).toEqual('default');
        });
    });
});
