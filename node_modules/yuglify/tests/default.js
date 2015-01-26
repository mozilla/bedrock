var vows = require('vows'),
    path = require('path'),
    assert = require('assert');

var tests = {
    "require": {
        topic: function() {
            return require('../lib');
        },
        "should have jsmin": function(topic) {
            assert.ok(topic.jsmin);
        },
        "should have cssmin": function(topic) {
            assert.ok(topic.cssmin);
        }
    }
};

vows.describe('yUglify').addBatch(tests).export(module);
