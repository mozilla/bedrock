/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/**
 * Monitors inputs and filters a list of positions when they change.
 */
function PositionFilters(typeInput, teamInput, locationInput, positionTable) {
    this.typeInput = typeInput;
    this.teamInput = teamInput;
    this.locationInput = locationInput;
    this.positionTable = positionTable;
    this.emptyFilterMessage = document.getElementById('empty-filter-message');
}

PositionFilters.prototype = {
    /**
     * Bind onFilterChange to the change events for each input.
     */
    bindEvents: function () {
        const self = this;
        const callback = function () {
            self.onFilterChange();
        };

        this.typeInput.addEventListener('change', callback);
        this.teamInput.addEventListener('change', callback);
        this.locationInput.addEventListener('change', callback);
    },

    /**
     * When a filter changes, refresh the position list.
     */
    onFilterChange: function () {
        // collection of tr.position elements
        const positions = this.positionTable.getElementsByClassName('position');
        let positionsVisible = false;
        let querystring = '';

        const filters = {
            position_type: this.typeInput.value,
            team: this.teamInput.value,
            location: this.locationInput.value
        };

        // Hide table and show all positions.
        this.positionTable.classList.add('hidden');
        this.emptyFilterMessage.classList.add('hidden');

        for (let i = 0; i < positions.length; i++) {
            positions.item(i).classList.remove('hidden');
        }

        // Hide positions that don't match the current filters.
        this.filterPositions('type', filters['position_type']);
        this.filterPositions('team', filters['team']);
        this.filterLocations(filters['location']);

        // If there aren't any positions being shown, show the no-results message.
        for (let j = 0; j < positions.length; j++) {
            if (!positions.item(j).classList.contains('hidden')) {
                positionsVisible = true;
                break;
            }
        }

        if (!positionsVisible) {
            this.emptyFilterMessage.classList.remove('hidden');
        }

        // Get rid of unset filters.
        for (const k in filters) {
            if (
                Object.prototype.hasOwnProperty.call(filters, k) &&
                !filters[k]
            ) {
                delete filters[k];
            }
        }

        // Build a querystring from populated filters.
        for (const prop in filters) {
            querystring += prop + '=' + filters[prop];
        }

        // Preserve Google Analytics parameters.
        const ga_parameters = window.location.search
            .substr(1)
            .split('&')
            .filter(function (parameter) {
                return parameter.indexOf('utm_') === 0;
            });

        if (querystring.length && ga_parameters.length) {
            querystring += '&';
        }

        querystring += ga_parameters.join('&');

        if (querystring.length) {
            querystring = '?' + querystring;
        }

        // Replace history state with this filtered state.
        window.history.replaceState(
            filters,
            'Filtered',
            location.pathname + querystring
        );

        this.positionTable.classList.remove('hidden');
    },

    /**
     * Hide any positions that do have the correct value for the given field.
     */
    filterPositions: function (field, value) {
        if (!value) return;

        const positions = this.positionTable.getElementsByClassName('position');

        for (let i = 0; i < positions.length; i++) {
            const data = positions.item(i).dataset[field];

            if (data.indexOf(value) === -1) {
                positions.item(i).classList.add('hidden');
            }
        }
    },

    filterLocations: function (value) {
        // Note that filtering is based on a data attr, but the position's
        // location shown in the HTML may be different to (or contain _more_
        // items than) the data attribute's value.
        if (!value) return;

        const positions = this.positionTable.getElementsByClassName('position');

        for (let i = 0; i < positions.length; i++) {
            const data = positions.item(i).dataset.location + ',';

            // When user selects 'Remote' only list jobs explicitly marked
            // Remote otherwise list jobs matching value (which is a mozilla
            // office) and those marked as 'All Offices'
            if (value === 'Remote') {
                if (data.indexOf(value + ',') === -1) {
                    positions.item(i).classList.add('hidden');
                }
            } else if (value.indexOf('Remote') !== -1 && data === 'Remote,') {
                continue;
            } else if (
                data.indexOf(value + ',') === -1 &&
                data.indexOf('All Offices,') === -1
            ) {
                positions.item(i).classList.add('hidden');
            }
        }
    }
};

export default PositionFilters;
