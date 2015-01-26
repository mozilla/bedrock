yUglify
=======

`yuglify` is a wrapper around [UglifyJS](https://github.com/mishoo/UglifyJS) and [cssmin](https://github.com/jbleuzen/node-cssmin)
with the default YUI configurations on each of them.


Build Status
------------

[![Build Status](https://secure.travis-ci.org/yui/yuglify.png?branch=master)](http://travis-ci.org/yui/yuglify)


CLI Usage
----------

    npm -g install yuglify

`yuglify` has a very simple CLI interface to allow you to compress files from the command line.

    yuglify ./lib/*.js #uses shell globbing, won't work on Windows

This will read all passed files and compress them (js or css) and write them back beside the original
with the name altered to `-min.js|css`.

Required
--------

    npm install yuglify


```javascript

var yuglify = require('yuglify');

yuglify.jsmin('<string of source', function(err, smashed) {
    fs.writeFile('/path/to/file', smashed, 'utf8', function() {});
});

yuglify.cssmin('<string of source', function(err, smashed) {
    fs.writeFile('/path/to/file', smashed, 'utf8', function() {});
});

```

Purpose
-------

This module is primarily designed to be used inside [shifter](http://yui.github.com/shifter/).

Why not use the default Uglify?
-------------------------------

We need to support the `/*!` license comment blocks when minifying, so we added
a preprocessor to the code to pull them from the source, then place them back when
the minification is complete.

We also needed to make sure that the file ends in a clean line ending for our
combo servers. This way we ensure that other modules don't have to end with a
semi-colon and the combohandler doesn't concat them together in a bad way.

We've also added support to add a semi-colon if the last character of the
minified source is either a `)` or a `}`.

The last thing this module does is provide the default config that we think
is the most compatible with the way that YUI Compressor used to minify our
files.

```javascript
{
    mangle: true,
    squeeze: true,
    semicolon: false,
    lift_vars: false,
    mangle_toplevel: true,
    no_mangle_functions: true,
    max_line_length: 6000
}
```

Testing
-------

Currently, the tests for this module are just to make sure that they are exported properly.
Shifter's test suite validates that these compressors are working as expected. Soon, we'll
move them over to this repo too.
