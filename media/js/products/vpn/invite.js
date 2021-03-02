/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var newsletterForm = document.getElementById('newsletter-form');

    if (!newsletterForm) {
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
            errorList.className = 'mzp-u-list-styled';

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
        window.scrollTo(0, 0);
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

        var platforms = '';
        var platformOptions = document.querySelector('.vpn-invite-platform-options');
        var email = document.getElementById('id_email').value;
        var newsletter = document.getElementById('id_newsletters').value;
        var country = document.getElementById('id_country').value;
        var lang = document.getElementById('id_lang').value;

        // platform options are not required in the form.
        if (platformOptions) {
            var windows = document.getElementById('platforms-windows');
            var ios = document.getElementById('platforms-ios');
            var android = document.getElementById('platforms-android');
            var mac = document.getElementById('platforms-mac');
            var chromebook = document.getElementById('platforms-chromebook');
            var linux = document.getElementById('platforms-linux');


            platforms += windows.checked ? '&platforms=' + windows.value : '';
            platforms += ios.checked ? '&platforms=' + ios.value : '';
            platforms += android.checked ? '&platforms=' + android.value : '';
            platforms += mac.checked ? '&platforms=' + mac.value : '';
            platforms += chromebook.checked ? '&platforms=' + chromebook.value : '';
            platforms += linux.checked ? '&platforms=' + linux.value : '';
        }

        var params = 'email=' + encodeURIComponent(email) +
                     '&newsletters=' + newsletter +
                     '&country=' + country +
                     '&lang=' + lang +
                     '&privacy=true' +
                     '&fmt=H' +
                     platforms +
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
