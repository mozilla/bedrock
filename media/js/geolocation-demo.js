var map = null;
var vector = null;

var geodemo = {
    initialize: function() {
        if (!map) {
            map = new OpenLayers.Map("map_canvas");
            var layer = new OpenLayers.Layer.OSM("OpenStreetMap");
            vector = new OpenLayers.Layer.Vector("vector");
            map.addLayers([layer, vector]);
        }

        map.setCenter(new OpenLayers.LonLat(-122.08, 37.41).transform(
            new OpenLayers.Projection("EPSG:4326"),
            map.getProjectionObject()
        ), 1);
    },

    aaa: function(a) {
        var center = new OpenLayers.LonLat(a.coords.longitude, a.coords.latitude).transform(
            new OpenLayers.Projection("EPSG:4326"),
            map.getProjectionObject()
        );

        $('#locateButton').siblings('img').hide();
        var zoomLevel = 14;

        if (a.coords.accuracy > 500)
            zoomLevel = 10;

        map.setCenter(center, zoomLevel);

        vector.removeAllFeatures();

        var circle = new OpenLayers.Feature.Vector(
            OpenLayers.Geometry.Polygon.createRegularPolygon(
                (new OpenLayers.Geometry.Point(center.lon, center.lat)),
                a.coords.accuracy,
                40,
                0
            ),
            {},
            {
                fillColor: '#0000ff',
                fillOpacity: 0.2,
                strokeColor: '#0000ff',
                strokeOpacity: 1,
                strokeWidth: 1
            }
        );
        vector.addFeatures([circle]);
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
