/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* eslint no-unused-vars: [2, { "varsIgnorePattern": "buildsPager" }] */

(function($){
    'use strict';

    var buildsPager;

    // Only enable the pager if we have two ESR versions.
    if ($('.esr-builds-table').length > 1) {
        buildsPager = new Mozilla.Pager($('#main-content'));

        // Show the legacy builds if the URL contains `#legacy`
        if (location.hash.replace(/^#/, '') === 'legacy') {
            buildsPager.setStateFromPath('builds', false, false);
        }
    }

    $(function (){
        var $form = $('#language-search');
        var $input = $('#language-search-q');
        var $tables = $('table.build-table');

        $form.on('submit', function(e) { filter(e); });
        $input.on('input', function(e) { filter(e); });

        function filter (e) {
            e.preventDefault();

            var historyEnabled = typeof history.replaceState === 'function' && e.originalEvent;
            var searchQ = $.trim($input.val());  // trim whitespace

            if (!searchQ) {
                showAll();

                // Replace the browser history to clear the search query
                if (historyEnabled) {
                    history.replaceState({}, document.title, '.');
                }

                return;
            }

            $tables.each(function(){
                var $table = $(this);
                var $tableContent = $table.find('thead, tbody');
                var $container = $table.closest('div');
                var $notFound = $container.find('.not-found');
                var $allRows = $table.find('tr[data-search]');
                var $matches = $allRows.filter(function(){
                    var words = searchQ.toLowerCase().split(/,|,?\s+/);
                    var data = $(this).data('search');
                    var count = 0;
                    // Array.every is not supported by older IEs. Go traditional.
                    $.each(words, function(index, word) {
                        if (data.indexOf(word) > -1) {
                            count++;
                        }
                    });
                    return words.length === count;
                });

                if ($matches.length) {
                    $allRows.not($matches).hide();
                    $matches.show();
                    $tableContent.show();
                    $notFound.hide();
                }
                else {
                    $tableContent.hide();
                    $notFound.show();
                }
            });

            // Replace the browser history to save the search query
            if (historyEnabled) {
                history.replaceState({ query: searchQ }, document.title, '?q=' + encodeURI(searchQ));
            }
        }

        $(window).on('popstate', function (e) {
            var state = e.originalEvent.state;

            $input.val((state && state.query) ? state.query : '');
            $form.trigger('submit');
        });

        function showAll(){
            $tables.find('thead, tbody').show();
            $('tr[data-search]').show();
            $('.not-found').hide();
        }
    });
})(jQuery);
