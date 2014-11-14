/**
 * loraxApp is the core module.
 * It serves as bootstrap for the app.
 *
 * @mixin lorax/loraxApp
 *
 */
define([
  'lorax/config/routes',
  //'core/config/http',

  // controller
  'lorax/controllers/core',
  'lorax/controllers/explore',
  'lorax/controllers/detail',
  'lorax/controllers/nav',

  // directives
  'lorax/directives/window',
  'lorax/directives/prevent-default',
  'lorax/directives/issue-details',
  'lorax/directives/issue-scroll',
  'lorax/directives/issue-all',
  'lorax/directives/chart-top-internet-companies',
  'lorax/directives/chart-terms-and-conditions',
  'lorax/directives/chart-common-languages',
  'lorax/directives/chart-line-graph',
  'lorax/directives/chart-world-map',
  'lorax/directives/chart-static-image',
  'lorax/directives/chart-accessible',
  'lorax/directives/chart-platform-neutrality',
  'lorax/directives/chart-lobbying',
  'lorax/directives/chart-cyber-threats',
  'lorax/directives/chart-data-portability',
  'lorax/directives/chart-open-source',
  'lorax/directives/chart-surveillance',
  'lorax/directives/chart-data-tracking',
  'lorax/directives/explore-canvas',
  'lorax/directives/add-infographic-directive',

  // services
  'lorax/services/window',
  'lorax/services/scroll',
  'lorax/services/pubsub',
  'lorax/services/data',
  'lorax/services/explore',

  //'core/constants/resource-bundle',

  'angular',
  'angular-route'
  //'angular-animate',
  //'angular-touch',
  //'angular-resource',

  //'core/providers/angular-adaptive-detection'
], function (
  RouteConfig,
  //HTTPConfig,

  // controllers
  CoreCtrl,
  ExploreCtrl,
  DetailCtrl,
  NavCtrl,

  // directives
  WindowDirective,
  PreventDefaultDirective,
  IssueDetailsDirective,
  IssueScrollDirective,
  IssueAllDirective,
  ChartTopInternetCompaniesDirective,
  ChartTermsAndConditionsDirective,
  ChartCommonLanguagesDirective,
  ChartLineGraphDirective,
  ChartWorldMapDirective,
  ChartStaticImageDirective,
  ChartAccessibleDirective,
  ChartPlatformNeutralityDirective,
  ChartLobbyingDirective,
  ChartCyberThreatsDirective,
  ChartDataPortabilityDirective,
  ChartOpenSourceDirective,
  ChartSurveillanceDirective,
  ChartDataTrackingDirective,
  ExploreCanvasDirective,
  AddInfographicDirective,

  // services
  windowService,
  scrollService,
  pubSubService,
  dataService,
  exploreService,

  //ResourceBundle,

  angular
) {
    'use strict';

    angular.module('loraxApp', [
        'ngRoute'
        // 'ngAnimate',
        //'ngTouch',
        //'ngResource',

        //'adaptive.detection'
    ])

        // Set up routing
        .config(RouteConfig)

        // Set up HTTP Interception
        //.config(HTTPConfig)

        // Attach environment config object
        //.constant('ENVIRONMENT', ENVIRONMENT)

        // For this simple implementation we can
        // consider the resource bundle as a constant.
        //.constant('ResourceBundle', ResourceBundle)

        /**
         * Injects {@link lorax/controllers/CoreCtrl} as 'CoreCtrl'
         * @method lorax/loraxApp~controller
         */
        .controller('CoreCtrl', CoreCtrl)

        /**
         * Injects {@link lorax/controllers/ExploreCtrl} as 'ExploreCtrl'
         * @method lorax/loraxApp~controller
         */
        .controller('ExploreCtrl', ExploreCtrl)

        /**
         * Injects {@link lorax/controllers/ExploreCtrl} as 'ExploreCtrl'
         * @method lorax/loraxApp~controller
         */
        .controller('DetailCtrl', DetailCtrl)

        /**
         * Injects {@link lorax/controllers/NavCtrl} as 'NavCtrl'
         * @method lorax/loraxApp~controller
         */
        .controller('NavCtrl', NavCtrl)

        /**
         * Injects {@link lorax/directives/WindowDirective} as 'WindowDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxWindow', WindowDirective)

        /**
         * Injects {@link lorax/directives/WindowDirective} as 'WindowDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxPreventDefault', PreventDefaultDirective)

        /**
         * Injects {@link lorax/directives/IssueDetails} as 'IssueDetails'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxIssueDetails', IssueDetailsDirective)

        /**
         * Injects {@link lorax/directives/IssueScrollDirective} as 'IssueScrollDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxIssueScroll', IssueScrollDirective)

        /**
         * Injects {@link lorax/directives/IssueAll} as 'IssueAllDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxIssueAll', IssueAllDirective)

        /**
         * Injects {@link lorax/directives/ChartTopInternetCompaniesDirective}
         * as 'ChartTopInternetCompaniesDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartTopInternetCompanies', ChartTopInternetCompaniesDirective)

        /**
         * Injects {@link lorax/directives/ChartTermsAndConditionsDirective}
         * as 'ChartTermsAndConditionsDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartTermsAndConditions', ChartTermsAndConditionsDirective)

        /**
         * Injects {@link lorax/directives/ChartCommonLanguagesDirective}
         * as 'ChartCommonLanguagesDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartCommonLanguages', ChartCommonLanguagesDirective)

        /**
         * Injects {@link lorax/directives/ChartLineGraphDirective}
         * as 'ChartLineGraphDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartLineGraph', ChartLineGraphDirective)

        /**
         * Injects {@link lorax/directives/ChartWorldMapDirective}
         * as 'ChartLineGraphDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartWorldMap', ChartWorldMapDirective)

        /**
         * Injects {@link lorax/directives/ChartStaticImageDirective}
         * as 'ChartStaticImageDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartStaticImage', ChartStaticImageDirective)

        /**
         * Injects {@link lorax/directives/ChartAccessibleDirective}
         * as 'ChartAccessibleDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartAccessible', ChartAccessibleDirective)

        /**
         * Injects {@link lorax/directives/ChartPlatformNeutralityDirective}
         * as 'ChartPlatformNeutralityDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartPlatformNeutrality', ChartPlatformNeutralityDirective)

        /**
         * Injects {@link lorax/directives/ChartLobbyingDirective}
         * as 'ChartLobbyingDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartLobbying', ChartLobbyingDirective)

        /**
         * Injects {@link lorax/directives/ChartCyberThreatsDirective}
         * as 'ChartCyberThreatsDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartCyberThreats', ChartCyberThreatsDirective)

        /**
         * Injects {@link lorax/directives/ChartDataPortabilityDirective}
         * as 'ChartDataPortabilityDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartDataPortability', ChartDataPortabilityDirective)

        /**
         * Injects {@link lorax/directives/ChartOpenSourceDirective}
         * as 'ChartOpenSourceDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartOpenSource', ChartOpenSourceDirective)

        /**
         * Injects {@link lorax/directives/ChartSurveillanceDirective}
         * as 'ChartSurveillanceDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartSurveillance', ChartSurveillanceDirective)

        /**
         * Injects {@link lorax/directives/ChartDataTrackingDirective}
         * as 'ChartDataTrackingDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxChartDataTracking', ChartDataTrackingDirective)

        /**
         * Injects {@link lorax/directives/ChartLobbyingCostsDirective}
         * as 'ChartLobbyingCostsDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxExploreCanvas', ExploreCanvasDirective)

        /**
         * Injects {@link lorax/directives/ChartLobbyingCostsDirective}
         * as 'ChartLobbyingCostsDirective'
         * @method lorax/loraxApp~directive
         */
        .directive('loraxAddInfographicDirective', AddInfographicDirective)

        /**
         * Inject {@link lorax/services/locationService} as 'locationService'
         * @method lorax/loraxApp~service
         */
        //.service('locationService', locationService)

        /**
         * Inject {@link lorax/services/windowService} as 'windowService'
         * @method lorax/loraxApp~service
         */
        .service('windowService', windowService)

        /**
         * Inject {@link lorax/services/scrollService} as 'scrollService'
         * @method lorax/loraxApp~service
         */
        .service('scrollService', scrollService)

        /**
         * Inject {@link lorax/services/dataService} as 'dataService'
         * @method lorax/loraxApp~factory
         */
        .service('exploreService', exploreService)

        /**
         * Inject {@link lorax/services/pubSubService} as 'pubSubService'
         * @method lorax/loraxApp~factory
         */
        .factory('pubSubService', pubSubService)

        /**
         * Inject {@link lorax/services/dataService} as 'dataService'
         * @method lorax/loraxApp~factory
         */
        .factory('dataService', dataService)

      /**
       * Bootstrap the application
       */
      return angular.bootstrap(document, ['loraxApp']);
});
