/**
 * @fileOverview Explore canvas directive
 * @author <a href="mailto:leandroferreira@moco.to">Leandro Ferreira</a>
 */
define(['explore/explore'], function (Explore) {
    'use strict';

    /**
     * directive
     */
    var ExploreCanvasDirective = function () {
        return {
            restrict: 'A',
            replace: true,
            controller: ExploreCanvasController,
            link: ExploreCanvasLinkFn,
            templateUrl: '/media/shapeoftheweb/app/lorax/directives/explore-canvas.tpl.html'
        };
    };

    /**
     * Controller for explore canvas directive
     * @constructor
     */
    var ExploreCanvasController = function (
        $scope,
        dataService,
        exploreService
        )
    {
        this._$scope = $scope;

        dataService.getMain().then(function(model) {
            this._explore = new Explore();
            this._explore.setData(model);
            this._explore.setContainer(this._container);
            exploreService.setCanvas(this._explore);
        }.bind(this));
    };

    /**
     * Array of dependencies to be injected into controller
     * @type {Array}
     */
    ExploreCanvasController.$inject = [
        '$scope',
        'dataService',
        'exploreService'
    ];

    /**
     * Link function
     * @param {object} scope      Angular scope.
     * @param {JQuery} iElem      jQuery element.
     * @param {object} iAttrs     Directive attributes.
     * @param {object} controller Controller reference.
     */
    var ExploreCanvasLinkFn = function (scope, iElem, iAttrs, controller) {
        controller._container = iElem;
    };

    return ExploreCanvasDirective;
});
