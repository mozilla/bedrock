$(document).ready(function() {

    $('#sidebar nav ul li.has-children > a').click(function(e) {
        e.preventDefault();

        var $li = $(this).parent('li');

        if ($li.hasClass('active')) {
            // close ul
            $(this).next()
                .slideUp('fast', function() {
                    $li.removeClass('active');
                })
                .css('zoom', '1');
        } else {
            $li.addClass('active');

            // open ul
            $(this).next('ul')
                .css('display', 'none')
                .css('zoom', '1')
                .slideDown('fast');

            // close siblings
            $li
                .siblings('li.has-children')
                .find('ul')
                .slideUp(
                    'fast',
                    function() {
                        $(this)
                            .parent('li')
                            .removeClass('active');
                    }
                );
        }

    });

});
