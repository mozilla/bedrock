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

    /*
    List of countries where phones are available.

    If partner entry has 'developer_only' set to true, that partner should only
    be available on developer facing pages (/firefox/os/devices/). Currently
    used for ZTE Open C eBay links.

    Full list of ISO_3166-1 country codes is available here
    for reference: http://en.wikipedia.org/wiki/ISO_3166-1
    */

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
            'display': 'Chile',
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
                    'name': 'Alcatel One Touch Fire',
                    'url': 'http://aktion.congstar.de/firefox-os'
                },
                {
                    'name': 'Alcatel One Touch Fire E',
                    'url': 'http://www.congstar.de/handy/alcatel-one-touch-fire-e-braun/'
                },
                {
                    'name': 'Alcatel One Touch Fire E',
                    'url': 'http://www.o2online.de/handy/alcatel-onetouch-fire-e/',
                    'carrier': 'o2'
                },
                {
                    'name': 'ZTE Open C',
                    'url': 'http://www.ebay.de/itm/eBay-Exklusiv-ZTE-OPEN-C-Neuesten-Firefox-OS-DualCore-1-2-GHz-4-0-3G-Smartphone-/131151681046?ssPageName=STRK:MESE:IT',
                    'developer_only': true
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
        'gb': {
            'display': 'United Kingdom',
            'partner': [
                {
                    'name': 'eBay',
                    'url': 'http://item.ebay.co.uk/171301269724',
                    'developer_only': true
                }
            ]
        },
        'fr': {
            'display': 'France',
            'partner': [
                {
                    'name': 'ZTE France',
                    'url': 'http://www.ztefrance.com/firefox-open-c.php'
                },
                {
                    'name': 'LDLC',
                    'url': 'http://www.ldlc.com/fiche/PB00171571.html#53302f3f2a970'
                },
                {
                    'name': 'E.Leclerc',
                    'url': 'http://www.leclercmobile.fr/telephones-mobiles/notre-gamme/mobiles/Zte_Open-C.aspx'
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
                    'url': 'https://www.movistar.com.mx/catalogo'
                },
                {
                    'name': 'Telcel',
                    'url': 'http://www.telcel.com/portal/equipos/begin.do?idEquipo=3618'
                }
            ]
        },
        'pe': {
            'display': 'Peru',
            'partner': [
                {
                    'name': 'Movistar',
                    'url': 'http://movistarfirefoxos.pe/'
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
        'ru': {
            'display': 'Russia',
            'partner': [
                {
                    'name': 'eBay',
                    'url': 'http://www.ebay.com/itm/eBay-Exclusive-ZTE-OPEN-C-Dual-Core-4-Latest-Firefox-OS-3G-Unlocked-Smartphone-/111326263156?ssPageName=STRK:MESE:IT',
                    'developer_only': true
                }
            ]
        },
        'us': {
            'display': 'United States',
            'partner': [
                {
                    'name': 'eBay',
                    'url': 'http://item.ebay.com/291125433026',
                    'developer_only': true
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

    Mozilla.FxOs.Devices = {
        'alcatel_onetouchfire': {
            'type': 'smartphone',
            'display': 'Alcatel One Touch Fire',
            'countries': ['br', 'cl', 'co', 'de', 'gr', 'hu', 'it', 'me', 'mx', 'pe', 'pl', 'rs', 'uy', 've']
        },
        'alcatel_onetouchfirec': {
            'type': 'smartphone',
            'display': 'Alcatel One Touch Fire C',
            'countries': []
        },
        'alcatel_onetouchfiree': {
            'type': 'smartphone',
            'display': 'Alcatel One Touch Fire E',
            'countries': ['de']
        },
        'huawei_y300-2': {
            'type': 'smartphone',
            'display': 'Huawei Y300II',
            'countries': ['mx']
        },
        'lg_fireweb': {
            'type': 'smartphone',
            'display': 'LG Fireweb',
            'countries': ['br', 'uy']
        },
        'zte_open': {
            'type': 'smartphone',
            'display': 'ZTE Open',
            'countries': ['co', 'es', 'mx', 'pe', 'uy', 've']
        },
        'zte_openc': {
            'type': 'smartphone',
            'display': 'ZTE Open C',
            'countries': ['de', 'fr', 'gb', 'ru', 'us', 'uy']
        },
        'zte_open2': {
            'type': 'smartphone',
            'display': 'ZTE Open II',
            'countries': ['co', 'pe']
        }
    };
})(window.jQuery);
