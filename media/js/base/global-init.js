/* global init_download_links, init_mobile_download_links,
   update_download_text_for_old_fx, init_lang_switcher */

// init global.js functions
$(document).ready(function() {
    init_download_links();
    init_mobile_download_links();
    update_download_text_for_old_fx();
    init_lang_switcher();
    $(window).on('load', function () {
        $('html').addClass('loaded');
    });
});
