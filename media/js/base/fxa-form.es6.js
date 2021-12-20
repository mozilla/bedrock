/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const FxaForm = {};

let formElem;
let email;
let entrypointInput;
let entrypointExp;
let entrypointVar;
let utmCampaign;
let utmContent;
let utmSource;
let utmTerm;

const utms = [
    'utm_source',
    'utm_campaign',
    'utm_content',
    'utm_term',
    'utm_medium'
];

const fxaParams = [
    'device_id',
    'flow_id',
    'flow_begin_time',
    'entrypoint_experiment',
    'entrypoint_variation'
];

const acceptedParams = utms.concat(fxaParams);

/**
 * Creates a hidden form input.
 * @param name {String} input name.
 * @param value (String) input value.
 * @returns HTML element.
 */
FxaForm.createInput = function (name, value) {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;
    return input;
};

/**
 * Fetch and validate accepted params from the page URL for FxA referral.
 * https://mozilla.github.io/ecosystem-platform/docs/relying-parties/metrics-for-relying-parties#metrics-related-query-parameters
 * @returns {Object} if params are valid, else {null}.
 */
FxaForm.getAttributionData = function (params) {
    const allowedChars = /^[\w/.%-]+$/;
    const finalParams = {};

    for (let i = 0; i < acceptedParams.length; i++) {
        const acceptedParam = acceptedParams[i];
        if (Object.prototype.hasOwnProperty.call(params, acceptedParam)) {
            try {
                const foundParam = decodeURIComponent(params[acceptedParam]);
                if (allowedChars.test(foundParam)) {
                    finalParams[acceptedParam] = foundParam;
                }
            } catch (e) {
                // silently drop malformed parameter values (issue #10897)
            }
        }
    }

    // Both utm_source and utm_campaign are considered required, so only pass through referral data if they exist.
    // Alternatively, pass through entrypoint_experiment and entrypoint_variation independently.
    if (
        (Object.prototype.hasOwnProperty.call(finalParams, 'utm_source') &&
            Object.prototype.hasOwnProperty.call(
                finalParams,
                'utm_campaign'
            )) ||
        (Object.prototype.hasOwnProperty.call(
            finalParams,
            'entrypoint_experiment'
        ) &&
            Object.prototype.hasOwnProperty.call(
                finalParams,
                'entrypoint_variation'
            ))
    ) {
        return finalParams;
    }

    return null;
};

/**
 * Pass through utm_params from URL if present,
 * to attribute external marketing campaigns.
 *
 * @returns {Object} of utm parameters
 */
FxaForm.getUTMParams = function () {
    const urlParams = new window._SearchParams().utmParams();
    return FxaForm.getAttributionData(urlParams) || {};
};

/**
 * Get tokens from FxA for analytics purposes.
 * This is non-critical to the user flow.
 */
FxaForm.fetchTokens = function () {
    let destURL = formElem.getAttribute('action') + 'metrics-flow';

    // add required params to the token fetch request
    destURL += '?form_type=email';
    destURL += '&entrypoint=' + entrypointInput.value;
    destURL += '&utm_source=' + utmSource.value;

    if (utmContent) {
        destURL += '&utm_content=' + utmContent.value;
    }

    if (utmCampaign) {
        destURL += '&utm_campaign=' + utmCampaign.value;
    }

    if (utmTerm) {
        destURL += '&utm_term=' + utmTerm.value;
    }

    if (entrypointExp) {
        destURL += '&entrypoint_experiment=' + entrypointExp.value;
    }

    if (entrypointVar) {
        destURL += '&entrypoint_variation=' + entrypointVar.value;
    }

    return fetch(destURL)
        .then((resp) => {
            return resp.json();
        })
        .then((r) => {
            formElem.querySelector('[name="device_id"]').value = r.deviceId;
            formElem.querySelector('[name="flow_id"]').value = r.flowId;
            formElem.querySelector('[name="flow_begin_time"]').value =
                r.flowBeginTime;
        })
        .catch(() => {
            // silently fail, leaving flow_id and flow_begin_time as default empty value
        });
};

/**
 * Intercept event handler for FxA forms, lets the browser drive the FxA Flow using
 * the `showFirefoxAccounts` UITour API. Attaches several UTM parameters from the current page
 * that will be forwarded to the browser and later on to FxA services.
 * @param event {Event}
 * @private
 */
FxaForm.interceptFxANavigation = function (event) {
    event.preventDefault();
    const extraURLParams = FxaForm.getUTMParams();

    let entrypoint = null;
    if (entrypointInput && entrypointInput.value) {
        entrypoint = entrypointInput.value;
    }
    if (entrypointExp && entrypointExp.value) {
        extraURLParams['entrypoint_experiment'] = entrypointExp.value;
    }
    if (entrypointVar && entrypointVar.value) {
        extraURLParams['entrypoint_variation'] = entrypointVar.value;
    }

    if (email) {
        email = email.value;
    }

    if (formElem) {
        const deviceId = formElem.querySelector('[name="device_id"]');
        const flowId = formElem.querySelector('[name="flow_id"]');
        const flowBeginTime = formElem.querySelector(
            '[name="flow_begin_time"]'
        );
        if (deviceId && deviceId.value) {
            extraURLParams['device_id'] = deviceId.value;
        }
        if (flowId && flowId.value) {
            extraURLParams['flow_id'] = flowId.value;
        }
        if (flowBeginTime && flowBeginTime.value) {
            extraURLParams['flow_begin_time'] = parseInt(
                flowBeginTime.value,
                10
            );
        }
    }
    return Mozilla.UITour.showFirefoxAccounts(
        extraURLParams,
        entrypoint,
        email
    );
};

/**
 * Configures Sync for Firefox browsers.
 */
FxaForm.setServiceContext = function () {
    const contextField = formElem.querySelector('[name="context"]');
    const userVer = parseFloat(Mozilla.Client._getFirefoxVersion());
    const useUITourForFxA =
        userVer >= 80 && typeof Mozilla.UITour !== 'undefined';

    if (useUITourForFxA) {
        // context is required for all Firefox desktop clients.
        if (!contextField) {
            const context = FxaForm.createInput('context', 'fx_desktop_v3');
            formElem.appendChild(context);
        }

        Mozilla.UITour.ping(() => {
            // intercept the flow and submit the form using the UITour API.
            formElem.addEventListener('submit', FxaForm.interceptFxANavigation);
        });
    }
};

FxaForm.isSupported = function () {
    return 'Promise' in window && 'fetch' in window;
};

FxaForm.init = function () {
    if (!FxaForm.isSupported()) {
        return false;
    }

    formElem = document.getElementById('fxa-email-form');
    email = document.getElementById('fxa-email-field');
    entrypointInput = document.getElementById('fxa-email-form-entrypoint');
    entrypointExp = document.getElementById(
        'fxa-email-form-entrypoint-experiment'
    );
    entrypointVar = document.getElementById(
        'fxa-email-form-entrypoint-variation'
    );
    utmCampaign = document.getElementById('fxa-email-form-utm-campaign');
    utmContent = document.getElementById('fxa-email-form-utm-content');
    utmSource = document.getElementById('fxa-email-form-utm-source');
    utmTerm = document.getElementById('fxa-email-form-utm-term');

    return new window.Promise((resolve, reject) => {
        if (formElem) {
            // Pass through UTM params from the URL to the form.
            const utms = FxaForm.getUTMParams();
            Object.keys(utms).forEach((i) => {
                // check if input is available
                if (formElem.querySelector('[name="' + i + '"]')) {
                    formElem.querySelector('[name="' + i + '"]').value =
                        utms[i];
                } else {
                    // create input if one is not present
                    const input = FxaForm.createInput(i, utms[i]);
                    formElem.appendChild(input);
                }
            });

            FxaForm.fetchTokens().then(() => {
                // Configure Sync for Firefox desktop browsers.
                if (Mozilla.Client._isFirefoxDesktop()) {
                    FxaForm.setServiceContext();
                }
                resolve();
            });
        } else {
            reject();
        }
    });
};

export default FxaForm;
