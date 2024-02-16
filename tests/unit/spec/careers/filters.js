/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

import PositionFilters from '../../../../media/js/careers/listings/filters.es6.js';

describe('filters.js', function () {
    beforeEach(function () {
        const form = `<form id="listings-filters" class="hide-from-legacy-ie">
            <div class="listings-filter listings-filter-location">
                <select name="location" required="" id="id_location">
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
                </select>
                <label for="id_location" class="visually-hidden">Location</label>
            </div>
            <input type="hidden" id="id_position_type" name="position_type" value="">
            <div class="listings-filter listings-filter-name">
                <select name="team" autocomplete="off" required="" id="id_team">
                    <option value="" selected="">All Teams</option>
                    <option value="Business Development">Business Development</option>
                    <option value="Core Product-Firefox">Core Product-Firefox</option>
                    <option value="Core Product-Security">Core Product-Security</option>
                    <option value="Data Organization">Data Organization</option>
                    <option value="IT">IT</option>
                    <option value="Marketing">Marketing</option>
                    <option value="Mozilla Foundation">Mozilla Foundation</option>
                    <option value="People &amp; Organizational Development">People &amp; Organizational Development</option>
                </select>
                <label for="id_team" class="visually-hidden">Team</label>
            </div>
        </form>`;

        const table = `<table class="listings-positions" id="listings-positions">
            <thead>
            <tr>
                <th class="title" scope="col"><h4>Job Title</h4></th>
                <th class="location" scope="col"><h4>Location</h4></th>
                <th class="name" scope="col"><h4>Team</h4></th>
            </tr>
            </thead>
            <tbody>
            <tr class="position" data-team="Business Development" data-type="" data-location="San Francisco Office">
                <td class="title"><a href="#">Operations Specialist - Business Development</a></td>
                <td class="location">San Francisco Office</td>
                <td class="name">Business Development</td>
            </tr>
            <tr class="position" data-team="Core Product-Firefox" data-type="" data-location="Remote San Francisco Bay Area">
                <td class="title"><a href="#"> Localization Program Manager </a></td>
                <td class="location">Remote San Francisco Bay Area</td>
                <td class="name">Core Product-Firefox</td>
            </tr>
            <tr class="position" data-team="Core Product-Firefox" data-type="" data-location="Remote Canada">
                <td class="title"><a href="#">Senior Program Manager</a></td>
                <td class="location">Remote Canada</td>
                <td class="name">Core Product-Firefox</td>
            </tr>
            <tr class="position" data-team="Core Product-Security" data-type="" data-location="Remote US">
                <td class="title"><a href="#">Senior Software Engineer (C++)</a></td>
                <td class="location">Remote US</td>
                <td class="name">Core Product-Security</td>
            </tr>
            <tr class="position" data-team="Core Product-Security" data-type="" data-location="San Francisco Office">
                <td class="title"><a href="#">Senior UI Engineer</a></td>
                <td class="location">San Francisco Office</td>
                <td class="name">Core Product-Security</td>
            </tr>
            <tr class="position" data-team="Data Organization" data-type="" data-location="Remote Canada,Remote Germany,Remote US">
                <td class="title"><a href="#">Data Engineer</a></td>
                <td class="location">Remote Canada, Remote Germany, Remote US</td>
                <td class="name">Data Organization</td>
            </tr>
            <tr class="position" data-team="Data Organization" data-type="" data-location="Remote Canada,Remote US">
                <td class="title"><a href="#">Inference Data Scientist (Staff Level)</a></td>
                <td class="location">Remote Canada, Remote US</td>
                <td class="name">Data Organization</td>
            </tr>
            <tr class="position" data-team="Mozilla Foundation" data-type="" data-location="Remote">
                <td class="title"><a href="#">Senior Software Engineer</a></td>
                <td class="location">Remote</td>
                <td class="name">Mozilla Foundation</td>
            </tr>
            <tr class="empty-filter-message hidden" id="empty-filter-message">
                <td colspan="4">
                <p>No jobs found that match the selected filters.</p>
                </td>
            </tr>
            </tbody>
        </table>`;

        document.body.insertAdjacentHTML('beforeend', form);
        document.body.insertAdjacentHTML('beforeend', table);

        const inputs = document.getElementById('listings-filters').elements;
        const filters = new PositionFilters(
            inputs.position_type,
            inputs.team,
            inputs.location,
            document.getElementById('listings-positions')
        );
        filters.bindEvents();
    });

    afterEach(function () {
        const form = document.getElementById('listings-filters');
        form.parentNode.removeChild(form);

        const table = document.getElementById('listings-positions');
        table.parentNode.removeChild(table);
    });

    it('should filter the table based on selected location', function () {
        const location = document.getElementById('id_location');
        const evt = new CustomEvent('change');
        location.value = 'Remote US';
        location.dispatchEvent(evt);

        expect(
            document.querySelectorAll(
                '.listings-positions tbody tr.position:not(.hidden)'
            ).length
        ).toEqual(4);
    });

    it('should filter the table based on selected team', function () {
        const team = document.getElementById('id_team');
        const evt = new CustomEvent('change');
        team.value = 'Core Product-Firefox';
        team.dispatchEvent(evt);

        expect(
            document.querySelectorAll(
                '.listings-positions tbody tr.position:not(.hidden)'
            ).length
        ).toEqual(2);
    });

    it('should filter the table based on both location and team', function () {
        const evt = new CustomEvent('change');
        const location = document.getElementById('id_location');
        const team = document.getElementById('id_team');

        location.value = 'Remote US';
        location.dispatchEvent(evt);

        team.value = 'Core Product-Security';
        team.dispatchEvent(evt);

        expect(
            document.querySelectorAll(
                '.listings-positions tbody tr.position:not(.hidden)'
            ).length
        ).toEqual(1);
    });

    it('should display a message if no matching jobs are found', function () {
        const location = document.getElementById('id_location');
        const evt = new CustomEvent('change');
        location.value = 'Toronto Office';
        location.dispatchEvent(evt);

        const message = document.querySelector(
            '.listings-positions tbody tr.empty-filter-message'
        );

        expect(message.classList.contains('hidden')).toBeFalsy();
    });

    it('should display all jobs and locations when filters are unset', function () {
        const evt = new CustomEvent('change');
        const location = document.getElementById('id_location');
        const team = document.getElementById('id_team');

        location.value = 'Remote US';
        location.dispatchEvent(evt);

        team.value = 'Core Product-Security';
        team.dispatchEvent(evt);

        expect(
            document.querySelectorAll(
                '.listings-positions tbody tr.position:not(.hidden)'
            ).length
        ).toEqual(1);

        location.value = 'All Locations';
        location.dispatchEvent(evt);

        team.value = 'All Teams';
        team.dispatchEvent(evt);

        expect(
            document.querySelectorAll(
                '.listings-positions tbody tr.position:not(.hidden)'
            ).length
        ).toEqual(8);
    });
});
