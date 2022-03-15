/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    // TODO port this JS to Protocol
    // multi-newsletter signup allowed since issue #11120

    const newsletterForm = document.getElementById('newsletter-form');

    if (!newsletterForm) {
        return;
    }

    // handle errors
    let errorArray = [];
    let newsletterErrors = document.getElementById('newsletter-errors');
    const newsletterContent = document.querySelector(
        '.mzp-c-newsletter-content'
    );

    function disableFormFields() {
        const formFields = newsletterForm.querySelectorAll('input, select');

        for (let i = 0; i < formFields.length; i++) {
            formFields[i].disabled = true;
        }
    }

    function enableFormFields() {
        const formFields = newsletterForm.querySelectorAll('input, select');

        for (let i = 0; i < formFields.length; i++) {
            formFields[i].disabled = false;
        }
    }

    function newsletterError() {
        enableFormFields();

        if (errorArray.length) {
            // create error list container if it does not exist.
            if (!newsletterErrors) {
                newsletterErrors = document.createElement('div');
                newsletterErrors.id = 'newsletter-errors';
                newsletterErrors.className = 'mzp-c-form-errors';
                newsletterContent.insertBefore(
                    newsletterErrors,
                    newsletterContent.firstChild
                );
            }

            const errorList = document.createElement('ul');

            for (let i = 0; i < errorArray.length; i++) {
                const item = document.createElement('li');
                item.appendChild(document.createTextNode(errorArray[i]));
                errorList.appendChild(item);
            }

            newsletterErrors.appendChild(errorList);
            newsletterErrors.style.display = 'block';
        } else {
            // no error messages, forward to server for better troubleshooting
            newsletterForm.setAttribute('data-skip-xhr', true);
            newsletterForm.submit();
        }
    }

    // show sucess message
    function newsletterThanks() {
        const thanks = document.getElementById('newsletter-thanks');

        // show thanks message
        thanks.style.display = 'block';
    }

    // trigger success event
    function newsletterSuccess() {
        if (typeof document.CustomEvent === 'function') {
            document.dispatchEvent(
                new CustomEvent('newsletterSuccess', {
                    bubbles: true,
                    cancelable: true
                })
            );
        } else if (typeof document.createEvent === 'function') {
            const event = document.createEvent('Event');
            event.initEvent('newsletterSuccess', true, true);
            document.dispatchEvent(event);
        }
    }

    // XHR subscribe; handle errors; display thanks message on success.
    function newsletterSubscribe(evt) {
        const skipXHR = newsletterForm.getAttribute('data-skip-xhr');
        if (skipXHR) {
            return true;
        }
        evt.preventDefault();
        evt.stopPropagation();

        // new submission, clear old errors
        errorArray = [];

        if (newsletterErrors) {
            newsletterErrors.style.display = 'none';

            while (newsletterErrors.firstChild) {
                newsletterErrors.removeChild(newsletterErrors.firstChild);
            }
        }

        const fmtHtml = document.getElementById('format-html');
        const fmtText = document.getElementById('format-text');
        const fmt = fmtText.checked ? fmtText.value : fmtHtml.value;
        const email = document.getElementById('id_email').value;

        // Get newsletters by checked inputs
        const checkedNewsletters = Array.from(
            document.querySelectorAll("input[name='newsletters']:checked")
        ).map((newsletter) => newsletter.value);

        // confirm at least one newsletter is checked
        if (checkedNewsletters.length === 0) {
            const errorString = document
                .getElementById('newsletter-error-strings')
                .getAttribute('data-form-checkboxes-error');
            errorArray.push(errorString);
            return newsletterError();
        }
        const newsletters = checkedNewsletters;
        const privacy = document.querySelector('input[name="privacy"]:checked')
            ? '&privacy=true'
            : '';
        const country = document.getElementById('id_country').value;
        const lang = document.getElementById('id_lang').value;
        const params =
            'email=' +
            encodeURIComponent(email) +
            '&' +
            newsletters
                .map((n) => {
                    return 'newsletters=' + n;
                })
                .join('&') +
            privacy +
            '&fmt=' +
            fmt +
            '&country=' +
            country +
            '&lang=' +
            lang +
            '&source_url=' +
            encodeURIComponent(document.location.href);

        const xhr = new XMLHttpRequest();

        xhr.onload = function (r) {
            if (r.target.status >= 200 && r.target.status < 300) {
                let response = r.target.response || r.target.responseText;

                if (typeof response !== 'object') {
                    response = JSON.parse(response);
                }

                if (response.success) {
                    newsletterForm.style.display = 'none';
                    newsletterThanks();
                    enableFormFields();
                    newsletterSuccess();

                    if (window.dataLayer) {
                        window.dataLayer.push({
                            event: 'newsletter-signup-success',
                            newsletter: newsletters
                        });
                    }
                } else {
                    if (response.errors) {
                        for (let i = 0; i < response.errors.length; i++) {
                            errorArray.push(response.errors[i]);
                        }
                    }
                    newsletterError();
                }
            } else {
                newsletterError();
            }
        };

        xhr.onerror = function (e) {
            newsletterError(e);
        };

        const url = newsletterForm.getAttribute('action');

        xhr.open('POST', url, true);
        xhr.setRequestHeader(
            'Content-type',
            'application/x-www-form-urlencoded'
        );
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.timeout = 5000;
        xhr.ontimeout = newsletterError;
        xhr.responseType = 'json';
        xhr.send(params);

        disableFormFields();

        return false;
    }

    newsletterForm.addEventListener('submit', newsletterSubscribe, false);
})();
