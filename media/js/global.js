
// download buttons

/**
 * A special function for IE.  Without this hack there is no prompt to download after they click.  sigh.
 * bug 393263
 *
 * @param string direct link to download URL
 */
function trigger_ie_download(link) {
  if (navigator.appVersion.indexOf('MSIE') != -1) {
    window.open(link, 'download_window', 'toolbar=0,location=no,directories=0,status=0,scrollbars=0,resizeable=0,width=1,height=1,top=0,left=0');
    window.focus();
  }
}

// attach an event to all the download buttons to trigger the special
// ie functionality if on ie
function init_download_links() {
    $('.download-link').each(function() {
        var el = $(this);
        var link = el.data('direct-link');
        el.click(function() { trigger_ie_download(link); });
    });
}

// platform images

function init_platform_imgs() {
    $('.platform-img').each(function() {
        var suffix = '';
        if(site.platform == 'osx' || site.platform == 'mac') {
            suffix = '-mac';
        }
        else if(site.platform == 'linux') {
            suffix = '-linux';
        }
        
        var el = $(this);
        var parts = el.data('src').split('.');
        var base = parts.slice(0, parts.length-1);
        this.src = base + suffix + '.' + parts[parts.length-1];
        el.addClass(site.platform);
    });
}

// init

$(document).ready(function() {
    init_download_links();
    init_platform_imgs();
});