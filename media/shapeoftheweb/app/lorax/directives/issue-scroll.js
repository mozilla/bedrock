/**
 * @fileOverview Issue page scroll directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define(['jquery', 'jquery-scrollie'], function ($) {
    'use strict';

    /**
     * Issue Scroll directive
     */
    var IssueScrollDirective = function () {
        return {
            restrict: 'A',
            scope: true,
            controller: IssueScrollCtrl,
            link: IssueScrollLinkFn
        };
    };

    /**
     * Controller for detail scroll directive
     * @constructor
     */
    var IssueScrollCtrl = function (
        $scope,
        $timeout
    ) {

        this._$scope = $scope;
        this._$timeout = $timeout;
    };

    IssueScrollCtrl.$inject = [
        '$scope',
        '$timeout',
        'windowService'
    ];

    /**
     * Link function for Issue Page Scroll directive
     * @param {object} scope      Angular scope.
     * @param {JQuery} iElem      Detail wrapper jQuery element.
     */
    var IssueScrollLinkFn = function (scope, iElem, iAttrs, controller) {

        controller._$timeout(function () {
            var $body = $('body');
            var $detail = $('.detail');
            var status = $detail.eq(0).attr('data-issue-status');

            $body.attr('data-bg-mode', status);

            $detail.scrollie({
                scrollOffset : -100,
                scrollingInView : function (elem) {
                    status = elem.attr('data-issue-status');

                    $body.attr('data-bg-mode', status);
                }
            });
        }, 500);
    };

    return IssueScrollDirective;
});
