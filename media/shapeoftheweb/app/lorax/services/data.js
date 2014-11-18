/**
 * Manages data access.
 *
 * @class core/services/dataService
 */
define([
    'angular',
    'lorax/models/main'
], function (
    angular,
    MainModel
) {
    'use strict';

    var dataService = function ($http, $q) {

        this._defaultLocale = 'en-US';
        this._$http = $http;
        this._$q    = $q;
        this._mainData, this._requestingMain, this._mainDefer;
        this._mapData, this._requestingMap, this._mapDefer;

        function _buildMainEndpoint() {
            return [
                '/media/shapeoftheweb/data',
                'base',
                'main.json'
            ].join('/');
        }

        function _buildLocaleMainEndpoint(locale) {
            return [
                '/media/shapeoftheweb/data',
                'i18n',
                locale,
                'main.json'
            ].join('/');
        }

        function _buildInfographicEndpoint(locale) {
            return [
                '/media/shapeoftheweb/data',
                'i18n',
                locale,
                'infographics.json'
            ].join('/');
        }

        function _buildMapEndpoint() {
            return [
                '/media/shapeoftheweb/data',
                'base',
                'countries.topo.json'
            ].join('/');
        }

        function _buildCountryDataEndpoint(locale) {
            return [
                '/media/shapeoftheweb/data',
                'i18n',
                locale,
                'country-data.json'
            ].join('/');
        }

        /**
         * @method core/services/dataService~getMain
         * @param locale {String} Locale code
         */
        function getMain(locale) {
            locale = locale || this._defaultLocale;

            if (!this._mainData) {
                if (this._requestingMain) {
                    return this._mainDefer.promise;
                }

                this._requestingMain = true;
                this._mainDefer = this._$q.defer();

                var req = this._$http.get(_buildMainEndpoint());
                var localeReq = this._$http.get(_buildLocaleMainEndpoint(locale));
                var infographicReq = this._$http.get(_buildInfographicEndpoint(locale));

                req.then(function (res) {
                    if (res.data) {
                        localeReq.then(function (localeRes) {
                            if (localeRes.data) {
                                infographicReq.then(function (infographicRes) {
                                    this._mainData = new MainModel(res.data, localeRes.data, infographicRes.data);
                                    this._mainDefer.resolve(this._mainData);
                                }.bind(this));
                            }
                        }.bind(this));
                    }
                }.bind(this))['catch'](function (error) {
                    this._mainDefer.reject(error);
                }.bind(this));
            } else {
                this._mainDefer.resolve(this._mainData);
            }

            return this._mainDefer.promise;
        }

        function getMap(locale) {
            locale = locale || this._defaultLocale;

            if (!this._mapData) {
                if (this._requestingMap) {
                    return this._mapDefer.promise;
                }

                this._requestingMap = true;
                this._mapDefer = this._$q.defer();

                var req = this._$http.get(_buildMapEndpoint());
                var countryReq = this._$http.get(_buildCountryDataEndpoint(locale));

                req.then(function (res) {
                    if ( res.data ) {
                        countryReq.then(function (countryRes) {
                            this._mapData = {
                                "geoData": res.data,
                                "countryData": countryRes.data
                            };

                            this._mapDefer.resolve(this._mapData);
                        }.bind(this));
                    }
                }.bind(this))['catch'](function (error) {
                    this._mapDefer.reject(error);
                }.bind(this));
            } else {
                this._mapDefer.resolve(this._mapData);
            }

            return this._mapDefer.promise;
        }

        return {
            getMain: getMain.bind(this),
            getMap: getMap.bind(this)
        };
    };

    dataService.$inject = [
        '$http',
        '$q'
    ];

    return dataService;
});
