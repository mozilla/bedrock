/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


// download buttons

/**
 * Bug 393263 A special function for IE < 9.
 * Without this hack there is no prompt to download after they click. sigh.
 * @param {link} direct link to download URL
 * @param {userAgent} optional UA string for testing purposes.
 */
function trigger_ie_download(link, userAgent) {
    'use strict';
    var ua = userAgent !== undefined ? userAgent : navigator.userAgent;
    // Only open if we got a link and this is IE < 9.
    if (link && window.site.platform === 'windows' && /MSIE\s[1-8]\./.test(ua)) {
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

// Detect Firefox ESR simply by the *non-ESR* build IDs, as a fallback of the channel detection by
// the mozUITour API. There would be some false positives if the browser is a pre-release (Nightly,
// Aurora or Beta), semi-official (e.g. Ubuntu build by Canonical) or unofficial version of Firefox,
// because those builds have a different build ID from the official non-ESR build.
function isFirefoxESR(userAgent, buildID) {
    userAgent = userAgent || navigator.userAgent;
    buildID = buildID || navigator.buildID;

    if (!isFirefox(userAgent) || isFirefoxMobile(userAgent) || !buildID) {
        return false;
    }

    var version = getFirefoxMasterVersion(userAgent);
    var ESRs = {
        // 38.0, 38.0.1, 38.0.5 and 38.0.6
        // https://wiki.mozilla.org/Releases/Firefox_38/Test_Plan
        38: ['20150508094354', '20150513174244', '20150525141253', '20150605094246']
        // 45.0 goes here
    };

    return version in ESRs && ESRs[version].indexOf(buildID) === -1;
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
