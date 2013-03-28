// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

// Init function
// Grabs server init data from #init-data element
;(function ($) {
    // App's singleton object
    DOWNLOADTAB = {};
    DOWNLOADTAB.classes = {};
    DOWNLOADTAB.initData = $('#init-data').data();
} (jQuery));
