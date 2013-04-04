/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * 
 */


/**
 * Over-ride this function that's originally setup in /js/download.js
 * We don't want to spawn the pop-up download hack if we're already
 * on the download page, since it will result in two downloads (the
 * href is already a direct link).
 *
 */
function init_download() {
}



function parseGETVars()
{
    // validate query according to RFC 3986
    var qs = location.search.substring(1);
    if (qs.match(/[^a-zA-Z0-9\-\._~%!$&'()*+,;=:@\/\?]/))
        return false;

    var nv = qs.split('&');
    var url = {};
    for(i = 0; i < nv.length; i++) {
        var eq = nv[i].indexOf('=');
        url[nv[i].substring(0,eq).toLowerCase()] = unescape(nv[i].substring(eq + 1));
    }

    return url;
}

function validateDownloadVar(value)
{
    // validate download vars to prevent XSS
    if (value.match(/[^\-\.A-Za-z0-9]/))
        return false;

    return true;
}

var download_url = '';

function initDownload()
{
    // 1. Grab vars from URL (PRODUCT, OS, and LANG)
    var get = parseGETVars();

    var product = (get['product']) ? get['product'] : null;
    var os      = (get['os'])      ? get['os']      : null;
    var dlang    = (get['dlang'])    ? get['dlang']    : null;
    var channel = (get['channel']) ? get['channel'] : null;

    if ( !os || !dlang
        || !validateDownloadVar(product)
        || !validateDownloadVar(os)
        || !validateDownloadVar(dlang)
    ) {
        // No vars were specified, just display the fallback content.
        return;
    }


    /**
     * Gets whether or not the client is an officially unsupported platform
     *
     * Officially unsupported platforms are Windows 95, 98, ME and NT 4.x
     *
     * The regular expression matches:
     *
     *  - Win16
     *  - Win9x
     *  - Win95
     *  - Win98
     *  - WinNT (not followed by version or followed bu version < 5)
     *  - Windows ME
     *  - Windows CE
     *  - Windows 9x
     *  - Windows 95
     *  - Windows 98
     *  - Windows 3.1
     *  - Windows 4.10
     *  - Windows NT (not followed by version or followed by version < 5)
     *  - Windows_95
     */
    gPlatformUnsupported = 
        /(Win(16|9[x58]|NT( [1234]| [^0-9]|[^ -]|$))|Windows ([MC]E|9[x58]|3\.1|4\.10|NT( [1234]| [^0-9]|[^ ]|$))|Windows_95)/.test(navigator.userAgent);

    // Check for known unsupported platforms and redirect to the
    // unsupported platform page.
    if (gPlatformUnsupported) {
        var uri = location.protocol + '//' + location.host + '/<?=$lang?>/firefox/unsupported-systems.html' + location.search;
        window.location = uri;
        return;
    }

    switch (os) {
        case 'win' :
            var at_least_xp = /Windows NT (5\.[1-9]|[6-9]\.|[1-9][0-9]+\.)/.test(navigator.userAgent);
            if (jQuery.browser.msie && at_least_xp) {
                $('#install-steps-default').hide();
                $('#install-steps-windows').show();
            }
            break;
        case 'osx' :
            $('#install-steps-default').hide();
            $('#install-steps-osx').show();
        break;
    }

    // 2. Build download.mozilla.org URL out of those vars.
    download_url = "https://download.mozilla.org/?product=";
    download_url += product + '&os=' + os + '&dlang=' + dlang;

    if (typeof(channel != "undefined" && channel !== null)) {
        if (channel == 'fxaurora' || channel == 'aurora') {
            download_url = getDownloadURLForAuroraForLanguage(product, product_version, dlang, os);
        } 
    }

}

initDownload();

function downloadURL() {
    // Only start the download if we're not in IE.
    if (download_url.length != 0 && navigator.appVersion.indexOf('MSIE') == -1) {
        // 5. automatically start the download of the file at the constructed download.mozilla.org URL

        window.location = download_url;
    }
}

// If we're in Safari, call via setTimeout() otherwise use onload.
if ( navigator.appVersion.indexOf('Safari') != -1 ) {
    window.setTimeout(downloadURL, 2500);
} else {
    window.onload = downloadURL;
}


