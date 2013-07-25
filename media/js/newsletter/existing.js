/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Tell GA if user subscribed to anything new
jQuery(function($) {
  var handler = function (e) {
    e.preventDefault();
    var $form = $(this);
    $form.unbind('submit', handler);

    // get the newsletters they're already subscribed to
    // from the form's data-initial-newsletters attribute.
    var initialNewsletters = $form.data('initialNewsletters');
    var events = [];
    var processed_newsletters = '';

    // loop through all newsletters
    $form.find('input[name^="form-"][name$="-subscribed"]').each(function () {
      var $this = $(this);
      var newsletterInputName = $this.attr('name').replace("-subscribed", "-newsletter");
      var newsletter = $("input[name='" + newsletterInputName + "']").val();

      // make sure we haven't already looked at radio buttons associated with this newsletter
      if (processed_newsletters.indexOf(newsletter) === -1) {
        // find value of checked radio button within this set
        // True = subscribed, False = unsubscribed
        var subscribed = $('input[name="' + $this.attr('name') + '"]:checked').val();

        // if newsletter is checked and wasn't previously subscribed to, track the subscription
        if (subscribed === 'True' && initialNewsletters.indexOf(newsletter) === -1) {
          // newly subscribed to this newsletter
          events.push(['_trackEvent', 'Newsletter Registration', 'subscribe', newsletter]);
        // if newsletter is not checked and was previously subscribed to, track the unsubscription
        } else if (subscribed === 'False' && initialNewsletters.indexOf(newsletter) > -1) {
          // newly unsubscribed to this newsletter
          events.push(['_trackEvent', 'Newsletter Registration', 'unsubscribe', newsletter]);
        }

        // make sure we don't re-process this newsletter
        processed_newsletters += ',' + newsletter;
      }
    });

    if (typeof(gaTrack) === 'function' && events.length > 0) {
      // make GA call for each event
      $.each(events, function(i, evt) {
        // if the last event, add callback to submit the form
        if (i === (events.length - 1)) {
          gaTrack(evt, function() { $form.submit(); });
        } else {
          gaTrack(evt);
        }
      });
    } else {
      $form.submit();
    }
  };

  $('form#existing-newsletter-form').on('submit', handler);
});
