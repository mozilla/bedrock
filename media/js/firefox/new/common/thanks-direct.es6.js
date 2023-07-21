/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import TrackProductDownload from '../../../base/datalayer-productdownload.es6';

let timeout;
let requestComplete = false;

function beginFirefoxDownload() {
    const directDownloadLink = document.getElementById('direct-download-link');
    let downloadURL;

    // Only auto-start the download if a supported platform is detected.
    if (
        Mozilla.DownloadThanks.shouldAutoDownload(
            window.site.platform,
            window.site.fxSupported
        ) &&
        typeof Mozilla.Utils !== 'undefined'
    ) {
        downloadURL = Mozilla.DownloadThanks.getDownloadURL(window.site);

        if (downloadURL) {
            // Pull download link from the download button and add to the 'Try downloading again' link.
            // Make sure the 'Try downloading again' link is well formatted! (issue 9615)
            if (directDownloadLink && directDownloadLink.href) {
                directDownloadLink.href = downloadURL;
                directDownloadLink.addEventListener(
                    'click',
                    (event) => {
                        try {
                            TrackProductDownload.handleLink(event);
                        } catch (error) {
                            return;
                        }
                    },
                    false
                );
            }

            // Start the platform-detected download a second after DOM ready event.
            Mozilla.Utils.onDocumentReady(function () {
                try {
                    TrackProductDownload.sendEventFromURL(downloadURL);
                } catch (error) {
                    return;
                }
                setTimeout(function () {
                    window.location.href = downloadURL;
                }, 1000);
            });
        }
    }
}

function onSuccess() {
    // Make sure we only initiate the download once!
    clearTimeout(timeout);
    if (requestComplete) {
        return;
    }
    requestComplete = true;

    // Fire GA event to log attribution success
    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'direct-attribution',
        eLabel: 'success'
    });

    beginFirefoxDownload();
}

function onTimeout() {
    // Make sure we only initiate the download once!
    clearTimeout(timeout);
    if (requestComplete) {
        return;
    }
    requestComplete = true;

    // Fire GA event to log attribution timeout
    window.dataLayer.push({
        event: 'non-interaction',
        eAction: 'direct-attribution',
        eLabel: 'timeout'
    });

    beginFirefoxDownload();
}

/**
 * If visitor already has a cookie, or does not meet the typical requirements fo
 * stub attribution, then we can start the download as normal. If requirements *are*
 * met and the visitor does *not* have a cookie, then attempt to make the attribution
 * call before starting the download.
 */
if (
    typeof Mozilla.StubAttribution !== 'undefined' &&
    Mozilla.StubAttribution.meetsRequirements() &&
    !Mozilla.StubAttribution.hasCookie()
) {
    // Wait for GA to load so that we can pass along visit ID.
    Mozilla.StubAttribution.waitForGoogleAnalytics(function () {
        const data = Mozilla.StubAttribution.getAttributionData();

        // make sure we check referrer for AMO (issue 11467)
        if (
            data &&
            Mozilla.StubAttribution.withinAttributionRate() &&
            Mozilla.StubAttribution.hasValidData(data)
        ) {
            Mozilla.StubAttribution.successCallback = onSuccess;
            Mozilla.StubAttribution.timeoutCallback = onTimeout;
            // We don't want to delay the download indefinitely for a stub attribution call,
            // so we only wait up to an additional 2 seconds (on top of GA) before downloading.
            timeout = setTimeout(onTimeout, 2000);
            Mozilla.StubAttribution.requestAuthentication(data);
        } else {
            beginFirefoxDownload();
        }
    });
} else {
    beginFirefoxDownload();
}

// Bug 1354334 - add a hint for test automation that page has loaded.
document.getElementsByTagName('html')[0].classList.add('download-ready');
