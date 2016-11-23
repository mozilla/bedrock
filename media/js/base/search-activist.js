/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var $searchBar = $('#moz-search');
    var terms = $searchBar.data('terms').split(',');
    var displayTerm = $('.search-label-term');
    var searchField;
    var searchButton;

    // Cycle through suggested terms
    function changeTerm() {
        var term = displayTerm.data('term') || 0;
        displayTerm.data('term', term === terms.length -1 ? 0 : term + 1).text(terms[term]).fadeIn(150).delay(3500).fadeOut(150, changeTerm);
    }
    changeTerm();

    // Click on a suggested term to fill the field
    displayTerm.on('click', function() {
        searchField.val(displayTerm.text());
    });

    // Activist search
    var cx = '014783244707853607354:bbpl3emdsii';
    var gcse = document.createElement('script');
    gcse.type = 'text/javascript';
    gcse.async = true;
    gcse.src = 'https://cse.google.com/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);

    var setGTMSearch = function() {
        var element = window.google.search.cse.element.getElement('mozsearch');
        var query = element.getInputQuery();

        // GTM
        window.dataLayer.push({
            'search-query': query,
            'event': 'gcs-search'
        });
    };

    // Add event handlers
    var initMozSearch = function() {
        searchField = $('input#gsc-i-id1');
        searchButton = $('input.gsc-search-button');

        searchButton.on('click', setGTMSearch);
        searchField.keyup(function(e) {
            if (e.keyCode === 13 || e.which === 13) { // Enter
                setGTMSearch();
            }
        });
    };

    // Setup callback for when CSE is ready
    window.__gcse = {
        callback: initMozSearch
    };

})(jQuery);
