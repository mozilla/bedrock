/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // TODO port this JS to Protocol
    // !! this file assumes only one signup form per page !!

    var newsletterForm = document.getElementById('newsletter-form');

    if(!newsletterForm) {
        return;
    }

    // handle errors
    var errorArray = [];
    var newsletterErrors = document.getElementById('newsletter-errors');
    var newsletterContent = document.querySelector('.mzp-c-newsletter-content');

    function disableFormFields() {
        var formFields = newsletterForm.querySelectorAll('input, select');

        for (var i = 0; i < formFields.length; i++) {
            formFields[i].disabled = true;
        }
    }

    function enableFormFields() {
        var formFields = newsletterForm.querySelectorAll('input, select');

        for (var i = 0; i < formFields.length; i++) {
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
                newsletterContent.insertBefore(newsletterErrors, newsletterContent.firstChild);
            }

            var errorList = document.createElement('ul');

            for (var i = 0; i < errorArray.length; i++) {
                var item = document.createElement('li');
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
        var thanks = document.getElementById('newsletter-thanks');

        // show thanks message
        thanks.style.display = 'block';
    }

    // trigger success event
    function newsletterSuccess() {
        if (typeof document.CustomEvent === 'function') {
            document.dispatchEvent(new CustomEvent('newsletterSuccess', {
                bubbles: true,
                cancelable: true
            }));
        } else if (typeof document.createEvent === 'function') {
            var event = document.createEvent('Event');
            event.initEvent('newsletterSuccess', true, true);
            document.dispatchEvent(event);
        }
    }

    // XHR subscribe; handle errors; display thanks message on success.
    function newsletterSubscribe(evt) {
        var skipXHR = newsletterForm.getAttribute('data-skip-xhr');
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

        var fmtHtml = document.getElementById('format-html');
        var fmtText = document.getElementById('format-text');
        var fmt = fmtText.checked ? fmtText.value : fmtHtml.value;
        var email = document.getElementById('id_email').value;
        var newsletter = document.getElementById('id_newsletters').value;
        var privacy = document.querySelector('input[name="privacy"]:checked') ? '&privacy=true' : '';
        var country = document.getElementById('id_country').value;
        var lang = document.getElementById('id_lang').value;
        var params = 'email=' + encodeURIComponent(email) +
                     '&newsletters=' + newsletter +
                     privacy +
                     '&fmt=' + fmt +
                     '&country=' + country +
                     '&lang=' + lang +
                     '&source_url=' + encodeURIComponent(document.location.href);

        var xhr = new XMLHttpRequest();

        xhr.onload = function(r) {
            if (r.target.status >= 200 && r.target.status < 300) {
                var response = r.target.response || r.target.responseText;

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
                            'event': 'newsletter-signup-success',
                            'newsletter': newsletter
                        });
                    }
                } else {
                    if (response.errors) {
                        for (var i = 0; i < response.errors.length; i++) {
                            errorArray.push(response.errors[i]);
                        }
                    }
                    newsletterError();
                }
            }
            else {
                newsletterError();
            }
        };

        xhr.onerror = function(e) {
            newsletterError(e);
        };

        var url = newsletterForm.getAttribute('action');

        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-Requested-With','XMLHttpRequest');
        xhr.timeout = 5000;
        xhr.ontimeout = newsletterError;
        xhr.responseType = 'json';
        xhr.send(params);

        disableFormFields();

        return false;
    }

    newsletterForm.addEventListener('submit', newsletterSubscribe, false);
})();
