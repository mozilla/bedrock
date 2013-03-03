/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

var map = null;
var overlay = null;

var geodemo = {
    initialize: function() {
        map = new GMap2(document.getElementById("map_canvas"));
        map.setCenter(new GLatLng(37.41, -122.08), 1);
        map.addControl(new GSmallMapControl());
        map.addControl(new GMapTypeControl());
    },

    getCircleOverlay: function(lat, lon, err) {
        // math lifted from maps.forum.nu.  you want map examples, go there.
        with (Math) {
            var points = Array();
            var d = err/6378800;// accuracy / meters of Earth radius = radians  
            var lat1 = (PI/180)* lat; // radians                                                                                                                                                                                    
            var lng1 = (PI/180)* lon; // radians 
            
            for (var a = 0 ; a < 361 ; a+=10 ) {
                var tc = (PI/180)*a;
                var y = asin(sin(lat1)*cos(d)+cos(lat1)*sin(d)*cos(tc));
                var dlng = atan2(sin(tc)*sin(d)*cos(lat1),cos(d)-sin(lat1)*sin(y));
                var x = ((lng1-dlng+PI) % (2*PI)) - PI ; // MOD function
                var point = new GLatLng(parseFloat(y*(180/PI)),parseFloat(x*(180/PI)));
                points.push(point);
            }
        }
        return new GPolygon(points,'#0000ff',1,1,'#0000ff',0.2)
    },

    zoomLevel: function(a, step) {
        step++;
        map.setCenter(new GLatLng(a.coords.latitude, a.coords.longitude), step);
        if (step > 14) return;
        window.setTimeout(function() { geodemo.zoomLevel(a, step) }, 250);
    },

    aaa: function(a) {
        $('#locateButton').siblings('img').hide();
        var zoomLevel = 14;

        if (a.coords.accuracy > 500)
            zoomLevel = 10;

        map.setCenter(new GLatLng(a.coords.latitude, a.coords.longitude), zoomLevel);

        if (overlay) map.removerOverlay(overlay);

        overlay = geodemo.getCircleOverlay(a.coords.latitude, a.coords.longitude, a.coords.accuracy);
        map.addOverlay(overlay);
    },

    handleError: function(a) {
        $('#locateButton').siblings('img').hide();
        $('#geodemo-error').show();
    },

    locateMeOnMap: function() {
        $('#geodemo-error').hide();
        $('#locateButton').siblings('img').show();
        navigator.geolocation.getCurrentPosition(this.aaa, this.handleError);
    }
}

$(document).ready(function() {
    if (!navigator.geolocation) return true; // Fx 3.5+ only
    $('#try-geolocation')
        .nyroModal({
            minWidth: 510,
            minHeight: 400,
            processHandler: function() {
                $('#geodemo-error, #geo-busy').hide();
            },
            endShowContent: function() {
                geodemo.initialize();
            }
        })
        .show();
    $('#locateButton').click(function() {
        geodemo.locateMeOnMap();
    });
});
