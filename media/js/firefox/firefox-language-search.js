(function($){
"use strict";

$(function(){
    var $form = $('#language-search');
    var $input = $('#language-search-q');
    var $tables = $('table.build-table');

    $form.on('submit', function(e){
        e.preventDefault();
        var search_q = $.trim($input.val());  // trim whitespace
        if (!search_q) {
            show_all();
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
        if (typeof history.pushState === 'function' && e.originalEvent) {
            history.pushState({ query: search_q }, document.title,
                              '?q=' + encodeURI(search_q));
        }
    });

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
