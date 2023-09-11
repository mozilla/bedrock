/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

function handleScanEmail(e) {
    e.preventDefault();

    const form = e.target;
    const action = form.getAttribute('action');
    const data = new FormData(form);
    const email = data.get('email');
    const location = `${action}#email=${encodeURIComponent(email)}`;
    const formPosition = form.getAttribute('data-form-position');
    const position = formPosition ? formPosition : 'primary';

    window.dataLayer.push({
        event: 'in-page-interaction',
        eAction: 'Monitor form submit',
        eLabel: `Get free scan (${position})`
    });

    window.location.href = location;
}

function initFormScan() {
    const scanForm = document.querySelectorAll('.c-scan-form');

    for (let i = 0; i < scanForm.length; i++) {
        scanForm[i].addEventListener('submit', handleScanEmail, false);
    }
}

initFormScan();
