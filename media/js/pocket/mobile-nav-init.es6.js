/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import {
    mobileMenuQuery,
    init,
    addMediaQueryListeners
} from './mobile-nav.es6';

if (mobileMenuQuery.matches) {
    init();
} else {
    addMediaQueryListeners();
}
