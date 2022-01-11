/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * Take filter values in querystring and propogate to select inputs
 */
function propogateQueryParamsToSelects(query) {
    let keyVals;
    let match;
    let qs = typeof query !== 'undefined' ? query : window.location.search;
    let select;

    if (qs) {
        // drop the '?'
        qs = qs.slice(1);

        // split the querystring into key=val strings
        keyVals = qs.split('&');

        // for each key/value pair, update the associated select box
        for (let i = 0; i < keyVals.length; i++) {
            const keyVal = keyVals[i].split('=');

            // first index is the key, which, with an 'id_' prefix, matches the field id
            select = document.getElementById('id_' + keyVal[0]);

            // make sure the key is valid, then update the associated select box
            if (select && select.nodeName === 'SELECT') {
                // (decodeURIComponent does not change '+' to ' ', hence the replace call)
                const val = decodeURIComponent(keyVal[1]).replace(/\+/gi, ' ');

                // make sure select has an option matching the proposed value
                // this ensures the select box doesn't get set to an empty value if
                // e.g. there are no Intern positions available
                for (let j = 0; j < select.options.length; j++) {
                    if (select.options[j].value === val) {
                        match = true;
                        break;
                    }
                }

                if (match) {
                    select.value = val;
                }
            }
        }
    }
}

export default propogateQueryParamsToSelects;
