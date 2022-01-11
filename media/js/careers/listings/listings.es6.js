/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import propogateQueryParamsToSelects from './params.es6.js';
import PositionFilters from './filters.es6.js';

// Take filter values in querystring and propogate to select inputs.
propogateQueryParamsToSelects();

const inputs = document.getElementById('listings-filters').elements;
const filters = new PositionFilters(
    inputs.position_type,
    inputs.team,
    inputs.location,
    document.getElementById('listings-positions')
);
filters.bindEvents();

// Trigger sorting on initial load for querystring arguments.
filters.onFilterChange();
