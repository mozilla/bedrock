/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * Initialize main Navigation.
 */

import MzpNavigation from './m24-navigation.es6';
import MzpMenu from './m24-menu.es6';

// add both components to window as this is needed for MzpNavigation.checkScrollPosition()
window.MzpMenu = MzpMenu;
window.MzpNavigation = MzpNavigation;

MzpMenu.init();
MzpNavigation.init();
