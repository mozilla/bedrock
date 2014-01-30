// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

// Theater class
DOWNLOADTAB.classes.Theater = (function (singleton) {
    function Theater($, doc) {
        singleton.classes.Base.call(this);

        this.$ = $;

        this.startingScene = '#' + this._initData.activeScene;
        this._initData = undefined;

        this.cache = {
            body: this.$(doc.body),
            stage: this.$('#stage'),
            scenes: this.$('.scene'),
            scene1: this.$('#scene1'),
            scene2: this.$('#scene2'),
            scene3: this.$('#scene3')
        };

        this.hashes = {
            scene1: '#',
            scene2: '#share',
            scene3: '#get-involved'
        };

        // Initialize Theater
        this.init();
    }

    // Initialize Base object and set correct constructor
    Theater.prototype = new singleton.classes.Base();
    Theater.prototype.constructor = Theater;

    // Class methods
    Theater.prototype.init = function() {
        var self = this;

        // Show scene from URL's hashes
        self.detectHash();
    };

    Theater.prototype.showScene = function(scene_shown) {
        var visible = this.getActiveScene();

        if (visible.length) {
            this.cache.body.removeClass('on-' + visible.attr('id'));
            visible.addClass('hidden');
        }

        this.cache.body.addClass('on-scene' + scene_shown);
        this.cache['scene' + scene_shown]
            .removeClass('hidden')
            .addClass('fadeInUp');
    };

    Theater.prototype.changeHash = function(scene_shown) {
        if (scene_shown !== 1) {
            location.hash = this.hashes['scene' + scene_shown];
        }
    };

    Theater.prototype.detectHash = function() {
        var sceneId = this.startingScene;

        if (sceneId === this.hashes.scene2) {
            this.showScene(2);
        } else if (sceneId === this.hashes.scene3) {
            this.showScene(3);
        } else {
            this.showScene(1);
        }
    };

    Theater.prototype.getActiveScene = function() {
        return this.cache.scenes.not('.hidden');
    };

    return Theater;
} (DOWNLOADTAB));
