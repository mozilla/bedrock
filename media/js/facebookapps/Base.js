// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

// Base parent class
// Exposes references to singleton's properties
DOWNLOADTAB.classes.Base = (function (singleton) {
    function Base(){}
    Base.prototype._initData = singleton.initData;
    Base.prototype._classes = singleton.classes;

    return Base;
} (DOWNLOADTAB));
