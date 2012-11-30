(function($){
"use strict";

$(function(){
    var $form = $('#language-search');
    var $input = $('#language-search-q');
    var $tables = $('table.build-table');

    $form.on('submit', function(e){
        e.preventDefault();
        var search_q = $input.val().replace(/^\s+|\s+$/g, '');  // trim whitespace
        if (!search_q) {
            show_all();
            return;
        }

        $tables.each(function(){
            var $table = $(this);
            var $container = $table.closest('div');
            var $not_found = $container.find('.not-found');
            var $all_rows = $table.find('tr[data-search]');
            var $matches = $all_rows.filter(function(){
                return $(this).data('search').indexOf(search_q) > -1;
            });

            if ($matches.length) {
                $all_rows.not($matches).hide();
                $matches.show();
                $table.show();
                $not_found.hide();
            }
            else {
                $table.hide();
                $not_found.show();
            }
        });
    });

    var show_all = function(){
        $tables.show();
        $('tr[data-search]').show();
        $('.not-found').hide();
    };
});

})(jQuery);
