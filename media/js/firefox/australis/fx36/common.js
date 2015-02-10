(function() {
    'use strict';

    var $learnMore = $('#learn-more');

    $learnMore.on('click', function(e) {
        var newTab = (this.target === '_blank' || e.metaKey || e.ctrlKey);
        var href = this.href;

        if (newTab) {
            window.gaTrack(['_trackEvent', ' firstrun Page Interactions - New Firefox Tour','button click','Learn more about Hello']);
        } else {
            e.preventDefault();
            window.gaTrack(['_trackEvent', ' firstrun Page Interactions - New Firefox Tour','button click','Learn more about Hello'], function() {
                window.location = href;
            });
        }
    });
})();
