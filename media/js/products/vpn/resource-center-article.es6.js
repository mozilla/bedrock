/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

//event handlers for voting widget on article pages
const upvoteBtn = document.querySelector('.vpn-c-vote-btn.up');
const downvoteBtn = document.querySelector('.vpn-c-vote-btn.down');

function trackVoteInteraction(url, vote) {
    // UA
    window.dataLayer.push({
        event: 'vpn-article-vote',
        label: url,
        value: vote
    });
    // GA4
    window.dataLayer.push({
        event: 'widget_action',
        type: 'vote',
        action: vote,
        label: 'Was this article helpful?'
    });
}

function handleVote({ target }) {
    const isUpvote = target.classList.contains('up');
    if (upvoteBtn.ariaPressed || downvoteBtn.ariaPressed) {
        return null;
    } else {
        trackVoteInteraction(
            target.getAttribute('data-cta-text'),
            isUpvote ? 'helpful' : 'not helpful'
        );
        if (isUpvote) {
            upvoteBtn.setAttribute('aria-pressed', true);
            downvoteBtn.removeAttribute('aria-pressed');
        } else {
            downvoteBtn.setAttribute('aria-pressed', true);
            upvoteBtn.removeAttribute('aria-pressed');
        }
    }
}

[upvoteBtn, downvoteBtn].forEach((element) =>
    element.addEventListener('click', handleVote, false)
);
