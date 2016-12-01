/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    // Array.prototype.indexOf is undefined in older versions of browsers
    var arrayIndexOfSupported = typeof Array.prototype.indexOf === 'function';

    // Intl API is new, and NumberFormat is an even newer part of it
    var intlNumberFormatSupported = 'Intl' in window && 'NumberFormat' in Intl;

    var $body = $('body');
    var $takeoverModal = $('#fundraising_takeover');
    var $overlay = $('.page-overlay');
    var $closeModal = $('#close_takeover');
    var $form = $('#fundraising-form');
    var $donateOptionsSection = $('.donate-options');
    var $donateCustom = $('#donate-custom');
    var $optionLabels = $('label[class!="own-amount"]', $donateOptionsSection);
    var $optionLabelsText = $('label[class!="own-amount"] .label-text', $donateOptionsSection);
    var $options = $('input[type="radio"]', $donateOptionsSection);

    // Replaces label text with appropriately formatted numbers in supporting browsers
    function formatCurrency() {
        var locale = $form.data('locale');
        var currencyCode = $form.data('currency');
        var numberFormat = new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: currencyCode,
            minimumFractionDigits: 0
        });

        $optionLabelsText.each(function() {
            $(this).text(numberFormat.format($(this).data('amount')));
        });
    }

    // sets the mozorg.takeover state to true indicating that the user has
    // seen the takeover modal during their current session.
    function storeSession() {
        try {
            sessionStorage.setItem('mozorg.takeover.seen', 'true');
        } catch (ex) {
            // yum, errors taste nice ;)
        }
    }

    // Shows and hides the takeover modal
    // Removes the keyup event from body if specified
    function toggleModal(removeListener) {
        if (removeListener) {
            // no longer listen for keyup events.
            $body.off('keyup.takeover');
        }

        $([$takeoverModal, $overlay]).each(function() {
            $(this).toggleClass('hidden');
        });
    }

    // Removes checked from all the radio buttons
    // and selected from the labels.
    function clearOptions() {
        $optionLabels.removeClass('selected');
        $options.removeAttr('checked');
    }

    // Shows the take over modal, sets the required entry in
    // session storage and adds an `esc` key handler to close
    // the modal.
    function initTakeOver() {
        // format the currency in browsers that support it
        if (intlNumberFormatSupported) {
            formatCurrency();
        }
        // show the takeover
        toggleModal();
        // set mozorg.takeover.seen to true
        storeSession();

        // trap key events, listening for escape.
        // we only want to do this here so, we do not attach the event
        // if we are not showing the modal.
        $body.on('keyup.takeover', function(event) {
            if (event.key === 'Escape' || event.keyCode === 27) {
                // close the modal
                toggleModal(true);
            }
        });

        $overlay.on('click', function(){
            toggleModal();
        });
    }

    // Handles clicks on the labels of the radio input elements.
    $optionLabels.on('click', function() {
        // clear selected class from labels
        $optionLabels.removeClass('selected');
        // empty any value that might have been typed
        // into the custom amount field.
        $donateCustom.val('');
        // set the clicked label to selected
        $(this).addClass('selected');
    });

    // Once a user types into the custom amount field
    // clear all other options.
    $donateCustom.keyup(clearOptions);

    // the name of the parameter that indicates the amount the user
    // wish to donate has to be called amount. Seeing that we have
    // radio buttons with that name as well as an input field, we need
    // to disable the input field prior to form submission to avoid a
    // scenario where we have ?amount=50&amount=
    $form.on('submit', function() {
        if ($donateCustom.val() === '') {
            $donateCustom.attr('disabled', 'disabled');
        }
    });

    // If a user clicks on 'continue to mozilla.org',
    // close the modal and overlay
    $closeModal.on('click', function(event) {
        event.preventDefault();
        toggleModal(true);
    });

    // Do not bother showing the modal for users of IE8 and below
    // the donate.m.o site does not work for it.
    // Modal is waffled so first ensure it exists.
    if (arrayIndexOfSupported && $takeoverModal.length > 0) {
        try {
            // only show the takeover modal if the user has not already seen it
            // during this session.
            if (sessionStorage.getItem('mozorg.takeover.seen') !== 'true') {
                initTakeOver();
            }
        } catch (ex) {
            // Nothing to see here
        }
    }

    $('html').addClass('eoy-takeover');

})(jQuery);
