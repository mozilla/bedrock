(function() {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'exp_fx_new_scene1_all_links',
        variations: {
            'v=1': 3, // link under dl button to /firefox/all/
            'v=2': 3, // link under dl button opens modal w/direct dl links
            'v=3': 3 // double control group/no variation
        }
    });

    cop.init();
})(window.Mozilla);
