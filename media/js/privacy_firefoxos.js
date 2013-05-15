$(function() {

    var $panels = $('section');
    var $anchors = $('main a');
    var $success = $('.success');
    var $submission_state = $success.data('submission-state');

    // If the submission state is True it means that our form
    // was submitted, passed validation and the page has reloaded.
    // This means we need to ensure the page transitions to the contact
    // panel that contains the success message.
    if($submission_state === "True") {
        var contactPanel = $('#contact');

        deactivatePanels();

        // We need to move the success message do a different location
        // in the DOM so that it is above the fold when the below
        // transition happens.
        $success.insertBefore($('#introtxt'));

        contactPanel.addClass('active');
    }

    function deactivatePanels() {
        $panels.each(function() {
            $(this).removeClass('active');
        });
    }

    function setText($elem) {
        var currentTxt = $elem.text();
        if(currentTxt === 'Learn More') {
            $elem.text('Show Less');
        } else {
            $elem.text('Learn More');
        }
    }

    // Handle all click events
    $anchors.click(function(event) {
        var $anchor = $(this);
        var elementID = $anchor.data('panelid');
        var txtContent = $anchor.text();
        var $currentElement = $(elementID);

        if(txtContent === 'Learn More' ||
                txtContent === 'Show Less') {
            // We only want to prevent default for these links
            // for the others, the default behavior is required.
            event.preventDefault();
            setText($anchor);
            $currentElement.toggle();
        } else {
            deactivatePanels();
            $currentElement.addClass('active');
        }
    });
});
