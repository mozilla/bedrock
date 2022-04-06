/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import AffiliateAttribution from './affiliate-attribution.es6';

const notification = document.querySelector('.vpn-affiliate-notification');

function bindNotificationEvents() {
    if (notification) {
        notification
            .querySelector('.vpn-affiliate-notification-ok')
            .addEventListener('click', handleOkClick, false);

        notification
            .querySelector('.vpn-affiliate-notification-reject')
            .addEventListener('click', handleOptOutClick, false);

        notification
            .querySelector('.mzp-c-notification-bar-button')
            .addEventListener('click', handleCloseNotification, false);
    }
}

function unbindNotificationEvents() {
    if (notification) {
        notification
            .querySelector('.vpn-affiliate-notification-ok')
            .removeEventListener('click', handleOkClick, false);

        notification
            .querySelector('.vpn-affiliate-notification-reject')
            .removeEventListener('click', handleOptOutClick, false);

        notification
            .querySelector('.mzp-c-notification-bar-button')
            .removeEventListener('click', handleCloseNotification, false);
    }
}

function handleOptOutClick(e) {
    e.preventDefault();

    unbindNotificationEvents();
    AffiliateAttribution.optOut()
        .then(() => {
            notification.classList.remove('show');
            unbindNotificationEvents();

            window.dataLayer.push({
                eLabel: 'Banner Click (Reject)',
                'data-banner-name': 'VPN affiliate notification',
                'data-banner-click': '1',
                event: 'in-page-interaction'
            });
        })
        .catch((e) => {
            throw new Error(e);
        });
}

function handleOkClick(e) {
    e.preventDefault();
    AffiliateAttribution.setPreferenceCookie('accept');
    notification.classList.remove('show');
    unbindNotificationEvents();

    window.dataLayer.push({
        eLabel: 'Banner Click (OK)',
        'data-banner-name': 'VPN affiliate notification',
        'data-banner-click': '1',
        event: 'in-page-interaction'
    });
}

function handleCloseNotification(e) {
    e.preventDefault();
    AffiliateAttribution.setPreferenceCookie('accept');
    notification.classList.remove('show');
    unbindNotificationEvents();

    window.dataLayer.push({
        eLabel: 'Banner Dismissal',
        'data-banner-name': 'VPN affiliate notification',
        'data-banner-dismissal': '1',
        event: 'in-page-interaction'
    });
}

function showOptOutNotification() {
    const notification = document.querySelector('.vpn-affiliate-notification');

    if (notification) {
        notification.classList.add('show');
        bindNotificationEvents();

        window.dataLayer.push({
            eLabel: 'Banner Impression',
            'data-banner-name': 'VPN affiliate notification',
            'data-banner-impression': '1',
            event: 'non-interaction'
        });
    }
}

// Only initiate the affiliate attribution flow If there's not an opt-out cookie set.
if (AffiliateAttribution.shouldInitiateAttributionFlow()) {
    AffiliateAttribution.init()
        .then(() => {
            // If there's a CJ event param in the URL, or there's a marketing cookie
            // already set, then show the opt-out notification.
            if (AffiliateAttribution.shouldShowOptOutNotification()) {
                showOptOutNotification();
            }
        })
        .catch((e) => {
            throw new Error(e);
        });
} else {
    // Just add flow params as normal.
    AffiliateAttribution.addFlowParams();
}
