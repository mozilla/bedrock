/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// Lazyload images
Mozilla.LazyLoad.init();

//event handlers for voting widget on article pages
let hasVoted = false;
const upvoteBtn = document.querySelector('.vpn-c-vote-btn.up');
const downvoteBtn = document.querySelector('.vpn-c-vote-btn.down');

function trackVoteInteraction(url, vote) {
    window.dataLayer.push({
        event: 'vpn-article-vote',
        label: url,
        value: vote
    });
}

function handleVote({ target }) {
    const isUpvote = upvoteBtn.contains(target);
    if (
        ((isUpvote && upvoteBtn.classList.contains('active')) ||
            (!isUpvote && downvoteBtn.classList.contains('active'))) &&
        hasVoted
    ) {
        return null;
    } else {
        hasVoted = true;
        trackVoteInteraction(
            target.getAttribute('data-cta-text'),
            isUpvote ? 'helpful' : 'not helpful'
        );
        if (isUpvote) {
            upvoteBtn.classList.add('active');
            downvoteBtn.classList.remove('active');
        } else {
            downvoteBtn.classList.add('active');
            upvoteBtn.classList.remove('active');
        }
    }
}

[upvoteBtn, downvoteBtn].forEach((element) =>
    element.addEventListener('click', handleVote, false)
);
