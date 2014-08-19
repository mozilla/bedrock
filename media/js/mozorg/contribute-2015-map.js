/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var map = null;
    var topPane = null;
    var topLayer = null;
    var layers = {};

    var mozMap = {
        /*
         * Initialize mapbox and set default control values.
         * This should only be called once on page load.
         */
        init: function () {
            // get the mapbox api token.
            var token = $('#map').data('mapbox');
            //initialize map and center.
            map = L.mapbox.map('map').setView([28, 0], 2);
            // load mozilla custom map tiles
            var mapLayer = L.mapbox.tileLayer(token,{
                detectRetina: true
            });

            // when ready, set the map and page default states
            mapLayer.on('ready', function () {
                // add tile layer to the map
                mapLayer.addTo(map);
                // touch support detection.
                var touch = L.Browser.touch || L.Browser.msTouch;
                // disable map zoom on scroll.
                map.scrollWheelZoom.disable();
                // disable dragging for touch devices.
                if (touch) {
                    // disable drag and zoom handlers.
                    map.dragging.disable();
                    map.touchZoom.disable();
                    map.doubleClickZoom.disable();
                    // disable tap handler, if present.
                    if (map.tap) {
                        map.tap.disable();
                    }
                }
            });
        }
    };

    //initialize mapbox
    mozMap.init();

})(window.jQuery);
