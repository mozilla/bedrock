/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $brandPopup = $('#brand-popup');
    var supportsTransition = 'transition' in document.body.style;

    $('#close-brand-popup').on('click', function(e) {
        e.preventDefault();

        // Modern browsers get CSS transitions, else no animation for older browsers.
        if (supportsTransition) {
            $brandPopup.addClass('fade-out');
        } else {
            $brandPopup.remove();
        }
    });

    $brandPopup.on('transitionend', function(event) {
        var $target = $(event.target);

        // Remove popup only if the transition event came from the correct target element.
        if (event.originalEvent.propertyName === 'opacity' && $target.hasClass('fade-out')) {
            $brandPopup.remove();
        }
    });

    function enableStickyPopup() {
        try {
            if (sessionStorage.getItem('mozorg.popup.seen') !== 'true') {
                $brandPopup.addClass('show');
                /**
                 * set the mozorg.popup state to true indicating that the user has
                 * seen the popup during their current session.
                 */
                sessionStorage.setItem('mozorg.popup.seen', 'true');

                window.dataLayer.push({
                    'event': 'ad-impression',
                    'ad-content': 'open branding',
                    'interaction': 'impression'
                });
            }
        } catch(e) {
            // Nothing to see here.
        }
    }

    /**
     * Popup is waffled so first ensure it exists.
     * It should only be sticky for desktop browsers that have a tall enough screen
     */
    if ($brandPopup.length && typeof matchMedia !== 'undefined') {
        var mqDesktop = matchMedia('(min-width: 760px) and (min-height: 600px)');

        mqDesktop.addListener(function(mq) {
            if (mq.matches) {
                enableStickyPopup();
            } else {
                enableStickyPopup();
            }
        });

        if (mqDesktop.matches) {
            enableStickyPopup();
        }
    }

    // This class is used only for functional tests, to flag when the popup is ready.
    $('html').addClass('brand-popup-ready');

})(window.jQuery);
