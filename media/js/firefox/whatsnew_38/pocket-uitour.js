/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(function(){
    'use strict';

    var $window = $(window);
    var $document = $(document);

    function closePocketMenu() {
        // TODO close pocket menu
        Mozilla.UITour.hideHighlight();
        $document.off('click.pocket');
        $document.off('visibilitychange.pocket');
        $window.off('resize.pocket');
    }

    function handleVisibilityChange() {
        if (document.hidden) {
            closePocketMenu();
        }
    }

    // highlight pocket icon in the pallet and open the menu
    function openPocketMenu(e) {
        e.preventDefault();
        var target = 'pocket';

        Mozilla.UITour.getConfiguration('availableTargets', function (config) {
            // check to see if pocket icon is in the browser pallet
            if (config.targets && $.inArray(target, config.targets) !== -1) {
                //TODO open pocket menu
                Mozilla.UITour.showHighlight(target, 'wobble');
                $document.one('click.pocket', closePocketMenu);
                $document.one('visibilitychange.pocket', handleVisibilityChange);
                $window.one('resize.pocket', closePocketMenu);
            }
        });
    }

    $('.try-pocket').on('click.pocket', openPocketMenu);
});
