/**
 * @fileOverview Prevent Default directive
 * @author <a href="mailto:chris@work.co">Chris James</a>
 */
define(function () {
    'use strict';

    var PreventDefaultDirective = function () {
        return {
            restrict: 'A',
            link: PreventDefaultLinkFn
        };
    };

    var PreventDefaultLinkFn = function (scope, iElem, iAttrs) {
        if (iAttrs.ngClick || iAttrs.href === '' || iAttrs.href === '#') {
            iElem.on('click', function (e) {
                e.preventDefault();
            });
        }
    };

    return PreventDefaultDirective;
});
