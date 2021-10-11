/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

 (function() {
    'use strict';

    // Lazyload images
    Mozilla.LazyLoad.init();

    //event handlers for voting widget on article pages
    let hasVoted = false;
    const upvoteBtn = document.querySelector(".vpn-c-vote-btn.up");
    const downvoteBtn = document.querySelector(".vpn-c-vote-btn.down");

    function handleVote({target}) {
        const isUpvote = target.classList.contains('up');
        if (target.classList.contains('active') && hasVoted) {
            return null;
        } else {
            hasVoted = true;
            target.classList.add("active");
            if (isUpvote) {
                downvoteBtn.classList.remove("active")
            } else {
                upvoteBtn.classList.remove("active")
            }
        }
    }

    [upvoteBtn, downvoteBtn].forEach((element) => element.addEventListener("click", handleVote));


})();
