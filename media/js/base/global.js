/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


// download buttons

/**
 * A special function for IE.  Without this hack there is no prompt to download after they click.  sigh.
 * bug 393263
 * Note IE has since removed the 'MSIE' token in version 11. The hack is no longer needed for IE11.
 * http://msdn.microsoft.com/en-us/library/ie/bg182625%28v=vs.85%29.aspx#uaString
 * @param string direct link to download URL
 */
function trigger_ie_download(link, appVersion) {
    var version = appVersion || navigator.appVersion;
    // Only open if we got a link and this is IE < 11.
    if (link && version.indexOf('MSIE') !== -1) {
        window.open(link, 'download_window', 'toolbar=0,location=no,directories=0,status=0,scrollbars=0,resizeable=0,width=1,height=1,top=0,left=0');
        window.focus();
    }
}

// attach an event to all the download buttons to trigger the special
// ie functionality if on ie
function init_download_links() {
    $('.download-link').each(function() {
        var $el = $(this);
        $el.click(function() {
            trigger_ie_download($el.data('direct-link'));
        });
    });
    $('.download-list').attr('role', 'presentation');
}

function update_download_text_for_old_fx() {
    // if using an out of date firefox
    if (isFirefox() && !isFirefoxUpToDate()) {
        // look at each button to see if it's set to check for old firefox
        $('.download-button').each(function() {
            var $button = $(this);

            if ($button.hasClass('download-button-check-old-fx')) {
                // replace subtitle copy
                $button.find('.download-subtitle').text(window.trans('global-update-firefox'));
            }
        });
    }
}

// Replace Google Play links on Android devices to let them open
// the native Play Store app
function init_android_download_links() {
    if (site.platform === 'android') {
        $('a[href^="https://play.google.com/store/apps/"]').each(function() {
            $(this).attr('href', $(this).attr('href')
                .replace('https://play.google.com/store/apps/', 'market://'));
        });
    }
}

// language switcher

function init_lang_switcher() {
    $('#language').change(function() {
        window.dataLayer.push({
            event: 'change-language',
            languageSelected: $(this).val()
        });
        $('#lang_form').submit();
    });
}

//get Master firefox version
function getFirefoxMasterVersion(userAgent) {
    var version = 0;
    var ua = userAgent || navigator.userAgent;

    var matches = /Firefox\/([0-9]+).[0-9]+(?:.[0-9]+)?/.exec(
        ua
    );

    if (matches !== null && matches.length > 0) {
        version = parseInt(matches[1], 10);
    }

    return version;
}

// Used on the plugincheck page to also support all browsers based on Gecko.
function isLikeFirefox(userAgent) {
    var ua = userAgent || navigator.userAgent;
    return (/Iceweasel/i).test(ua) || (/IceCat/i).test(ua) ||
        (/SeaMonkey/i).test(ua) || (/Camino/i).test(ua) ||
        (/like Firefox/i).test(ua);
}

function isFirefox(userAgent) {
    var ua = userAgent || navigator.userAgent;
    return (/\sFirefox/).test(ua) && !isLikeFirefox(ua);
}

// 2015-01-20: Gives no special consideration to ESR builds
function isFirefoxUpToDate(latest) {
    var $html = $(document.documentElement);
    var fx_version = getFirefoxMasterVersion();
    var latestFirefoxVersion;

    if (!latest) {
        latestFirefoxVersion = $html.attr('data-latest-firefox');
        latestFirefoxVersion = parseInt(latestFirefoxVersion.split('.')[0], 10);
    } else {
        latestFirefoxVersion = parseInt(latest.split('.')[0], 10);
    }

    return (latestFirefoxVersion <= fx_version);
}

// used in bedrock for desktop specific checks like `isFirefox() && !isFirefoxMobile()`
// reference https://developer.mozilla.org/en-US/docs/Gecko_user_agent_string_reference
function isFirefoxMobile(userAgent) {
    var ua = userAgent || navigator.userAgent;
    return /Mobile|Tablet|Fennec/.test(ua);
}

// Detect Firefox 31 ESR using navigator.buildID. 20140716183446 is the *non-ESR*
// build ID that can be found at https://wiki.mozilla.org/Releases/Firefox_31/Test_Plan
// Since this is a simple and only way to detect ESR, there would be some false
// positives if the browser is a pre-release (Nightly, Aurora, Beta), semi-official
// (e.g. Ubuntu build by Canonical) or unofficial version of Firefox 31, because
// those builds have a different build ID from the official non-ESR build.
function isFirefox31ESR(userAgent, buildID) {
    userAgent = userAgent || navigator.userAgent;
    buildID = buildID || navigator.buildID;

    return !isFirefoxMobile(userAgent) &&
        getFirefoxMasterVersion(userAgent) === 31 &&
        buildID && buildID !== '20140716183446';
}


// Create text translation function using #strings element.
// TODO: Move to docs
// In order to use it, you need a block string_data bit inside your template,
// @see https://github.com/mozilla/bedrock/blob/master/apps/firefox/templates/firefox/partners/landing.html#L14
// then, each key name needs to be preceeded by data- as this uses data attributes
// to work. After this, you can access all strings defined inside the
// string_data block in JS using window.trans('keyofstring'); Thank @mkelly
var $strings = $('#strings');
window.trans = function trans(stringId) {
    return $strings.data(stringId);
};
