/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

 (function() {
    'use strict';

    // Lazyload images
    Mozilla.LazyLoad.init();

    //event handlers for voting widget on article pages
    var hasVoted = false;
    var upvoteBtn = document.querySelector(".vpn-c-vote-btn.up");
    var downvoteBtn = document.querySelector(".vpn-c-vote-btn.down");

    function handleVote(e) {
        var el = e.target;
        var isUpvote = el.classList.contains('up')
        if (el.classList.contains('active')) {
            return null;
        } else {
            el.classList.add("active");
            if (isUpvote) {
                downvoteBtn.classList.remove("active")
            } else {
                upvoteBtn.classList.remove("active")
            }
        }
    }

    [upvoteBtn, downvoteBtn].forEach(function(element) {
        element.addEventListener("click", handleVote)
    });


})();
