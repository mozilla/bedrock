define(function () {
    'use strict';

    var BaseModel = function () {
    };

    BaseModel.prototype._localize = function (localeData, area, id, attr) {
        var out = '';
        if (
            localeData &&
            localeData[area] &&
            localeData[area][id] &&
            localeData[area][id][attr]
        ) {
            out = localeData[area][id][attr];
        } else {
            out = [
                'WARN {unloc: ',
                area, ':',
                id, ':',
                attr, '}'
            ].join('');
        }
        return out;
    };

    return BaseModel;
});
