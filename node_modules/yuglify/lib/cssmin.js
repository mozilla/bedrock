/*
Copyright (c) 2012, Yahoo! Inc. All rights reserved.
Code licensed under the BSD License:
http://yuilibrary.com/license/
*/

var cssmin = require('ycssmin').cssmin,
    lines = 6000;

exports.cssmin = function (source, num, callback) {
    if (typeof num === 'function') {
        callback = num;
        num = lines;
    }
    num = num || lines;
    var result = cssmin(source, num);
    callback(null, result + '\n');
};

