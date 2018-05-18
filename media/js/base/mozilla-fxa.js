/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Depends on Mozilla-client.js
// adds classes to the body to indicate state of fxaccount

// Create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function(Mozilla) {
    'use strict';

    var FxaState = {
        body: document.getElementsByTagName('body')[0],
        defaultStateClass : 'state-fxa-default', // only present if added manually to page in HTML
    };

    FxaState.getStateClassAndDo = function(callback) {
        Mozilla.Client.getFxaDetails(function(details) {
            FxaState.convertFxaDetailsToStateAndDo(details, callback);
        });
    };

    FxaState.convertFxaDetailsToStateAndDo = function(details, callback) {
        var stateClass = '';

        if(details.firefox) {
            if(details.legacy) {
                stateClass = 'state-fxa-unsupported';
            } else if(details.mobile) {
                if(details.mobile === 'ios') {
                    stateClass = 'state-fxa-ios';
                } else {
                    stateClass = 'state-fxa-android';
                }
            } else {
                if(details.setup) {
                    stateClass = 'state-fxa-supported-signed-in';
                } else {
                    stateClass = 'state-fxa-supported-signed-out';
                }
            }
        } else {
            stateClass = 'state-fxa-not-fx';
        }
        callback(stateClass);
    };

    FxaState.applyStateToBody = function(stateClass) {
        FxaState.body.classList.remove(FxaState.defaultStateClass);
        FxaState.body.classList.add(stateClass);
    };

    Mozilla.FxaState = FxaState;

})(window.Mozilla);
