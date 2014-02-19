/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof Mozilla == 'undefined') {
    var Mozilla = {};
}

;(function($) {
    'use strict';

    // create namespace
    if (typeof Mozilla.FxOs == 'undefined') {
        Mozilla.FxOs = {};
    }

    Mozilla.FxOs.Countries = {
        'br': {
            'display': 'Brazil',
            'partner': [
                {
                    'name': 'Vivo',
                    'url': 'http://www.vivo.com.br/firefox'
                }
            ]
        },
        'cl': {
            "partner": [
                {
                    'name': 'Movistar',
                    'url': 'http://www.movistar.cl/equipos/catalogo/producto/847/contrato/'
                }
            ]
        },
        'co': {
            'display': 'Colombia',
            'partner': [
                {
                    'name': 'Movistar',
                    'url': 'http://www.movistar.co'
                }
            ]
        },
        'de': {
            'display': 'Germany',
            'partner': [
                {
                    'name': 'congstar',
                    'url': 'http://aktion.congstar.de/firefox-os'
                }
            ]
        },
        'es': {
            'display': 'Spain',
            'partner': [
                {
                    'name': 'Movistar',
                    'url': 'http://www.movistar.es/firefoxos?aff=aff-firefoxOS1'
                }
            ]
        },
        'gr': {
            'display': 'Greece',
            'partner': [
                {
                    'name': 'Cosmote',
                    'url': 'http://www.cosmote.gr/cosmoportal/cosmote.portal?_nfpb=true&_pageLabel=HDV&sku=20290038&s=0'
                }
            ]
        },
        'hu': {
            'display': 'Hungary',
            'partner': [
                {
                    'name': 'T-Mobile',
                    'url': 'https://webshop.t-mobile.hu/webapp/wcs/stores/ProductDisplay?catalogId=2001&storeId=2001&langId=-11&productId=644566'
                },
                {
                    'name': 'Telenor',
                    'url': 'http://www.telenor.hu/mobiltelefon/alcatel/one-touch-fire'
                }
            ]
        },
        'it': {
            'display': 'Italy',
            'partner': [
                {
                    'name': 'TIM',
                    'url': 'http://www.tim.it/prodotti/alcatel-one-touch-fire-mozilla-orange'
                }
            ]
        },
        'me': {
            'display': 'Montenegro',
            'partner': [
                {
                    'name': 'Telenor',
                    'url': 'http://www.telenor.me/sr/Privatni-korisnici/Uredjaji/Mobilni-telefoni/Alcatel/OT_Fire'
                }
            ]
        },
        'mx': {
            'display': 'Mexico',
            'partner': [
                {
                    'name': 'Movistar',
                    'url': 'http://www.movistar.com.mx/firefox'
                }
            ]
        },
        'pe': {
            'display': 'Peru',
            'partner': [
                {
                    'name': 'Movistar',
                    'url': 'http://catalogo.movistar.com.pe/zte-open'
                }
            ]
        },
        'pl': {
            'display': 'Poland',
            'partner': [
                {
                    'name': 'T-Mobile',
                    'url': 'http://www.t-mobile.pl/pl/firefox'
                }
            ]
        },
        'rs': {
            'display': 'Serbia',
            'partner': [
                {
                    'name': 'Telenor',
                    'url': 'https://www.telenor.rs/sr/Privatni-korisnici/webshop/Mobilni-telefoni/Alcatel/One_Touch_Fire'
                }
            ]
        },
        'uy': {
            'display': 'Uruguay',
            'partner': [
                {
                    'name': 'Movistar',
                    'url': 'http://www.firefoxos.movistar.com.uy/'
                }
            ]
        },
        've': {
            'display': 'Venezuela',
            'partner': [
                {
                    'name': 'Movistar',
                    'url': 'http://www.movistar.com.ve/movistar_firefox/index.html'
                }
            ]
        }
    };
})(window.jQuery);
