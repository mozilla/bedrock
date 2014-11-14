/**
 * @fileOverview Issue Details directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define([], function (IssueModel) {
    'use strict';

    /**
     * Issue Details directive
     */
    var IssueDetailsDirective = function () {
        return {
            restrict: 'A',
            replace: true,
            transclude: true,
            scope: {
                'issueStatus': '@',
                'issueName': '@'
            },
            controller: IssueDetailsController,
            //link: IssueDetailsLinkFn,
            templateUrl: '/media/shapeoftheweb/app/lorax/directives/issue-details.tpl.html'
        };
    };

    /**
     * Controller for detail directive
     * @constructor
     */
    var IssueDetailsController = function (
        $scope,
        dataService
        )
    {
        this._$scope = $scope;

        this._$scope.issueDetails = {
            status: $scope.issueStatus
        };

        dataService.getMain().then(function (model) {
            this._$scope.issueDetails.issue = model.getIssueById($scope.issueName);
        }.bind(this));
    };

    /**
     * Array of dependencies to be injected into controller
     * @type {Array}
     */
    IssueDetailsController.$inject = [
        '$scope',
        'dataService'
    ];

    /**
     * Doesn't really do anything
     * @param  {string}          No parameters
     * @return {string}          No return value
     */
    IssueDetailsController.prototype.testMethod = function () {
        console.log('test');
    };

    /**
     * Link function for Detail Section directive
     * @param {object} scope      Angular scope.
     * @param {JQuery} iElem      jQuery element.
     * @param {object} iAttrs     Directive attributes.
     * @param {object} controller Controller reference.
     */
    /*var IssueDetailsLinkFn = function (scope, iElem, iAttrs, controller) {

    };*/

    return IssueDetailsDirective;
});
