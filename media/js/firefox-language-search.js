(function($){
"use strict";

$(function(){
    var $form = $('#language-search');
    var $input = $('#language-search-q');
    var $tables = $('table.build-table');
    var ariaAnnounce = $('<div/>').attr({
        'role': 'status',
        'aria-live': 'polite',
        'class': 'hidden'
    });
    
    $('body').append(ariaAnnounce);

    $form.on('submit', function(e){
        e.preventDefault();
        var search_q = $.trim($input.val()).toLowerCase();  // trim whitespace
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
                return $(this).data('search').indexOf(search_q) !== -1;
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
        aria_announcement(search_q);
    });
    
    function aria_announcement (search_q) {
        var announcement = 'You have searched for '+search_q+', resulting in '+ $('#localized tbody tr:visible').length + ' fully localized version and '+ $('#localized-testing tbody tr:visible').length +' localized version in testing in the two tables below';
        ariaAnnounce.html(announcement);
        var clear_announcement = setTimeout(function() {
            ariaAnnounce.html('');
        }, 5000);
    }
 
    function show_all(){
        $tables.find('thead, tbody').show();
        $('tr[data-search]').show();
        $('.not-found').hide();
    }
});

})(jQuery);
