;(function($) {
    $('#fxos-learn-more').click(function(e) {
        e.preventDefault();

        var href = this.href;

        gaTrack([
            '_trackEvent','/whatsnew Interactions','button click',
            'Learn more about Firefox OS'], function() {
                window.location = href;
        });
    });
})(window.jQuery);
