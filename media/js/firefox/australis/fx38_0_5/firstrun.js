;(function($, Mozilla) {
    'use strict';

    var client = Mozilla.Client;

    var $document;

    // to be safe, make sure user is on desktop firefox version 38 or higher
    if (client.isFirefoxDesktop && client.FirefoxMajorVersion >= 38) {
        // Query if the UITour API is working before binding click handler.
        // If this fails, CTA falls back to linking to /firefox/sync/.
        Mozilla.UITour.getConfiguration('sync', function() {
            $document = $(document);

            // signup CTA opens about:accounts
            $('#cta-signup').on('click', function(e) {
                e.preventDefault();

                Mozilla.UITour.showFirefoxAccounts();
            });

            // signin CTA opens hamburger menu
            $('#cta-signin').on('click', function(e) {
                e.preventDefault();

                // call twice to correctly position highlight
                // https://bugzilla.mozilla.org/show_bug.cgi?id=1049130
                Mozilla.UITour.showHighlight('accountStatus', 'wobble');
                Mozilla.UITour.showHighlight('accountStatus', 'wobble');

                // allow clicking anywhere in page to hide menu
                // behind a timeout so event isn't captured with *this* click
                setTimeout(function() {
                    $document.one('click.hideHighlight', function(e) {
                        // don't create race condition if user clicks twice in
                        // succession on the sign in link
                        if ($(e.target).prop('id') !== 'cta-signin') {
                            Mozilla.UITour.hideHighlight();
                        }
                    });
                }, 50);
            });

            $document.on('visibilitychange', function() {
                if (document.hidden) {
                    $document.off('click.hideHighlight');
                    Mozilla.UITour.hideHighlight();
                }
            });
        });
    }
})(window.jQuery, window.Mozilla);
