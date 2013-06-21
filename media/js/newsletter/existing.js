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
    $form.find('input[name^="form-"][name$="-subscribed"]:checked').each(function () {
      var newsletterInputName = $(this).attr('name').replace("-subscribed", "-newsletter");
      var newsletter = $("input[name='" + newsletterInputName + "']").val();
      if (initialNewsletters.indexOf(newsletter) === -1) {
        // newly subscribed to this newsletter
        events.push(['_trackEvent', 'Newsletter Registration', 'submit', newsletter]);
      }
    });
    if (gaTrack && events.length > 0) {
      gaTrack(events, function () { $form.submit(); });
    } else {
      $form.submit();
    }
  };

  $('form#existing-newsletter-form').on('submit', handler);
});
