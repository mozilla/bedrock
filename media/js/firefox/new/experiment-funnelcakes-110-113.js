(function(Mozilla) {
    'use strict';

    // en-US only (handled with switch)
    // Windows only
    // Non-Firefox
    // Desktop only

    // swiped from mozilla-client.js
    var ua = navigator.userAgent;
    var isLikeFirefox = /Iceweasel|IceCat|SeaMonkey|Camino|like\ Firefox/i.test(ua);
    var isFirefox = /\s(Firefox|FxiOS)/.test(ua) && !isLikeFirefox(ua);
    var isMobile = /^(android|ios|fxos)$/.test(window.site.platform);

    if (window.site.platform === 'windows' && !isFirefox && !isMobile) {
        var zed = new Mozilla.TrafficCop({
            id: 'experiment-funnelcakes-110-113',
            cookieExpires: 168, // 1 week
            variations: {
                'f=110': 1,
                'f=111': 1,
                'f=112': 1,
                'f=113': 1
            }
        });

        zed.init();
    }
})(window.Mozilla);
