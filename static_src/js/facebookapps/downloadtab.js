// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

// Main function
// Calls App class
(function (singleton, $, win) {
    singleton.app = new singleton.classes.App($, win);
    singleton.app.startApp();
} (DOWNLOADTAB, jQuery, window));
