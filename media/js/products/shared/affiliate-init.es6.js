/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import AffiliateAttribution from './affiliate-attribution.es6';

const notification = document.querySelector('.affiliate-notification');

function bindNotificationEvents() {
    if (notification) {
        notification
            .querySelector('.affiliate-notification-ok')
            .addEventListener('click', handleOkClick, false);

        notification
            .querySelector('.affiliate-notification-reject')
            .addEventListener('click', handleOptOutClick, false);

        notification
            .querySelector('.mzp-c-notification-bar-button')
            .addEventListener('click', handleCloseNotification, false);
    }
}

function unbindNotificationEvents() {
    if (notification) {
        notification
            .querySelector('.affiliate-notification-ok')
            .removeEventListener('click', handleOkClick, false);

        notification
            .querySelector('.affiliate-notification-reject')
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

            // UA
            window.dataLayer.push({
                eLabel: 'Banner Click (Reject)',
                'data-banner-name': 'Affiliate notification',
                'data-banner-click': '1',
                event: 'in-page-interaction'
            });
            // GA4
            window.dataLayer.push({
                event: 'widget_action',
                type: 'affiliate notification',
                action: 'reject'
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

    // UA
    window.dataLayer.push({
        eLabel: 'Banner Click (OK)',
        'data-banner-name': 'Affiliate notification',
        'data-banner-click': '1',
        event: 'in-page-interaction'
    });
    // GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'affiliate notification',
        action: 'accept'
    });
}

function handleCloseNotification(e) {
    e.preventDefault();
    AffiliateAttribution.setPreferenceCookie('accept');
    notification.classList.remove('show');
    unbindNotificationEvents();

    // UA
    window.dataLayer.push({
        eLabel: 'Banner Dismissal',
        'data-banner-name': 'Affiliate notification',
        'data-banner-dismissal': '1',
        event: 'in-page-interaction'
    });
    // GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'affiliate notification',
        action: 'dismiss'
    });
}

function showOptOutNotification() {
    const notification = document.querySelector('.affiliate-notification');

    if (notification) {
        notification.classList.add('show');
        bindNotificationEvents();

        // UA
        window.dataLayer.push({
            eLabel: 'Banner Impression',
            'data-banner-name': 'Affiliate notification',
            'data-banner-impression': '1',
            event: 'non-interaction'
        });
        // GA4
        window.dataLayer.push({
            event: 'widget_action',
            type: 'affiliate notification',
            action: 'impression',
            non_interaction: true
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
            console.error(e); // eslint-disable-line no-console
        });
} else {
    // Just add flow params as normal.
    AffiliateAttribution.addFlowParams();
}
