(function($){
    'use strict';

    var buildsPager;

    // Only enable the pager if we have two ESR versions.
    if ($('.esr-builds-table').length > 1) {
        buildsPager = new Mozilla.Pager($('#main-content'));
    }

    $(function(){
        var $form = $('#language-search');
        var $input = $('#language-search-q');
        var $tables = $('table.build-table');

        $form.on('submit', function(e) { filter(e); });
        $input.on('input', function(e) { filter(e); });

        function filter (e) {
            e.preventDefault();

            var historyEnabled = typeof history.replaceState === 'function' && e.originalEvent;
            var search_q = $.trim($input.val());  // trim whitespace

            if (!search_q) {
                show_all();

                // Replace the browser history to clear the search query
                if (historyEnabled) {
                    history.replaceState({}, document.title, '.');
                }

                return;
            }

            $tables.each(function(){
                var $table = $(this);
                var $table_content = $table.find('thead, tbody');
                var $container = $table.closest('div');
                var $not_found = $container.find('.not-found');
                var $all_rows = $table.find('tr[data-search]');
                var $matches = $all_rows.filter(function(){
                    var words = search_q.toLowerCase().split(/,|,?\s+/);
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
                    $all_rows.not($matches).hide();
                    $matches.show();
                    $table_content.show();
                    $not_found.hide();
                }
                else {
                    $table_content.hide();
                    $not_found.show();
                }
            });

            // Replace the browser history to save the search query
            if (historyEnabled) {
                history.replaceState({ query: search_q }, document.title,
                                     '?q=' + encodeURI(search_q));
            }
        }

        $(window).on('popstate', function (e) {
            var state = e.originalEvent.state;

            $input.val((state && state.query) ? state.query : '');
            $form.trigger('submit');
        });

        function show_all(){
            $tables.find('thead, tbody').show();
            $('tr[data-search]').show();
            $('.not-found').hide();
        }
    });
})(jQuery);
