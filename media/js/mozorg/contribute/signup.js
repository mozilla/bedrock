$(function() {
    var $tooltipTrigger = $('.task h3');

    $tooltipTrigger.on('mouseenter', function() {
        var $currentItem = $(this).parents('li');
        $('.tooltip', $currentItem).removeClass('hidden');
    });

    $tooltipTrigger.on('mouseleave', function() {
        var $currentItem = $(this).parents('li');
        $('.tooltip', $currentItem).addClass('hidden');
    });
});
