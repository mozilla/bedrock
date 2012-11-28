/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


// download buttons

/**
 * A special function for IE.  Without this hack there is no prompt to download after they click.  sigh.
 * bug 393263
 *
 * @param string direct link to download URL
 */
function trigger_ie_download(link) {
    // Only open if we got a link and this is IE.
    if (link && navigator.appVersion.indexOf('MSIE') != -1) {
        window.open(link, 'download_window', 'toolbar=0,location=no,directories=0,status=0,scrollbars=0,resizeable=0,width=1,height=1,top=0,left=0');
        window.focus();
    }
}

// attach an event to all the download buttons to trigger the special
// ie functionality if on ie
function init_download_links() {
    $('.download-link').each(function() {
        var el = $(this);
        el.click(function() {
            dcsMultiTrack('DCS.dcssip',
                          'www.mozilla.org',
                          'DCS.dcsuri',
                          window.location.pathname,
                          'WT.ti', 'Link: Get Firefox',
                          'WT.dl', 99,
                          'WT.nv', 'Content',
                          'WT.ac', 'Download Firefox');

            trigger_ie_download(el.data('direct-link'));
        });
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

//get Master firefox version
function getFirefoxMasterVersion()
{
    var version = 0;
    
    var matches = /Firefox\/([0-9]+).[0-9]+(?:.[0-9]+)?/.exec(
        navigator.userAgent
    );
    
    if (matches !== null && matches.length > 0) {
        version = parseInt(matches[1], 10);
    }
    
    return version;
}
