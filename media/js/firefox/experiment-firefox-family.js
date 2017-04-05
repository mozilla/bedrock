(function() {
    'use strict';

    var mcnulty = new Mozilla.TrafficCop({
        id: 'experiment-firefox-family-spring-2017',
        cookieExpires: 720, // 1 month
        variations: {
            'v=a': 50, // double-control
            'v=b': 50 // actual variation
        }
    });

    mcnulty.init();
})();
