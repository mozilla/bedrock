/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

var CollusionAddon = (function() {
  var self = {
    isInstalled: function() {
      return ('onGraph' in window);
    },
    onGraph: window.onGraph,
    importGraph: window.importGraph,
    resetGraph: window.resetGraph,
    saveGraph: window.saveGraph,
    getSavedGraph: window.getSavedGraph
  };
  
  return self;
})();
