(function() {
    'use strict';

    var cop = new Mozilla.TrafficCop({
        id: 'exp_fx_new_scene1_all_links',
        variations: {
            'v=1': 25,
            'v=2': 25
        }
    });

    cop.init();
})(window.Mozilla);
