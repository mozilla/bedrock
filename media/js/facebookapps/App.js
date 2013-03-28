// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

// Main app class
DOWNLOADTAB.classes.App = (function (singleton) {
    function App ($, win) {
        singleton.classes.Base.call (this);

        this.$ = $;
        this.window = win;

        this.appId = this._initData.appId;
        this.pageNamespace = this._initData.pageNamespace;
        this.tabRedirectUrl = this.absoluteUrl(this._initData.tabRedirectPath);
        this.shareImageUrl = this.absoluteUrl(this._initData.shareImagePath);
        this._initData = undefined;
    }

    App.prototype = new singleton.classes.Base();
    App.prototype.constructor = App;

    App.prototype.domInit = function() {
        var self = this;
        var path_parts = self.window.location.pathname.split('/');
        var referrer = path_parts[path_parts.length - 2];

        self.locale = path_parts[1];
        self.virtualUrl = '/' + self.locale + '/products/download.html?referrer=' + referrer;

        self.setupDownloadLinks();

        self.theater = new self._classes.Theater(self.$, self.window.document);
        self.slider = new self._classes.Slider(self.$, '#slider-container');
    };

    App.prototype.facebookInit = function() {
        var self = this;

        self.$(function() {
            var redirectUrl = self.tabRedirectUrl + '?scene=get-involved';

            self.$('.js-share').on('click', function(event) {
                event.preventDefault();

                self.facebook.share({
                    link: self.facebook.getTabUrl(self.pageNamespace),
                    picture: self.shareImageUrl,
                    name: trans('app-title'),
                    caption: trans('share-caption'),
                    description: trans('share-description')
                }, redirectUrl);
            });

            self.$('.js-invite').on('click', function(event) {
                event.preventDefault();

                self.facebook.invite({
                    title: trans('invite-title'),
                    message: trans('invite-message'),
                    data: 'tab-invite'
                }, redirectUrl);
            });
        });
    };

    App.prototype.startApp = function() {
        var self = this;

        self.facebook = new self._classes.Facebook ({
            window: self.window,
            appId: self.appId,
            useUrlDialogs: true,
            callback: function() {
                self.facebookInit();
            }
        });

        self.$(function() {
            self.domInit();
        });
    };

    App.prototype.setupDownloadLinks = function() {
        var self = this;

        // Pull Firefox download link from the download button and add to
        // the 'click here' link.
        // TODO: Remove and generate link in bedrock.
        $('#direct-download-link').attr(
            'href', $('.download-list li:visible .download-link').attr('href')
        );

        $('#direct-download-link, .download-link').on('click', function(event) {
            var $activeScene;
            var downloadUrl;

            event.preventDefault();

            downloadUrl = $(event.currentTarget).attr('href');
            self.trackRedirect(downloadUrl, this.virtualUrl);

            $activeScene = self.theater.getActiveScene();

            if ($activeScene.attr('id') !== 'scene2') {
                self.theater.showScene(2);
            }
        });
    };

    App.prototype.getBaseUrl = function (options) {
        var protocol = '';
        var port = '';
        options = options || {};

        if (options.protocol === true) {
            protocol = this.window.location.protocol;
        } else if (options.protocol && typeof options.protocol === 'string') {
            protocol = options.protocol;
        }

        if (this.window.location.port) {
            port = ':' + this.window.location.port;
        }

        return protocol + '//' + this.window.location.hostname + port;
    };

    App.prototype.absoluteUrl = function(relativeUrl) {
        var self = this;
        return self.getBaseUrl({ protocol: true }) + relativeUrl;
    };

    App.prototype.trackRedirect = function(url, virtualUrl) {
        var self = this;
        virtualUrl = virtualUrl || url;

        if (!self.window._gat) {
            self.redirect(url);
        }

        self.window._gaq.push(['_trackPageview', virtualUrl]);
        self.window._gaq.push(function() {
            self.redirect(url);
        });
    };

    App.prototype.redirect = function(url, options) {
        var self = this;
        options = options || {};

        if (options.top) {
            self.window.top.location.href = url;
        } else {
            self.window.location.href = url;
        }
    };

    return App;
} (DOWNLOADTAB));
