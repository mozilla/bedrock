/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {

    var pocket = document.querySelectorAll('.mobile-pocket');
    var lockbox = document.querySelectorAll('.mobile-lockbox');
    var notes = document.querySelectorAll('.mobile-notes');
    var fxModal = document.getElementById('fx-modal');
    var qrCode = document.getElementById('qr-code');
    var bottomBannerMobile = document.getElementById('bottom-banner-mobile');

    var fxQrTitle = document.getElementById('fx-qr-title');
    var fxAppButtons = document.getElementById('fx-app-buttons');

    fxModal.addEventListener('click', openFxModal);

    function openFxModal() {
        fxQrTitle.style.display = 'block';
        fxAppButtons.style.display = 'inline-block';
        Mzp.Modal.createModal(this, content, {
            title: 'Download the Firefox App',
            className: 'mzp-t-firefox',
            closeText: window.Mozilla.Utils.trans('global-close'),
            onDestroy: function() {
                fxQrTitle.style.display = 'none';
                fxAppButtons.style.display = 'none';
            }
        });
        var qrCode = document.getElementById('qr-code');
        qrCode.setAttribute('class', 'fx-qr');
    }

    function openModal(e) {
        e.preventDefault();
        fxQrTitle.style.display = 'none';
        fxAppButtons.style.display = 'none';
        var parent = this.closest('.mzp-c-card-feature');
        var productString = parent.className;
        var mobileButtons = document.querySelectorAll('.mobile-download-buttons');
        var mobileTitles = document.querySelectorAll('.mobile-title');

        function show(product){
            for (var i = 0; i < product.length; i++){
                product[i].style.display = 'block';
            }
        }

        function hide(mobileTitles, mobileButtons){
            for (var i = 0; i < mobileTitles.length; i++){
                mobileTitles[i].style.display = 'none';
            }
            for (i = 0; i < mobileButtons.length; i++){
                mobileButtons[i].style.display = 'none';
            }
        }

        switch (true) {
        case productString.includes('lockbox'):
            qrCode.setAttribute('class', 'lockbox');
            show(lockbox);
            break;
        case productString.includes('pocket'):
            qrCode.setAttribute('class', 'pocket');
            show(pocket);
            break;
        case productString.includes('notes'):
            qrCode.setAttribute('class', 'notes');
            show(notes);
            break;
        }

        Mzp.Modal.createModal(this, content, {
            title: this.innerHTML,
            className: 'mzp-t-firefox',
            closeText: window.Mozilla.Utils.trans('global-close'),
            onDestroy: function() {
                hide(mobileTitles, mobileButtons);
                bottomBannerMobile.style.display = 'inline-block';
            }
        });

    }

    var qrLinks = document.querySelectorAll('.mzp-c-card-feature .mzp-c-cta-link');
    var content = document.querySelector('.mzp-u-modal-content');

    for (var i = 0; i < qrLinks.length; i++) {
        qrLinks[i].addEventListener('click', openModal);
    }



})();
