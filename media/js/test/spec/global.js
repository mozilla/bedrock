/* Base JS unit test spec for bedrock global.js
 * For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe("global.js", function() {

  describe("init_download_links", function () {

    /* Append an HTML fixture to the document body 
     * for each test in the scope of this suite */
    beforeEach(function () {
      $('<div class="download-button"><ul class="download-list">'
        + '<li><a class="download-link" data-channel="release" data-direct-link="bar">foo</a></li></ul>'
        + '<small class="download-other"><a href="/en-US/firefox/all" data-type="all">Systems &amp; Languages</a></small>'
        + '</div>').appendTo('body');

      window.site = {};
      track_and_popup = sinon.stub();
      track_and_redirect = sinon.stub();
      init_download_links();
    });

    /* Then after each test remove the fixture */
    afterEach(function() {
      $('.download-button').remove();

      delete window.site;
    });

    it("should call track_and_popup when a download button is clicked on IE", function () {
      // Pretend we're on IE
      window.site.isIE = true;
      $('.download-link').trigger('click');
      expect(track_and_popup.called).toBeTruthy();
      expect(track_and_redirect.called).toBeFalsy();
    });

    it("should call track_and_redirect when a download button is clicked on non-IE browsers", function () {
      // Pretend we're on a non-IE browser
      window.site.isIE = false;
      $('.download-link').trigger('click');
      expect(track_and_popup.called).toBeFalsy();
      expect(track_and_redirect.called).toBeTruthy();
    });

    it("should call track_and_redirect when an ancillary link is clicked", function () {
      // Pretend we're on IE
      window.site.isIE = true;
      $('.download-other a').trigger('click');
      expect(track_and_popup.called).toBeFalsy();
      expect(track_and_redirect.callCount).toEqual(1);

      // Pretend we're on a non-IE browser
      window.site.isIE = false;
      $('.download-other a').trigger('click');
      expect(track_and_popup.called).toBeFalsy();
      expect(track_and_redirect.callCount).toEqual(2);
    });

  });

  describe("init_android_download_links", function () {

    beforeEach(function () {
      // Pretend we're on Android
      window.site = {
        platform: 'android'
      };
      //create an HTML fixture to test against
      $('<a class="download-link" href="https://play.google.com/store/apps/details?id=org.mozilla.firefox">foo</a>').appendTo('body');
    });

    afterEach(function(){
      // Tidy up after each test
      window.site = null;
      $('.download-link').remove();
    });

    it("should set a URL with the market scheme", function () {
      init_android_download_links();
      expect($('.download-link').attr('href')).toEqual('market://details?id=org.mozilla.firefox');
    });

  });

  describe("init_platform_imgs", function () {

    beforeEach(function () {
      // Pretend we're on osx for each test
      window.site = {
        platform: 'osx'
      };
      //create an HTML fixture to test against
      $('<img class="platform-img js" data-src="foo/bar.jpg" src="">').appendTo('body');
    });

    afterEach(function(){
      // Tidy up after each test
      window.site = null;
      $('.platform-img').remove();
    });

    it("should set platform specific src file", function () {
      init_platform_imgs();
      expect($('.platform-img').attr('src')).toEqual('foo/bar-mac.jpg');
    });

    it("should set platform specific css class", function () {
      init_platform_imgs();
      expect($('.platform-img').hasClass('osx')).toBeTruthy();
    });
  });

  describe("getFirefoxMasterVersion", function () {

    it("should return the firefox master version number", function () {
      var result;
      // Pretend to be Firefox 23
      var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0';
      result = getFirefoxMasterVersion(ua);
      expect(result).toEqual(23);
    });

    it("should return 0 for non Firefox browsers", function () {
      var result;
      var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36';
      result = getFirefoxMasterVersion(ua);
      expect(result).toEqual(0);
    });
  });

  describe("isFirefox", function() {
    it("should consider Firefox to be Firefox", function() {
      var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0';

      var result = isFirefox(ua);

      expect(result).toBeTruthy();
    });

    it("should not consider Camino to be Firefox", function() {
      var ua = 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; en; rv:1.9.2.24) Gecko/20111114 Camino/2.1 (like Firefox/3.6.24)';
      var result = isFirefox(ua);
      expect(result).not.toBeTruthy();
    });

    it("should not consider Chrome to be Firefox", function() {
      var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36';
      var result = isFirefox(ua);
      expect(result).not.toBeTruthy();
    });

    it("should not consider Safari to be Firefox", function() {
      var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2';
      var result = isFirefox(ua);
      expect(result).not.toBeTruthy();
    });

    it("should not consider IE to be Firefox", function() {
      var ua = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)';
      var result = isFirefox(ua);
      expect(result).not.toBeTruthy();
    });

    it("should not consider SeaMonkey to be Firefox", function() {
      var ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 SeaMonkey/2.22.1';
      var result = isFirefox(ua);
      expect(result).not.toBeTruthy();
    });
  });

  describe("isFirefoxUpToDate", function () {

      it("should consider up to date if latest is equal to firefox version", function() {
        var result;
        /* Use a stub to return a pre-programmed value
         * from getFirefoxMasterVersion */
        getFirefoxMasterVersion = sinon.stub().returns(21);
        result = isFirefoxUpToDate("21.0", [10, 17]);
        expect(getFirefoxMasterVersion.called).toBeTruthy();
        expect(result).toBeTruthy();
      });

      it("should consider up to date if latest is less than firefox version", function() {
        var result;
        getFirefoxMasterVersion = sinon.stub().returns(22);
        result = isFirefoxUpToDate("21.0", [10, 17]);
        expect(getFirefoxMasterVersion.called).toBeTruthy();
        expect(result).toBeTruthy();
      });

      it("should not consider up to date if latest greater than firefox version", function() {
        var result;
        getFirefoxMasterVersion = sinon.stub().returns(20);
        result = isFirefoxUpToDate("21.0", [10, 17]);
        expect(getFirefoxMasterVersion.called).toBeTruthy();
        expect(result).not.toBeTruthy();
      });

      it("should consider esr builds up to date", function() {
        var result;
        getFirefoxMasterVersion = sinon.stub().returns(10);
        result = isFirefoxUpToDate("21.0", [10, 17]);
        expect(getFirefoxMasterVersion.called).toBeTruthy();
        expect(result).toBeTruthy();
      });
  });

  describe("gaTrack", function () {

    var clock;

    /* Google Analytics is not loaded for these tests, so we'll
     * use an array and test the objects that get pushed to it */
    window._gaq = [];

    /* For this test suite we use fake timers, which provides
     * synchronous implementation of setTimeout. Seems a little
     * waiting is needed when testing a push to window._gaq */
    beforeEach(function () {
      clock = sinon.useFakeTimers();
    });

    afterEach(function () {
      clock.restore();
      window._gaq = [];
    });

    it("should track a single GA event", function () {
      var evt = ['_trackEvent', 'GA event test', 'test', 'test'];
      gaTrack(evt);
      clock.tick(10);
      expect(window._gaq[0]).toEqual(evt);
    });

    it("should fire a callback if needed", function () {
      /* For our callback use a jasmine spy, then we can easily test
       * to make sure it gets called once gaTrack has finished executing */
      var callback = jasmine.createSpy();
      gaTrack(['_trackEvent', 'GA event test', 'test', 'test'], callback);
      clock.tick(600); // must be longer than callback timeout (500ms) in gaTrack
      expect(callback).toHaveBeenCalled();
    });

    it("should not fire a callback twice", function () {
      /* For our callback use a jasmine spy, then we can easily test
       * to make sure it gets called once gaTrack has finished executing */
      var callback = jasmine.createSpy();
      gaTrack(['_trackEvent', 'GA event test', 'test', 'test'], callback);
      clock.tick(600); // must be longer than callback timeout (500ms) in gaTrack
      expect(callback.callCount).toEqual(1);
      // The callback should not be executed by subsequent GA events
      gaTrack(['_trackEvent', 'GA event test', 'test', 'test']);
      clock.tick(600); // must be longer than callback timeout (500ms) in gaTrack
      expect(callback.callCount).toEqual(1);
    });

    it("should still fire a callback if window._gaq is undefined", function () {
      var callback = jasmine.createSpy();
      window._gaq = undefined;
      gaTrack(['_trackEvent', 'GA event test', 'test', 'test'], callback);
      clock.tick(10);
      expect(callback).toHaveBeenCalled();
    });

  });

});
