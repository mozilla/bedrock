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
    if (isFirefox()) {
        window.getFirefoxDetails(function(data) {
            // if using an out of date firefox
            if (!data.isUpToDate) {
                // look at each button to see if it's set to check for old firefox
                $('.download-button').each(function() {
                    var $button = $(this);

                    if ($button.hasClass('download-button-check-old-fx')) {
                        // replace subtitle copy
                        $button.find('.download-subtitle').text(window.trans('global-update-firefox'));
                    }
                });
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
    var $language = $('#language');
    var previousLanguage = $language.val();
    $language.change(function() {

        window.dataLayer.push({
            'event': 'change-language',
            'languageSelected': $language.val(),
            'previousLanguage': previousLanguage
        });
        $('#lang_form').submit();
    });
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

/**
 * Get the user's Firefox version number.
 *
 * @param  {String} ua - browser's user agent string, navigator.userAgent is
 *                  used if not specified
 * @return {String} version number.
 */
function getFirefoxVersion(ua) {
    ua = ua || navigator.userAgent;

    var matches = /Firefox\/(\d+\.\d+(?:\.\d+)?)/.exec(ua);

    return (matches !== null && matches.length > 0) ? matches[1] : '0';
};

/**
 * Get the user's Firefox major version number.
 *
 * @param  {String} ua - browser's user agent string, navigator.userAgent is
 *                  used if not specified
 * @return {Integer} major version number
 */
function getFirefoxMasterVersion(ua) {
    return parseInt(getFirefoxVersion(ua), 10);
}

/**
 * Detect whether the user's Firefox is up to date or outdated. This data is
 * mainly used for security notifications.
 *
 * @param  {Boolean} strict - whether the minor and patch-level version numbers
 *                   should be compared. Default: true
 * @param  {Boolean} isESR - whether the Firefox update channel is ESR
 * @param  {String}  userVer - browser's version number
 * @return {Boolean} result
 */
function isFirefoxUpToDate(strict, isESR, userVer) {
    strict = strict === undefined ? true : strict;
    isESR = isESR === undefined ? isFirefoxESR() : isESR;
    userVer = userVer === undefined ? getFirefoxVersion() : userVer;

    var $html = $(document.documentElement);

    if (!$html.attr('data-esr-versions') || !$html.attr('data-latest-firefox')) {
        return false;
    }

    var versions = isESR ? $.parseJSON($html.attr('data-esr-versions').replace(/\'/g, '"'))
                         : [$html.attr('data-latest-firefox')];
    var userVerArr = userVer.match(/^(\d+\.\d+(?:\.\d+)?)/)[1].split('.');
    var isUpToDate = false;

    // Compare the newer version first
    versions.sort(function(a, b) { return parseFloat(a) < parseFloat(b); });

    // Only check the major version in non-strict comparison mode
    if (!strict) {
        userVerArr.length = 1;
    }

    for (var i = 0; i < versions.length; i++) {
        var latestVerArr = versions[i].split('.');

        // Only check the major version in non-strict comparison mode
        if (!strict) {
            latestVerArr.length = 1;
        }

        for (var j = 0; j < userVerArr.length; j++) {
            if (Number(userVerArr[j]) < Number(latestVerArr[j] || 0)) {
                isUpToDate = false;
                break;
            } else {
                isUpToDate = true;
            }
        }

        if (isUpToDate) {
            break;
        }
    }

    return isUpToDate;
};

/**
 * Use the async mozUITour API of Firefox to retrieve the user's browser info,
 * including the update channel and accurate, patch-level version number. This
 * API is available on Firefox 35 and later.
 * http://bedrock.readthedocs.org/en/latest/uitour.html
 *
 * @param  {Function} callback - callback function to be executed
 * @return {None}
 */
function getFirefoxDetails(callback) {
    var callbackID = Math.random().toString(36).replace(/[^a-z]+/g, '');

    var listener = function (event) {
        if (!event.detail || !event.detail.data ||
                event.detail.callbackID !== callbackID) {
            return;
        }

        // Cancel the timer as we've got the data
        window.clearTimeout(fallback);
        document.removeEventListener('mozUITourResponse', listener);

        var version = event.detail.data.version;
        var channel = event.detail.data.defaultUpdateChannel;

        // Fire the callback function with the accurate data
        callback({
            version: version,
            channel: channel,
            isUpToDate: isFirefoxUpToDate(true, channel === 'esr', version),
            isESR: channel === 'esr'
        });
    };

    // Prepare fallback function in case the API doesn't work
    var fallback = window.setTimeout(function () {
        var isESR = isFirefoxESR();

        document.removeEventListener('mozUITourResponse', listener);

        callback({
            version: getFirefoxVersion(),
            channel: isESR ? 'esr' : 'release',
            isUpToDate: isFirefoxUpToDate(false, false, userVer),
            isESR: isESR
        });
    }, 500);

    // Trigger the API
    document.addEventListener('mozUITourResponse', listener);
    document.dispatchEvent(new CustomEvent('mozUITour', {
        bubbles: true,
        detail: {
            action: 'getConfiguration',
            data: { configuration: 'appinfo', callbackID: callbackID }
        }
    }));
};

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
