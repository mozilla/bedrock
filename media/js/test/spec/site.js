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

    describe("getArchType", function () {

        it("should identify x86", function () {
            expect(window.site.getArchType('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0', 'Win64')).toBe('x86');
            expect(window.site.getArchType('Mozilla/5.0 (Windows NT 6.3; rv:27.0) Gecko/20100101 Firefox/27.0', 'Win32')).toBe('x86');
            expect(window.site.getArchType('Mozilla/5.0 (Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko', 'Win32')).toBe('x86');
            expect(window.site.getArchType('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0', 'MacIntel')).toBe('x86');
            expect(window.site.getArchType('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0', 'Linux x86_64')).toBe('x86');
            expect(window.site.getArchType('Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:27.0) Gecko/20100101 Firefox/27.0', 'Linux i686')).toBe('x86');
        });

        it("should identify ARM", function () {
            expect(window.site.getArchType('Mozilla/5.0 (Android; Mobile; rv:27.0) Gecko/27.0 Firefox/27.0', 'Linux armv7l')).toBe('armv7');
            expect(window.site.getArchType('Mozilla/5.0 (X11; U; Linux armv6l; en-US; rv:1.9.1b2pre) Gecko/20081116 Fennec/1.0a2pre', 'Linux armv6l')).toBe('armv6');
        });

        it("should identify PowerPC", function () {
            expect(window.site.getArchType('Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.4; en-US; rv:1.9.2.22) Gecko/20110902 Firefox/3.6.22', 'MacPPC')).toBe('ppc');
        });
    });

    describe("getArchSize", function () {

        it("should identify 64", function () {
            expect(window.site.getArchSize('Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0', 'Win64')).toBe(64);
            expect(window.site.getArchSize('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0', 'Linux x86_64')).toBe(64);
        });

        it("should identify 32", function () {
            expect(window.site.getArchSize('Mozilla/5.0 (Windows NT 6.3; rv:27.0) Gecko/20100101 Firefox/27.0', 'Win32')).toBe(32);
            expect(window.site.getArchSize('Mozilla/5.0 (Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko', 'Win32')).toBe(32);
            expect(window.site.getArchSize('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0', 'MacIntel')).toBe(32);
            expect(window.site.getArchSize('Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:27.0) Gecko/20100101 Firefox/27.0', 'Linux i686')).toBe(32);
            expect(window.site.getArchSize('Mozilla/5.0 (X11; U; Linux armv6l; en-US; rv:1.9.1b2pre) Gecko/20081116 Fennec/1.0a2pre', 'Linux armv6l')).toBe(32);
        });
    });
});
