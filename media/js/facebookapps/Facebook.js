// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

// Facebook view class
DOWNLOADTAB.classes.Facebook = (function (singleton) {
    function Facebook (parametersObject) {
        var options = parametersObject || {};

        singleton.classes.Base.call (this);

        if (typeof options.startImmediately === 'undefined') {
            options.startImmediately = true;
        }

        if (typeof options.useUrlDialogs === 'undefined') {
            options.useUrlDialogs = false;
        }

        this.window = options.window;
        this.appId = options.appId;
        this.channelUrl = options.channelUrl;
        this.callback = options.callback;
        this.isImmediate = options.startImmediately;
        this.isUrlDialog = options.useUrlDialogs;

        this.isDebug = this._initData.isDev;
        this._initData = undefined;

        if (this.isImmediate) {
            this.start();
        }
    }

    Facebook.prototype = new singleton.classes.Base();
    Facebook.prototype.constructor = Facebook;

    Facebook.prototype.start = function() {
        var self = this;

        if (self.isUrlDialog) {
            self._invokeIfCallable(self.callback);
        } else {
            self.window.fbAsyncInit = function() {
                // init the FB JS SDK
                FB.init ({
                    appId: self.appId, // App ID from the App Dashboard
                    channelUrl: self.channelUrl, // Channel File for x-domain communication
                    status: true, // check the login status upon init?
                    cookie: true, // set sessions cookies to allow your server to access the session?
                    xfbml: true // parse XFBML tags on this page?
                });

                self._invokeIfCallable(self.callback);
            };

            // Load the SDK's source Asynchronously
            (function(d, debug){
               var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
               if (d.getElementById(id)) {return;}
               js = d.createElement('script'); js.id = id; js.async = true;
               js.src = '//connect.facebook.net/en_US/all' + (debug ? '/debug' : '') + '.js';
               ref.parentNode.insertBefore(js, ref);
            }(self.window.document, /*debug*/ self.isDebug));
        }
    };

    Facebook.prototype.getTabUrl = function(pageNamespace) {
        var self = this;
        return self.window.location.protocol + '//www.facebook.com/' + pageNamespace + '/app_' + self.appId;
    };

    Facebook.prototype.share = function(options, callback) {
        var self = this;
        self._dialog('feed', options, callback);
    };

    Facebook.prototype.invite = function(options, callback) {
        var self = this;
        self._dialog('apprequests', options, callback);
    };

    Facebook.prototype._dialog = function(dialogMethod, options, callback) {
        var self = this;
        var dialogUrl;
        options = options || {};
        options.show_error = self.isDebug;

        if (self.isUrlDialog) {
            options.app_id = self.appId;

            if (typeof callback === 'string') {
                options.redirect_uri = callback;
            } else {
                options.redirect_uri = self.window.location.href;
            }

            dialogUrl = '//www.facebook.com/dialog/' + dialogMethod + '/?';
            dialogUrl += self._objectToQueryString(options);

            self.window.top.location = dialogUrl;
        } else {
            options.method = dialogMethod;

            if (typeof options.callback !== 'function') {
                callback = undefined;
            }

            FB.ui(options, callback);
        }
    };


    // Utility methods
    //------------------------------------------
    Facebook.prototype._invokeIfCallable = function(fnCallableThing) {
        if (typeof fnCallableThing === 'function') {
            fnCallableThing();
        }
    };

    Facebook.prototype._objectToQueryString = function(argumentsObject) {
        var self = this;
        var urlEncode = self.window.encodeURIComponent;
        var fieldsArray = [];
        var field;
        var value;
        var queryString;

        for (field in argumentsObject) {
            value = argumentsObject[field];
            fieldsArray.push(urlEncode(field) + '=' + urlEncode(value));
        }

        queryString = fieldsArray.join('&');
        return queryString;
    };

    return Facebook;
} (DOWNLOADTAB));
