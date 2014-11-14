/**
 * Nav bar controller
 *
 * @class lorax/controllers/DetailCtrl
 * @param $scope
 */
define([], function () {
    'use strict';

    var NavCtrl = function (
        $scope,
        $location,
        dataService
    ) {

        this._$scope = $scope;
        this._$location = $location;

        this._$scope.nav = {
            active : 'access'
        };

        this._$scope.nav.handleClick = function (topic) {
            this._$scope.nav.active = topic;
        }.bind(this);

        dataService.getMain().then(function (model) {
            this._$scope.nav.model = model;
        }.bind(this));

        var topic = this._$location.search().topic;
        if (topic) {
            this._$scope.nav.active = topic;
        }
        else {
            this._$scope.nav.active = 'access';
        }
    };

    NavCtrl.$inject = [
        '$scope',
        '$location',
        'dataService'
    ];

    return NavCtrl;
});
