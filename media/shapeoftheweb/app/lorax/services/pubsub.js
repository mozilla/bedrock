define(['jquery'], function ($) {
    'use strict';

    var PubSubFactory = function () {
        var cache = {};

        return {
            publish: function (topic, args) {
                cache[topic] && $.each(cache[topic], function () {
                    this.apply(null, args || []);
                });
            },

            subscribe: function (topic, callback) {
                if (!cache[topic]) {
                    cache[topic] = [];
                }
                cache[topic].push(callback);
                return [topic, callback];
            },

            unsubscribe: function (handle) {
                var t = handle[0];
                cache[t] && $.each(cache[t], function (idx) {
                    (this === handle[1]) && cache[t].splice(idx, 1);
                });
            }
        };
    };

    return PubSubFactory;
});
