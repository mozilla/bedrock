$(document).ready(function() {

    $('#sidebar')
        .focusin(function(e) { $('#sidebar').toggleClass('child-focus'); })
        .focusout(function(e) { $('#sidebar').toggleClass('child-focus'); });

    $('#sidebar nav ul li.has-children > a').click(function(e) {
        e.preventDefault();

        var $li = $(this).parent('li');

        if ($li.hasClass('active')) {
            // close ul
            $(this).next()
                .slideUp('fast', function() {
                    $li.removeClass('active');
                })
        } else {
            $li.addClass('active');

            // open ul
            $(this).next('ul')
                .css('display', 'none')
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
