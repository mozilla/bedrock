var map = null;
var overlay = null;

var geodemo = {
    initialize: function() {
        map = new google.maps.Map(document.getElementById("map_canvas"), {
            center: new google.maps.LatLng(37.41, -122.08),
            zoom: 1,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });
    },

    aaa: function(a) {
        var center = new google.maps.LatLng(a.coords.latitude, a.coords.longitude);
        $('#locateButton').siblings('img').hide();
        var zoomLevel = 14;

        if (a.coords.accuracy > 500)
            zoomLevel = 10;

        map.setCenter(center);
        map.setZoom(zoomLevel);

        if (overlay) {
            overlay.setMap(null);
            overlay = null;
        }

        overlay = new google.maps.Circle({
            center: center,
            radius: a.coords.accuracy,
            fillColor: '#0000ff',
            fillOpacity: 0.2,
            strokeColor: '#0000ff',
            strokeOpacity: 1,
            strokeWeight: 1
        });
        overlay.setMap(map);
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
