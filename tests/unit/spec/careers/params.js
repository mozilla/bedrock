/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

import propogateQueryParamsToSelects from '../../../../media/js/careers/listings/params.es6.js';

describe('params.js', function () {
    beforeEach(function () {
        const location = `<select name="location" required="" id="id_location">
            <option value="" selected="">All Locations</option>
            <option value="Berlin Office">Berlin Office</option>
            <option value="Portland Office">Portland Office</option>
            <option value="Remote">Remote</option>
            <option value="Remote Canada">Remote Canada</option>
            <option value="Remote France">Remote France</option>
            <option value="Remote Germany">Remote Germany</option>
            <option value="Remote San Francisco Bay Area">Remote San Francisco Bay Area</option>
            <option value="Remote UK">Remote UK</option>
            <option value="Remote US">Remote US</option>
            <option value="San Francisco Office">San Francisco Office</option>
            <option value="Toronto Office">Toronto Office</option>
        </select>`;

        const team = `<select name="team" required="" id="id_team">
            <option value="" selected="">All Teams</option>
            <option value="Business Development">Business Development</option>
            <option value="Core Product-Firefox">Core Product-Firefox</option>
            <option value="Core Product-Security">Core Product-Security</option>
            <option value="Data Organization">Data Organization</option>
            <option value="IT">IT</option>
            <option value="Marketing">Marketing</option>
            <option value="Mozilla Foundation">Mozilla Foundation</option>
            <option value="People &amp; Organizational Development">People &amp; Organizational Development</option>
        </select>`;

        document.body.insertAdjacentHTML('beforeend', location);
        document.body.insertAdjacentHTML('beforeend', team);
    });

    afterEach(function () {
        const location = document.getElementById('id_location');
        location.parentNode.removeChild(location);

        const team = document.getElementById('id_team');
        team.parentNode.removeChild(team);
    });

    it('should select location based on query param value', function () {
        const select = document.getElementById('id_location');

        propogateQueryParamsToSelects('?location=Berlin%20Office');
        expect(select.options[select.selectedIndex].value).toEqual(
            'Berlin Office'
        );

        propogateQueryParamsToSelects('?location=Remote%20UK');
        expect(select.options[select.selectedIndex].value).toEqual('Remote UK');
    });

    it('should select team based on query param value', function () {
        const select = document.getElementById('id_team');

        propogateQueryParamsToSelects('?team=Core%20Product-Firefox');
        expect(select.options[select.selectedIndex].value).toEqual(
            'Core Product-Firefox'
        );

        propogateQueryParamsToSelects('?team=Marketing');
        expect(select.options[select.selectedIndex].value).toEqual('Marketing');
    });

    it('should handle multiple parameters', function () {
        const location = document.getElementById('id_location');
        const team = document.getElementById('id_team');

        propogateQueryParamsToSelects(
            '?team=Core%20Product-Firefox&location=Berlin%20Office'
        );

        expect(location.options[location.selectedIndex].value).toEqual(
            'Berlin Office'
        );

        expect(team.options[team.selectedIndex].value).toEqual(
            'Core Product-Firefox'
        );
    });

    it('should no nothing if a corresponding input is not found', function () {
        const location = document.getElementById('id_location');
        const team = document.getElementById('id_team');

        propogateQueryParamsToSelects('?position_type=Intern');

        expect(location.options[location.selectedIndex].value).toEqual('');
        expect(team.options[team.selectedIndex].value).toEqual('');
    });

    it('should do nothing is a corresponding value is not found', function () {
        const location = document.getElementById('id_location');
        const team = document.getElementById('id_team');

        propogateQueryParamsToSelects('?location=nowhere');
        propogateQueryParamsToSelects('?team=thedude');

        expect(location.options[location.selectedIndex].value).toEqual('');
        expect(team.options[team.selectedIndex].value).toEqual('');
    });
});
