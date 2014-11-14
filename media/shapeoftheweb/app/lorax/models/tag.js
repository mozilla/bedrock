define([
    'lorax/models/base'
], function (
    BaseModel
) {
    'use strict';

    var TagModel = function (id) {
        this._id = id;
        // this._name = this._localize(localeData, 'tags', id, 'name');
        this._name = id;
        this._issues = [];
    };

    TagModel.prototype = new BaseModel();

    TagModel.prototype.getId = function () {
        return this._id;
    };

    TagModel.prototype.getName = function () {
        return this._name;
    };

    TagModel.prototype.getIssues = function () {
        return this._issues;
    };

    TagModel.prototype.addIssue = function (issue) {
        this._issues.push(issue);
    };

    TagModel.prototype.getRelated = function () {
        return this.getIssues();
    };

    return TagModel;
});

