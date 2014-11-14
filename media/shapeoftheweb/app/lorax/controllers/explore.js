/**
 * Explore controller
 *
 * @class lorax/controllers/ExploreCtrl
 * @param $scope
 */
define([], function () {
    'use strict';

    /*jshint unused: false */
    var ExploreCtrl = function (
        $scope,
        exploreService
    ) {

        this._$scope = $scope;
        this._$scope.explore = {
            switchView: this.switchView.bind(this),
            currentView: 'explore'
        };

        this._exploreService = exploreService;
    };

    ExploreCtrl.$inject = [
        '$scope',
        'exploreService'
    ];

    ExploreCtrl.prototype.switchView = function (view) {
        this._$scope.explore.currentView = view;
        this._exploreService.switchView(view);
    };

    return ExploreCtrl;
});
