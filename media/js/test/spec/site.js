describe("site.js", function () {

    describe("getPlatform", function () {

        it("should identify old-Windows", function () {
            expect(window.site.getPlatform('Mozilla/4.0 (compatible; MSIE 4.01; Windows 95)', 'foo')).toBe('oldwin');
            expect(window.site.getPlatform('Mozilla/4.0 (compatible; MSIE 4.01; Windows 98)', 'foo')).toBe('oldwin');
            expect(window.site.getPlatform('Mozilla/2.0 (compatible; MSIE 3.0; Windows 3.1)', 'foo')).toBe('oldwin');
            expect(window.site.getPlatform('Mozilla/4.0 (compatible; MSIE 5.05; Windows NT 4.0)', 'foo')).toBe('oldwin');
        });

        it("should identify Windows", function () {
            expect(window.site.getPlatform('foo', 'Win32')).toBe('windows');
            expect(window.site.getPlatform('foo', 'Win64')).toBe('windows');
        });

        it("should identify Android", function () {
            expect(window.site.getPlatform('Mozilla/5.0 (Android; Mobile; rv:26.0) Gecko/26.0 Firefox/26.0', 'foo')).toBe('android');
            expect(window.site.getPlatform('Mozilla/5.0 (Android; Tablet; rv:26.0) Gecko/26.0 Firefox/26.0', 'foo')).toBe('android');
        });

        it("should identify Linux", function () {
            expect(window.site.getPlatform('foo', 'Linux')).toBe('linux');
        });

        it("should identify old-Mac", function () {
            expect(window.site.getPlatform('foo', 'MacPPC')).toBe('oldmac');
            expect(window.site.getPlatform('foo', 'Mac')).toBe('oldmac');
            expect(window.site.getPlatform('Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27', 'foo')).toBe('oldmac');
            expect(window.site.getPlatform('Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; nl-nl) AppleWebKit/533.16 (KHTML, like Gecko) Version/4.1 Safari/533.16', 'foo')).toBe('oldmac');
            expect(window.site.getPlatform('Mozilla/4.0 (compatible; MSIE 5.23; Mac_PowerPC)', 'foo')).toBe('oldmac');
        });

        it("should identify iOS", function () {
            expect(window.site.getPlatform('foo', 'iPhone')).toBe('ios');
            expect(window.site.getPlatform('foo', 'iPad')).toBe('ios');
            expect(window.site.getPlatform('foo', 'iPod')).toBe('ios');
            expect(window.site.getPlatform('foo', 'iPhone Simulator')).toBe('ios');
        });

        it("should identify OSX", function () {
            expect(window.site.getPlatform('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:30.0) Gecko/20100101 Firefox/30.0', 'foo')).toBe('osx');
        });

        it("should identify Firefox OS", function () {
            expect(window.site.getPlatform('Mozilla/5.0 (Mobile; rv:26.0) Gecko/26.0 Firefox/26.0', '')).toBe('fxos');
            expect(window.site.getPlatform('Mozilla/5.0 (Tablet; rv:26.0) Gecko/26.0 Firefox/26.0', '')).toBe('fxos');
        });
    });
});
