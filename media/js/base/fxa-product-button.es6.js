/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const FxaProductButton = {};

const allowedList = [
    'https://accounts.firefox.com.cn/',
    'https://accounts.firefox.com/',
    'https://accounts.stage.mozaws.net/',
    'https://getpocket.com/',
    'https://guardian-dev.herokuapp.com/',
    'https://monitor.firefox.com/',
    'https://relay.firefox.com/',
    'https://stage.guardian.nonprod.cloudops.mozgcp.net/',
    'https://vpn.mozilla.org/'
];

let _buttons;

/**
 * Returns the hostname for a given URL.
 * @param {String} url.
 * @returns {String} hostname.
 */
FxaProductButton.getHostName = function (url) {
    const matches = url.match(/^https?:\/\/(?:[^/?#]+)(?:[/?#]|$)/i);
    return matches && matches[0];
};

/**
 * Get tokens from FxA for analytics purposes.
 * This is non-critical to the user flow.
 */
FxaProductButton.fetchTokens = function (buttons) {
    // assume the first button should dictate the metrics flow request
    const buttonURL = buttons[0].getAttribute('href');
    let metricsURL = buttons[0].getAttribute('data-action') + 'metrics-flow';

    // strip url to everything after `?`
    const buttonURLParams = buttonURL.match(/\?(.*)/)[1];

    // collect values from Fxa product button
    const params = window._SearchParams.queryStringToObject(buttonURLParams);

    // add required params to the token fetch request
    metricsURL += '?form_type=' + params.form_type;

    // add service identifier for VPN (issue #10811)
    if (params.service) {
        metricsURL += '&service=' + params.service;
    }

    metricsURL += '&entrypoint=' + params.entrypoint;
    metricsURL += '&utm_source=' + params.utm_source;

    // add optional utm params to the token fetch request
    if (params.utm_campaign) {
        metricsURL += '&utm_campaign=' + params.utm_campaign;
    }

    if (params.utm_content) {
        metricsURL += '&utm_content=' + params.utm_content;
    }

    if (params.utm_medium) {
        metricsURL += '&utm_medium=' + params.utm_medium;
    }

    if (params.utm_term) {
        metricsURL += '&utm_term=' + params.utm_term;
    }

    if (params.entrypoint_experiment) {
        metricsURL += '&entrypoint_experiment=' + params.entrypoint_experiment;
    }

    if (params.entrypoint_variation) {
        metricsURL += '&entrypoint_variation=' + params.entrypoint_variation;
    }

    return fetch(metricsURL)
        .then((resp) => {
            return resp.json();
        })
        .then((r) => {
            // add retrieved deviceID, flowBeginTime and flowId values to cta url
            let flowParams = '&device_id=' + r.deviceId;
            flowParams += '&flow_begin_time=' + r.flowBeginTime;
            flowParams += '&flow_id=' + r.flowId;
            return flowParams;
        })
        .catch(() => {
            // silently fail: deviceId, flowBeginTime, flowId are not added to url.
        });
};

/**
 * Attaches metrics flow parameters to FxA links.
 * @param {Object} Node List
 * @param {String} flowParams
 */
FxaProductButton.updateProductLinks = function (
    buttons,
    flowParams,
    overwrite
) {
    // if flowParams are undefined (e.g. blocked by CORS), then do nothing.
    if (!flowParams) {
        return;
    }

    // applies url to all buttons and adds cta position
    for (let i = 0; i < buttons.length; i++) {
        const href = buttons[i].href;
        const hostName = FxaProductButton.getHostName(href);
        // check if link is in the FxA referral allowedListDomains.
        if (hostName && allowedList.indexOf(hostName) !== -1) {
            // Only add flow params if they do not already exist,
            // unless `overwrite` is true.
            if (
                !overwrite &&
                href.indexOf('flow_id') === -1 &&
                href.indexOf('flow_begin_time') === -1 &&
                href.indexOf('device_id') === -1
            ) {
                buttons[i].href += flowParams;
            } else if (overwrite) {
                const buttonParams = window._SearchParams.queryStringToObject(
                    href.split('?')[1]
                );
                const updated =
                    window._SearchParams.queryStringToObject(flowParams);

                if (buttonParams.flow_id) {
                    buttonParams.flow_id = updated.flow_id;
                }

                if (buttonParams.flow_begin_time) {
                    buttonParams.flow_begin_time = updated.flow_begin_time;
                }

                if (buttonParams.device_id) {
                    buttonParams.device_id = updated.device_id;
                }

                const newParams =
                    window._SearchParams.objectToQueryString(buttonParams);

                buttons[i].href = `${href.split('?')[0]}?${newParams}`;
            }
        }
    }
};

FxaProductButton.isSupported = function () {
    return (
        'Promise' in window &&
        'fetch' in window &&
        typeof window._SearchParams !== 'undefined'
    );
};

FxaProductButton.init = function (overwrite) {
    // Do not overwrite existing flow params by default.
    const ow = typeof overwrite === 'boolean' ? overwrite : false;

    // Collect all Fxa product buttons
    _buttons = document.getElementsByClassName('js-fxa-product-button');

    if (!FxaProductButton.isSupported() || _buttons.length === 0) {
        return false;
    }

    return new window.Promise(function (resolve, reject) {
        if (_buttons.length) {
            FxaProductButton.fetchTokens(_buttons).then(function (flowParams) {
                FxaProductButton.updateProductLinks(_buttons, flowParams, ow);
                resolve(flowParams);
            });
        } else {
            reject();
        }
    });
};

export default FxaProductButton;
