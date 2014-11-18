/* global require:true */
(function (require) {
    'use strict';

    require.config({
        baseUrl: '/media/shapeoftheweb/app/',

        name: '../scripts/components/almond/almond',

        paths: {
            'angular': '../scripts/components/angular/angular',
            'angular-route': '../scripts/components/angular-route/angular-route',
            'jquery': '../scripts/components/jquery/jquery',
            'jquery-mobile': '../scripts/libs/jquery.mobile.min',
            'jquery-scrollie': '../scripts/libs/jquery.scrollie.min',
            'jquery-selectric': '../scripts/components/jquery-selectric/jquery.selectric',
            'modernizr': '../scripts/modernizr',
            'd3': '../scripts/components/d3/d3',
            'topojson': '../scripts/libs/topojson.v1.min',
            'pubsub': '../scripts/components/jquery-tiny-pubsub/tiny-pubsub',
            'utils': '../scripts/utils',
            'lodash': '../scripts/components/lodash/lodash.compat',
            'pixi': '../scripts/components/pixi/pixi.dev',
            'stats': '../scripts/components/stats.js/stats.min',
            'createjs': '../scripts/components/TweenJS/tweenjs-0.5.1.combined',
            'signals': '../scripts/components/js-signals/signals',
            'explore': '../scripts/explore'
        },

        include: ['lorax/lorax-app'],

        insertRequire: ['lorax/lorax-app'],

        shim: {
            'angular': {
                exports: 'angular',
                deps: ['jquery']
            },
            'angular-route': {
                deps: ['angular']
            },
            'jquery-mobile': {
                deps: ['jquery']
            },
            'jquery-scrollie': {
                deps: ['jquery']
            },
            'jquery-selectric': {
                deps: ['jquery']
            },
            'pubsub': {
                deps: ['jquery']
            },
            'modernizr': {
                exports: ['Modernizr']
            },
            'stats': {
                exports: 'Stats'
            },
            'createjs': {
                exports: 'createjs'
            }
        },

        deps: ['lorax/lorax-app'],

        wrap: true

    });

}(require));
