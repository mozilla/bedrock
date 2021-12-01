(function() {
    'use strict';

    /*
    *  Listings
    */

    /**
     * Take filter values in querystring and propogate to select inputs
    */
    function propogateQueryParamsToSelects() {
        var i;
        var j;
        var keyVal;
        var keyVals;
        var match;
        var qs = window.location.search;
        var select;
        var val;

        if (qs) {
            // drop the '?'
            qs = qs.slice(1);

            // split the querystring into key=val strings
            keyVals = qs.split('&');

            // for each key/value pair, update the associated select box
            for (i = 0; i < keyVals.length; i++) {
                keyVal = keyVals[i].split('=');

                // first index is the key, which, with an 'id_' prefix, matches the field id
                select = document.getElementById('id_' + keyVal[0]);

                // make sure the key is valid, then update the associated select box
                if (select) {
                    // (decodeURIComponent does not change '+' to ' ', hence the replace call)
                    val = decodeURIComponent(keyVal[1]).replace(/\+/gi, ' ');

                    // make sure select has an option matching the proposed value
                    // this ensures the select box doesn't get set to an empty value if
                    // e.g. there are no Intern positions available
                    for (j = 0; j < select.options.length; j++) {
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

    // init listings
    propogateQueryParamsToSelects();
})();
