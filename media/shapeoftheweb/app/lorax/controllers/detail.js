/**
 * Detail page controller
 *
 * @class lorax/controllers/DetailCtrl
 * @param $scope
 */
define([], function () {
    'use strict';

    var DetailCtrl = function (
        $scope,
        $route
    ) {

        this._$scope = $scope;
        this._$route = $route;

        this._$scope.detail = { };

        // var getMainPromise = dataService.getMain();

        // this._$scope.$on('$routeChangeSuccess', function(evt, newParam) {
        //   this._$scope.detail.topicParam = newParam.params.topic;
        //   this._$scope.detail.issueParam = newParam.params.issue;

        //   getMainPromise.then(function(model) {
        //     this._$scope.detail.model = model;

        //     this._$scope.$evalAsync( function() {
        //       if ( newParam.params.issue ) {
        //         console.log("Issue exists. Animate!");
        //       } else if ( newParam.params.topic ) {
        //         console.log("Topic exists. Animate!");
        //         var issue = this._$scope.detail.model.getTopicById(newParam.params.topic).getIssues()[0].getId();
        //         $('#' + issue).scrollIntoView();
        //       } else {
        //         console.log("Nothing. Go to top of page.");
        //       }
        //     }.bind(this));
        //   }.bind(this));
        // }.bind(this));


    };

    DetailCtrl.$inject = [
        '$scope',
        '$route'
    ];

    return DetailCtrl;
});
