
/**
 * A special function for IE.  Without this hack there is no prompt to download after they click.  sigh.
 * bug 393263
 *
 * @param string direct link to download URL
 */
function init_ie_download(link) {
  if (navigator.appVersion.indexOf('MSIE') != -1) {
    window.open(link, 'download_window', 'toolbar=0,location=no,directories=0,status=0,scrollbars=0,resizeable=0,width=1,height=1,top=0,left=0');
    window.focus();
  }
}

$(document).ready(function() {
    $('.download-link').each(function() {
        var el = $(this);
        var link = el.data('direct-link');
        el.click(function() { init_ie_download(link); });
    });
});