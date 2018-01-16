/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global L */

$(document).ready(function() {
    var map = null;
    var circle = null;

    var geodemo = {
        initialize: function() {
            var $main = $('#main-content');

            if (!map) {
                var token = $main.data('mapbox');
                L.mapbox.accessToken = $main.data('token');
                map = L.mapbox.map('map_canvas', token);
            }
            map.setView([37.41, -122.08], 1);

            $('#locateButton').siblings('img').hide();
            $('#geodemo-error').hide();
        },

        handleSuccess: function(position) {
            $('#locateButton').siblings('img').hide();

            var center = [position.coords.latitude, position.coords.longitude];
            var radius = position.coords.accuracy;
            var zoomLevel = 14;

            if (radius > 500) {
                zoomLevel = 10;
            }

            map.setView(center, zoomLevel);

            if (circle) {
                map.removeLayer(circle);
            }

            circle = L.circle(center, radius, {
                color: '#00f',
                weight: 1,
                opacity: 1,
                fillColor: '#00f',
                fillOpacity: 0.2
            }).addTo(map);
        },

        handleError: function() {
            $('#locateButton').siblings('img').hide();
            $('#geodemo-error').show();
        },

        locateMeOnMap: function() {
            $('#geodemo-error').hide();
            $('#locateButton').siblings('img').show();
            navigator.geolocation.getCurrentPosition(this.handleSuccess, this.handleError);
        }
    };

    if (!navigator.geolocation) {
        return true; // Fx 3.5+ only
    }

    $('#try-geolocation').show();

    $('#try-geolocation').on('click', function (e) {
        e.preventDefault();
        Mozilla.Modal.createModal(this, $('#geo-demo'), { onCreate: geodemo.initialize });
    });

    $('#locateButton').on('click', function() {
        geodemo.locateMeOnMap();
    });
});
