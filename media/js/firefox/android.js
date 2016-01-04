/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    var isOldIE = (/MSIE\s[1-7]\./.test(navigator.userAgent));

    // slideshow/accordion variables
    var customizeAccordion;
    var $accordionElem = $('#customize-accordion');
    var $phoneWrapper = $('#phone-wrapper');
    var $screencastWrapper = $('#screencast-wrapper');
    var $phoneScreens = $('#phone-screens');
    var $screencastImages = $('#screencast-images');
    var $slideshows = $('.slideshow');
    var $pagerButtons = $('.customize-pager');
    var screencastVisible = false;
    var slideshowRunning = false;
    var cycleOpts = {
        speed: 450,
        timeout: 2000
    };

    // send to device vars
    var hasWidget = $('#intro').data('hasWidget') !== 'False';
    var sendToDeviceWidget;
    var sendToDeviceWidgetTop;

    // move screencast images into the slideshow container
    $screencastImages.append($('#screencast .media-desktop').html());

    // hide download buttons from Android users
    if (Mozilla.Client.isFirefoxAndroid) {
        $('.dl-button-wrapper').hide();

        $('#subscribe-wrapper').removeClass('floating');
    }

    // stops any running slideshow
    var stopSlideshow = function() {
        // stop slideshow
        if (slideshowRunning) {
            $slideshows.cycle('destroy');
            slideshowRunning = false;
        }
    };

    var startPhoneScreenSlideshow = function(sectionId) {
        // if new markup has more than one image, start a slideshow
        if ($phoneScreens.children('img').length > 1) {
            // addons/faves should slide while others (search) should fade
            cycleOpts.fx = (sectionId === 'addons') ? 'scrollHorz' : 'fade';

            $phoneScreens.cycle(cycleOpts);

            slideshowRunning = true;
        }
    };

    var startScreencastSlideshow = function() {
        // make sure fx is set to 'fade'
        cycleOpts.fx = 'fade';

        $screencastImages.cycle(cycleOpts);

        slideshowRunning = true;
    };

    // replaces content of phone container with specified image(s)
    var setPhoneScreen = function(markup, sectionId) {
        // processing for all sections except screencast
        if (sectionId !== 'screencast') {
            $phoneScreens.empty().append(markup);

            // if currently displaying screencasts, fade out/in wrappers
            if (screencastVisible) {
                $screencastWrapper.stop().fadeOut('fast', function() {
                    stopSlideshow();

                    $phoneWrapper.stop().fadeIn('fast');

                    startPhoneScreenSlideshow(sectionId);
                });

                screencastVisible = false;
            } else {
                stopSlideshow();

                startPhoneScreenSlideshow(sectionId);
            }
        } else {
            if (!screencastVisible) {
                $phoneWrapper.stop().fadeOut('fast', function() {
                    stopSlideshow();

                    $screencastWrapper.stop().fadeIn('fast');

                    // we know screencast should have a slideshow
                    startScreencastSlideshow();
                });

                screencastVisible = true;
            } else {
                stopSlideshow();

                // we know screencast should have a slideshow
                startScreencastSlideshow();
            }

            slideshowRunning = true;
        }
    };

    var initAccordionsDesktop = function() {
        customizeAccordion = new Mozilla.Accordion($accordionElem);
        var hasExpanded = -1;

        // if no accordions are open, open the first section
        for (var i = 0; i < customizeAccordion.sections.length; i++) {
            if (customizeAccordion.sections[i].expanded) {
                hasExpanded = i;
                break;
            }
        }

        // if no section is expanded from previous visit
        if (hasExpanded === -1) {
            // open first section
            customizeAccordion.sections[0].expand();

            // display phone wrapper
            $phoneWrapper.fadeIn('fast');

            // update phone screen
            setPhoneScreen($('#broadcast').find('.media-desktop').html());
        } else {
            // if going from mobile view, multiple sections could be expanded
            // make sure only the first stays expanded - collapse the rest
            var section;

            for (var j = 0; j < customizeAccordion.sections.length; j++) {
                section = customizeAccordion.sections[j];

                if (section.expanded && j !== hasExpanded) {
                    section.collapse();
                }
            }

            // update phone screen to match auto-expanded section
            var $expandedSection = $('#' + customizeAccordion.sections[hasExpanded].id);

            // if not showing screencast section on page load, fade in phone wrapper
            if ($expandedSection.prop('id') !== 'screencast') {
                $phoneWrapper.fadeIn('fast');
            }

            setPhoneScreen($expandedSection.find('.media-desktop').html(), $expandedSection.prop('id'));
        }

        // add custom handlers to accordion tabs
        $('.accordion [data-accordion-role="tab"]').on('click.android-desktop', function() {
            var $tab = $(this);

            // only take action when expanding a new section
            if ($tab.attr('aria-expanded') === 'false') {
                var section;
                var $tabParent = $tab.parent();

                // update the phone images
                setPhoneScreen($tabParent.find('.media-desktop').html(), $tabParent.prop('id'));

                // if a section is already expanded, collapse it
                for (var i = 0; i < customizeAccordion.sections.length; i++) {
                    section = customizeAccordion.sections[i];

                    // set the min-height of the accordion to current height
                    // before collapsing section to avoid page height jump.
                    $accordionElem.css('min-height', $accordionElem.height());

                    if (section.expanded) {
                        section.collapse();
                    }
                }
            }
        });

        // click listener for pager arrows
        $pagerButtons.on('click', function() {
            // make sure pager is available (disabled during transitions)
            if (!$pagerButtons.prop('disabled')) {
                $pagerButtons.prop('disabled', true);
                var $this = $(this);
                var currentlyExpanded = 0;
                var nextExpanded;

                // find currently expanded section, if any
                for (var i = 0; i < customizeAccordion.sections.length; i++) {
                    section = customizeAccordion.sections[i];

                    if (section.expanded) {
                        currentlyExpanded = i;
                        break;
                    }
                }

                if ($this.prop('id') === 'customize-prev') {
                    nextExpanded = (currentlyExpanded === 0) ? customizeAccordion.sections.length - 1 : currentlyExpanded - 1;
                } else {
                    nextExpanded = (currentlyExpanded === (customizeAccordion.sections.length - 1)) ? 0 : currentlyExpanded + 1;
                }

                $('#' + customizeAccordion.sections[nextExpanded].id).find('[data-accordion-role="tab"]').trigger('click');

                // prevent UI busting from spamming pager arrows
                setTimeout(function() {
                    $pagerButtons.prop('disabled', false);
                }, 600);
            }
        });

        $pagerButtons.prop('disabled', false);
    };

    var initAccordionsMobile = function() {
        // remove desktop bindings
        $('.accordion [data-accordion-role="tab"]').off('click.android-desktop');
        $('.customize-pager').off('click');

        customizeAccordion = new Mozilla.Accordion($accordionElem);
    };

    // fire sync animation when scrolled to
    $('#sync').waypoint(function() {
        Mozilla.syncAnimation();
        this.destroy(); // only execute waypoint once
    }, {
        offset: '50%'
    });

    // if not IE 7 or older, initialize the page
    if (!isOldIE) {
        if (typeof matchMedia !== 'undefined') {
            var queryMobileViewport = matchMedia('(max-width: 760px)');

            // listen for viewport resize
            queryMobileViewport.addListener(function(mq) {
                if (mq.matches) {
                    Mozilla.Accordion.destroyAccordions();
                    stopSlideshow();
                    initAccordionsMobile();
                } else {
                    initAccordionsDesktop();
                }
            });

            if (queryMobileViewport.matches) {
                initAccordionsMobile();
            } else {
                initAccordionsDesktop();
            }
        } else {
            // attempt to be reasonably sure user is on a mobile device
            if (window.screen.width <= 760) {
                initAccordionsMobile();
            } else {
                initAccordionsDesktop();
            }
        }
    }

    // track link on the primary CTA
    $('#intro .dl-button').attr({
        'data-interaction': 'download click',
        'data-download-version': 'Firefox for Android'
    });

    // track link on the secondary CTA
    $('#subscribe-download-wrapper .dl-button').attr({
        'data-interaction': 'button download click',
        'data-download-version': 'Firefox for Android'
    });

    // track links except the accordion
    $('#privacy, #sync, #subscribe-download-wrapper ul').attr({
        'data-interaction': 'link click',
        'data-download-version': 'href'
    });

    if (hasWidget) {
        sendToDeviceWidgetTop = $('#send-to-device').offset().top;
        sendToDeviceWidget = new Mozilla.SendToDevice();
        sendToDeviceWidget.init();

        // add hidden input to update basket id
        $('#send-to-device-form').append('<input type="hidden" name="send-to-device-basket-id" value="android-embed">');

        // wire nav/footer links to scroll to widget
        $('.send-to').on('click', function(e) {
            e.preventDefault();

            Mozilla.smoothScroll({
                top: sendToDeviceWidgetTop - 100
            });
        });
    }
})(window.jQuery, window.Mozilla);
