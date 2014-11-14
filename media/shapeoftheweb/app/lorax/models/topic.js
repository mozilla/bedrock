define([
    'lorax/models/issue'
], function (
    IssueModel
) {
    'use strict';

    var TopicModel = function (id, data, tags, localeData, infographicData) {
        this._id = id;
        this._name = localeData.name;
        this._tagline = localeData.tagline;
        this._issues = [];

        for (var idxIssue in data.issues) {
            this._issues.push(new IssueModel(
                this,
                idxIssue,
                data.issues[idxIssue],
                tags,
                localeData.issues[idxIssue],
                infographicData[idxIssue]
            ));
        }
    };

    TopicModel.prototype.getId = function () {
        return this._id;
    };

    TopicModel.prototype.getName = function () {
        return this._name;
    };

    TopicModel.prototype.getTagline = function () {
        return this._tagline;
    };

    TopicModel.prototype.getIssues = function () {
        return this._issues;
    };

    return TopicModel;
});

