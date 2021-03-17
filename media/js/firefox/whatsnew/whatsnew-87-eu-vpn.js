/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var lang = document.getElementsByTagName('html')[0].getAttribute('lang');
    var locales = ['de', 'fr'];
    var countrySelect = document.getElementById('id_country');

    function setSelectedCountry(id, options) {
        for (var i = 0; i < options.length; i++) {
            if (options[i].value === id) {
                options[i].selected = 'selected';
                break;
            }
        }
    }

    // Pre select France / Germany in country drop down for respective locales.
    if (lang && countrySelect && locales.includes(lang)) {
        setSelectedCountry(lang, countrySelect.options);
    }

})(window.Mozilla);
