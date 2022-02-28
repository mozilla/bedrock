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

        // Get newsletters by hidden id or checked inputs
        let newsletters = '';
        const singleNewsletterForm = document.getElementById('id_newsletters');
        if (singleNewsletterForm) {
            newsletters = singleNewsletterForm.value;
        } else {
            // MDN suggested Array.from Polyfill: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from#polyfill
            // Production steps of ECMA-262, Edition 6, 22.1.2.1
            if (!Array.from) {
                Array.from = (function () {
                    let symbolIterator;
                    try {
                        symbolIterator = Symbol.iterator
                            ? Symbol.iterator
                            : 'Symbol(Symbol.iterator)';
                    } catch (e) {
                        symbolIterator = 'Symbol(Symbol.iterator)';
                    }

                    const toStr = Object.prototype.toString;
                    const isCallable = function (fn) {
                        return (
                            typeof fn === 'function' ||
                            toStr.call(fn) === '[object Function]'
                        );
                    };
                    const toInteger = function (value) {
                        const number = Number(value);
                        if (isNaN(number)) return 0;
                        if (number === 0 || !isFinite(number)) return number;
                        return (
                            (number > 0 ? 1 : -1) * Math.floor(Math.abs(number))
                        );
                    };
                    const maxSafeInteger = Math.pow(2, 53) - 1;
                    const toLength = function (value) {
                        const len = toInteger(value);
                        return Math.min(Math.max(len, 0), maxSafeInteger);
                    };

                    const setGetItemHandler = function setGetItemHandler(
                        isIterator,
                        items
                    ) {
                        const iterator = isIterator && items[symbolIterator]();
                        return function getItem(k) {
                            return isIterator ? iterator.next() : items[k];
                        };
                    };

                    const getArray = function getArray(
                        T,
                        A,
                        len,
                        getItem,
                        isIterator,
                        mapFn
                    ) {
                        // 16. Let k be 0.
                        let k = 0;

                        // 17. Repeat, while k < len… or while iterator is done (also steps a - h)
                        while (k < len || isIterator) {
                            const item = getItem(k);
                            const kValue = isIterator ? item.value : item;

                            if (isIterator && item.done) {
                                return A;
                            } else {
                                if (mapFn) {
                                    A[k] =
                                        typeof T === 'undefined'
                                            ? mapFn(kValue, k)
                                            : mapFn.call(T, kValue, k);
                                } else {
                                    A[k] = kValue;
                                }
                            }
                            k += 1;
                        }

                        if (isIterator) {
                            throw new TypeError(
                                'Array.from: provided arrayLike or iterator has length more then 2 ** 52 - 1'
                            );
                        } else {
                            A.length = len;
                        }

                        return A;
                    };

                    // The length property of the from method is 1.
                    return function from(
                        arrayLikeOrIterator /*, mapFn, thisArg */
                    ) {
                        // 1. Let C be the this value.
                        const C = this;

                        // 2. Let items be ToObject(arrayLikeOrIterator).
                        const items = Object(arrayLikeOrIterator);
                        const isIterator = isCallable(items[symbolIterator]);

                        // 3. ReturnIfAbrupt(items).
                        if (arrayLikeOrIterator === null && !isIterator) {
                            throw new TypeError(
                                'Array.from requires an array-like object or iterator - not null or undefined'
                            );
                        }

                        // 4. If mapfn is undefined, then let mapping be false.
                        const mapFn =
                            arguments.length > 1
                                ? arguments[1]
                                : void undefined;
                        let T;
                        if (typeof mapFn !== 'undefined') {
                            // 5. else
                            // 5. a If IsCallable(mapfn) is false, throw a TypeError exception.
                            if (!isCallable(mapFn)) {
                                throw new TypeError(
                                    'Array.from: when provided, the second argument must be a function'
                                );
                            }

                            // 5. b. If thisArg was supplied, let T be thisArg; else let T be undefined.
                            if (arguments.length > 2) {
                                T = arguments[2];
                            }
                        }

                        // 10. Let lenValue be Get(items, "length").
                        // 11. Let len be ToLength(lenValue).
                        const len = toLength(items.length);

                        // 13. If IsConstructor(C) is true, then
                        // 13. a. Let A be the result of calling the [[Construct]] internal method
                        // of C with an argument list containing the single item len.
                        // 14. a. Else, Let A be ArrayCreate(len).
                        const A = isCallable(C)
                            ? Object(new C(len))
                            : new Array(len);

                        return getArray(
                            T,
                            A,
                            len,
                            setGetItemHandler(isIterator, items),
                            isIterator,
                            mapFn
                        );
                    };
                })();
            }
            // end Array.from polyfill

            const checkedNewsletters = Array.from(
                document.querySelectorAll("input[name='newsletter-id']:checked")
            ).map((newsletter) => newsletter.value);

            // confirm at least one newsletter is checked
            if (checkedNewsletters.length === 0) {
                const errorString = document
                    .getElementById('newsletter-error-strings')
                    .getAttribute('data-form-checkboxes-error');
                errorArray.push(errorString);
                return newsletterError();
            }
            newsletters = checkedNewsletters.join(',');
        }
        const privacy = document.querySelector('input[name="privacy"]:checked')
            ? '&privacy=true'
            : '';
        const country = document.getElementById('id_country').value;
        const lang = document.getElementById('id_lang').value;
        const params =
            'email=' +
            encodeURIComponent(email) +
            '&newsletters=' +
            newsletters +
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
