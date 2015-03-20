// //Deprecated tracking for twitter interaction on Student Ambassador Page, 
// //replaced with data-attr's and GTM

// $(function() {
//   // GA event tracking
//   function _track(event, cmd) {
//     if (event.target.target === '_blank' || event.metaKey || event.ctrlKey) {
//       // New tab
//       window.dataLayer = window.dataLayer || [];
//       window.dataLayer.push(cmd);
//     } else {
//       // Current tab
//       event.preventDefault();
//       cmd.eventCallback = function() { window.location.href = event.currentTarget.href;}
//       window.dataLayer = window.dataLayer ||[];
//       window.dataLayer.push(cmd);
//     }
//   }

//   // Twitter Follow button
//   $('.twitter-follow-button').on('click', function(event) {
//     _track(event, {event: 'twitter-interaction', socialAction: 'Twitter Follow'});
//   });

//   // Twitter timeline widget
//   $('#twitter-timeline-widget').on('click', 'a', function(event) {
//     if ($(this).hasClass('twitter-follow-button')) {
//       return; // Tracking will be done by the function above
//     }
//     _track(event, {event: 'twitter-interaction', socialAction: 'Twitter ' + ({
//       'post': 'Post Link Exit',
//       'author': 'Author Link Exit',
//       'credit': 'Retweet Credit Link Exit',
//       'image': 'Preview Image Exit',
//       'hash': 'Hashtag Link Exit',
//       'mention': 'Mention Link Exit',
//       'media': 'Media Link Exit',
//       'reply': 'Reply',
//       'retweet': 'Retweet',
//       'favorite': 'Favorite'
//     }[$(this).attr('class')] || 'General Link Exit')});
//   });
// });
