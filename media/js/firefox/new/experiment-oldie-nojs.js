(function(Mozilla) {
    'use strict';

    var cop;

    // run on IE 8 only
    if (window.site.platform === 'windows' && /MSIE\s8\./.test(navigator.userAgent)) {
        cop = new Mozilla.TrafficCop({
            id: 'experiment-firefox-new-oldie-nojs',
            variations: {
                'v=1': 25,
                'v=2': 25 // control (no variation)
            }
        });

        cop.init();
    }
})(window.Mozilla);
