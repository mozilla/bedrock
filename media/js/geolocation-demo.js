/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

var map = null;
var circle = null;

var geodemo = {
    initialize: function() {
        if (!map) {
            map = L.map('map_canvas');
            var attribution = 'Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
            var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: attribution,
            }).addTo(map); // same as openlayers default

            if (location.search) {
                // other tile servers from http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Tile_servers
                var ocm = L.tileLayer('http://{s}.tile.opencyclemap.org/cycle/{z}/{x}/{y}.png', {
                    maxZoom: 16,
                    attribution: [
                        attribution,
                        'Imagery &copy; <a href="http://www.thunderforest.com/opencyclemap/">OpenCycleMap</a>'
                    ].join(', '),
                }),
                oct = L.tileLayer('http://{s}.tile2.opencyclemap.org/transport/{z}/{x}/{y}.png', {
                    maxZoom: 16,
                    attribution: [
                        attribution,
                        'Imagery &copy; <a href="http://www.thunderforest.com/transport/">OpenCycleMap</a>'
                    ].join(', '),
                }),
                ocl = L.tileLayer('http://{s}.tile3.opencyclemap.org/landscape/{z}/{x}/{y}.png', {
                    maxZoom: 16,
                    attribution: [
                        attribution,
                        'Imagery &copy; <a href="http://www.thunderforest.com/landscape/">OpenCycleMap</a>'
                    ].join(', '),
                }),
                cmm = L.tileLayer('http://{s}.tile.cloudmade.com/b465ca1b6fe040dba7eec0291ecb7a8c/997/256/{z}/{x}/{y}.png', {
                    attribution: [
                        attribution,
                        'Imagery &copy; <a href="http://cloudmade.com">CloudMade</a>'
                    ].join(', '),
                }), // used to be Leaflet default, api key from remo, just for local test
                mqm = L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png', {
                    subdomains: '1234',
                    attribution: [
                        attribution,
                        'Imagery &copy; <a href="http://www.mapquest.com/">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">'
                    ].join(', '),
                }),
                mbs = L.tileLayer('http://{s}.tiles.mapbox.com/v3/examples.map-vyofok3q/{z}/{x}/{y}.png', {
                    attribution: [
                        attribution,
                        'Imagery &copy; <a href="http://mapbox.com/tos/">MapBox</a>'
                    ].join(', '),
                }); // registration for free, 3000/month
                L.control.layers({
                    'OpenStreetMap': osm,
                    'OpenCycleMap': ocm,
                    'OpenCycleMap Transport': oct,
                    'OpenCycleMap Landscape': ocl,
                    'CloudMade': cmm,
                    'MapQuest': mqm,
                    'MapBox Streets': mbs,
                }, {}).addTo(map);
            }
        }
        map.setView([37.41, -122.08], 1);
    },

    aaa: function(a) {
        $('#locateButton').siblings('img').hide();
        var zoomLevel = 14;

        if (a.coords.accuracy > 500)
            zoomLevel = 10;

        map.setView([a.coords.latitude, a.coords.longitude], zoomLevel);

        if (circle) map.removeLayer(circle);

        circle = L.circle([a.coords.latitude, a.coords.longitude], a.coords.accuracy, {
            color: '#00f',
            weight: 1,
            opacity: 1,
            fillColor: '#00f',
            fillOpacity: 0.2
        }).addTo(map);
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
