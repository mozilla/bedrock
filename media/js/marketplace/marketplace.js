/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

jQuery(document).ready(function ()
{
    var $button = $('#marketplace-button');

    var isFirefox18Android = (function() {
        var ua = navigator.userAgent;
        var matches = ua.match(/Android;.*(?:Firefox|Aurora)\/(\d+)\./);
        return (matches && matches[1] >= 18);
    })();

    if (isFirefox18Android) {

        // Hide default text in "Showcased" section, show Fx-specific version
        $('#showcased-nonfx').hide();
        $('#showcased-fx').show();

        // Remove the qr-codes from app previews
        $('.qr-code').remove();

        // swap marketplace button title
        $button.text($button.attr('data-mobile-title'));

    } else {

        // add accessible attributes
        $button.attr({
            'role': 'button',
            'aria-haspopup': true,
            'aria-expanded': false
        });

        var documentClickHandler = function(e)
        {
            var $target = $(e.target);

            // skip if we clicked on the panel
            if ($target.is($panel)
                || $target.parents('#marketplace-panel').length > 0
                || $target.is($button)
                || $target.parents('#marketplace-button').length > 0
            ) {
                return;
            }

            // skip if relatively positioned (mobile layout)
            if ($panel.css('position') == 'relative') {
                return;
            }

            // close the panel
            if ($panel.css('display') == 'block') {
                $panel.fadeOut();
                $button.focus();
            }
        }

        var documentKeydownHandler = function(event){
            if(event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) {
                return true;
            }
            if(event.keyCode === 27){
                $button.trigger('click');
            }
        }

        // make clicking the button open the panel
        $panel = $('#marketplace-panel');
        $button.click(function(e) {
            e.preventDefault(e);

            // change the state of aria-expanded
            $button.attr('aria-expanded', $panel.css('display') !== 'block');

            // add document click-to-close handler
            if ($panel.css('display') == 'block') {
                $(document)
                    .unbind('click', documentClickHandler)
                    .unbind('keydown', documentKeydownHandler);
                // when closed set focus to button
                $button.focus();
            } else {
                $(document)
                    .click(documentClickHandler)
                    .keydown(documentKeydownHandler);
            }

            $panel.fadeToggle();
        });

    }

});
