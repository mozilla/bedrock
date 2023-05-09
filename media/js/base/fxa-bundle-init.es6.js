/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import FxaLink from './fxa-link.es6.js';
import FxaAttribution from './fxa-attribution.es6.js';

const urlParams = new window._SearchParams();

// Track external URL parameter referrals for Firefox Account links.
FxaAttribution.init(urlParams.params);

// Configure Firefox Account links for Sync on desktop.
FxaLink.init();
