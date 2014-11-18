define(function () {
    'use strict';

    var RouteConfig = function (
            $routeProvider,
            $locationProvider
        ) {

        // Invoke HTML5 pushState
        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
        });

        $routeProvider

            /* --------- Explore -------- */

            .when('/en-US/shapeoftheweb', {
                templateUrl: '/media/shapeoftheweb/app/lorax/templates/explore.tpl.html'
            })

            /* -------------------- Detail -------------------- */

            .when('/en-US/shapeoftheweb/detail/', {
                templateUrl: '/media/shapeoftheweb/app/lorax/templates/issues.tpl.html',
                reloadOnSearch: false
            })

            /* -------------------- Error -------------------- */

            .when('/error', {
                redirectTo: '/en-US/shapeoftheweb'
                //templateUrl: '/media/shapeoftheweb/app/lorax/templates/404.tpl.html'
            });

    };


    /**
     * Array of dependencies to preserve Angular DI during rjs minification
     * @type {Array}
     */
    RouteConfig.$inject = [
        '$routeProvider',
        '$locationProvider'
    ];

    return RouteConfig;
});
