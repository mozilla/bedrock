$(document).ready(function() {
    $('li').each(function() {
        $this = $(this);
        if ($this.attr('id')) {
            var id = $this.attr('id'),
                popin = '#' + id + '-popin';
            if ($(popin).length) {
                var $popin = $(popin);
                $this.hover(function() {
                    $popin.fadeIn(200);
                }, function() {
                    $popin.fadeOut(200);
                });
            }
        }
    });
});
