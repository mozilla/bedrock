/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const fs = require('fs');
const path = require('node:path');
const im = require('node-imagemagick');
let imgFile = process.argv[2]; // get first argument passed to script
let sizesCSV = process.argv[3]; // get second argument passed to script
let sizes = [];
let srcset = ''; // collect declarations here as we create image sizes

if (!sizesCSV) {
    // eslint-disable-next-line no-console
    console.log('Error: please provide a list of desired sizes');
    return;
} else {
    sizes = sizesCSV.split(',').map(Number); // make intro array of numbers (not strings)
}

// check it is a file
if (fs.existsSync(imgFile)) {
    let imgPath = path.resolve(imgFile); // local path to file
    imgPath = path.parse(imgPath);
    let imgSrcDir = imgPath.dir.split('bedrock/media/')[1]; // path to file for img src purposes

    im.identify(['-format', '%w', imgFile], function (err, output) {
        if (err)
            throw (
                'Error: not able to identify image width. Full error: \n' + err
            );
        let imgWidth = output;

        for (var size of sizes) {
            // only resize to sizes the source file is bigger than
            if (imgWidth >= size) {
                let newPath =
                    imgPath.dir + '/' + imgPath.name + '-' + size + imgPath.ext;
                let newSrc =
                    imgSrcDir + '/' + imgPath.name + '-' + size + imgPath.ext;
                // resize and save
                im.convert([imgFile, '-resize', size, newPath], function (err) {
                    if (err) throw err;
                });
                // add entry to srcset text
                srcset += '\t"' + newSrc + '": "' + size + 'w",\n';
            } else {
                // eslint-disable-next-line no-console
                console.log(
                    'Error: source file is not big enough to make versions larger than ' +
                        imgWidth +
                        'px.'
                );
                return;
            }
        }
        // eslint-disable-next-line no-console
        console.log('srcset={\n' + srcset + '},');

        // eslint-disable-next-line no-console
        console.log("\n\nDon't forget to optimize these with img-opt.sh!");
    });
} else {
    // eslint-disable-next-line no-console
    console.log('Error: could not find file.');
}
