/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Portions adapted from the jQuery Easing plugin written by Robert Penner and
 * used under the following license:
 *
 *   Copyright 2001 Robert Penner
 *   All rights reserved.
 *
 *   Redistribution and use in source and binary forms, with or without
 *   modification, are permitted provided that the following conditions are
 *   met:
 *
 *   - Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *   - Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *   - Neither the name of the author nor the names of contributors may be
 *     used to endorse or promote products derived from this software without
 *    specific prior written permission.
 *
 *   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 *   TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 *   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 *   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 *   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 *   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 *   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 *   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 *   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

// Create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

Mozilla.Accordion = function Accordion (index, $accordion) {
    'use strict';

    var accordionId = this.id = $accordion.attr('id') ||
                                'moz-accordion-' + (index + 1);
    var sections = this.sections = [];
    var state = this.loadState() || {};

    // add ARIA attributes
    $accordion.attr({
        'role': 'tablist',
        'aria-multiselectable': 'true'
    });

    function Section (index, $header) {
        var section = this;
        var $parent = $header.parent();
        var headerId = $header.attr('id');
        var panelId = $header.attr('aria-controls');

        // Use the parent node's ID or generate an unique ID
        this.id = (!$parent.is($accordion) && $parent.attr('id'))
                ? $parent.attr('id')
                : accordionId + '-' + (index + 1);

        if (!headerId) {
            headerId = this.id + '-header';
            $header.attr('id', headerId);
        }

        // Get the panel
        if (panelId) {
            this.$panel = $('#' + panelId).attr({
                'aria-labelledby': headerId,
                'role': 'tabpanel'
            });
        } else {
            panelId = this.id + '-panel';
            $header.attr('aria-controls', panelId);
            this.$panel = $header.siblings('[data-accordion-role="tabpanel"]:first').attr({
                'id': panelId,
                'role': 'tabpanel',
                'aria-labelledby': headerId
            });
        }

        // Activate the header
        this.$header = $header.attr({
            'tabindex': '0',
            'aria-selected': 'false',
            'aria-expanded': 'false',
            'role': 'tab'
        });

        $header.on('focus blur', function(event) {
            $header.attr('aria-selected', event.type === 'focus');
        });

        $header.on('click', function(event) {
            // Expand or close the section
            section.toggle(true, true);
            event.preventDefault();
        });

        $header.on('keydown', function(event) {
            var next;
            var len = sections.length;

            switch (event.which) {
                case 13: // Space
                case 32: // Enter or Return
                    // Expand or close the section
                    section.toggle(true, true);
                    event.preventDefault();
                    break;

                case 33: // Page Up
                case 36: // Home
                    // Find the first section in the accordion
                    next = sections[0];
                    break;

                case 34: // Page Down
                case 35: // End
                    // Find the last section in the accordion
                    next = sections[len - 1];
                    break;

                case 37: // Left Arrow
                case 38: // Up Arrow
                    // Find the previous or last section in the accordion
                    next = sections[(index === 0) ? len - 1 : index - 1];
                    break;

                case 39: // Right Arrow
                case 40: // Down Arrow
                    // Find the next or first section in the accordion
                    next = sections[(index === len - 1) ? 0 : index + 1];
                    break;
            }

            if (next) {
                // Manage focus
                next.$header.focus();
                event.preventDefault();
            }
        });

        // Append a controller if needed
        if (trans('accordion-expand')) {
            this.$headerController = $('<span role="presentation"></span>')
                                       .appendTo($header);
        }

        // Determine if the panel should be expanded or collapsed by checking
        // 1. the aria-expanded state on the header
        // 2. the URL hash string
        // 3. the saved state in session storage
        if ($header.attr('aria-expanded') === 'true' ||
                location.hash.substr(1) === this.id ||
                state[this.id] === true) {
            this.expand(false, false);
        } else {
            this.collapse(false, false);
        }
    }

    Section.prototype.expand = function(animation, interaction) {
        var section = this;

        section.$panel.slideDown({
            'duration': (animation) ? 'fast' : 0,
            'easing': 'accordionExpand',
            'complete': function() {
                section.expanded = true;
                section.$header.attr('aria-expanded', 'true');
                section.$panel.attr('aria-hidden', 'false');

                if (section.$headerController) {
                    section.$headerController.text(trans('accordion-collapse'));
                }
            }
        });

        if (interaction) {
            // Google Analytics event tracking
            gaTrack([
                '_trackEvent',
                location.pathname + ' Accordion Interactions',
                'Expand',
                section.$header.text()
            ]);
        }
    };

    Section.prototype.collapse = function(animation, interaction) {
        var section = this;

        section.$panel.slideUp({
            'duration': (animation) ? 'fast' : 0,
            'easing': 'accordionCollapse',
            'complete': function() {
                section.expanded = false;
                section.$header.attr('aria-expanded', 'false');
                section.$panel.attr('aria-hidden', 'true');

                if (section.$headerController) {
                    section.$headerController.text(trans('accordion-expand'));
                }
            }
        });

        if (interaction) {
            // Google Analytics event tracking
            gaTrack([
                '_trackEvent',
                location.pathname + ' Accordion Interactions',
                'Collapse',
                section.$header.text()
            ]);
        }
    };

    Section.prototype.toggle = function(animation, interaction) {
        if (this.expanded) {
            this.collapse(animation, interaction);
        } else {
            this.expand(animation, interaction);
        }
    };

    // Find the header elements from grandchild nodes
    $('> * > [data-accordion-role="tab"]', $accordion).each(function(index) {
        sections.push(new Section(index, $(this)));
    });
};

Mozilla.Accordion.prototype.expandAll = function(animation, interaction) {
    'use strict';

    $.each(this.sections, function(index, section) {
        section.expand(animation, interaction);
    });
};

Mozilla.Accordion.prototype.collapseAll = function(animation, interaction) {
    'use strict';

    $.each(this.sections, function(index, section) {
        section.collapse(animation, interaction);
    });
};

Mozilla.Accordion.prototype.loadState = function() {
    'use strict';

    var itemId = location.pathname + '#' + this.id;

    try {
        return JSON.parse(sessionStorage.getItem(itemId));
    } catch (ex) {
        // sessionStorage or cookie is not supported or disabled
        return null;
    }
};

Mozilla.Accordion.prototype.saveState = function() {
    'use strict';

    var state = {};
    var itemId = location.pathname + '#' + this.id;

    $.each(this.sections, function(index, section) {
        state[section.id] = section.expanded;
    });

    try {
        sessionStorage.setItem(itemId, JSON.stringify(state));
    } catch (ex) {
        // sessionStorage or cookie is not supported or disabled
    }
};

$(function() {
    'use strict';

    // Discard old browsers, notably IE6 and IE7, where CSS attribute selectors
    // are not properly supported. The content looks plain but is totally
    // accessible.
    if (/MSIE\s[1-7]\./.test(navigator.userAgent)) {
        return;
    }

    var accordions = [];

    // Add easing functions
    $.extend($.easing, {
        'accordionExpand': function (x, t, b, c, d) {
            return c * (t /= d) * t + b;
        },
        'accordionCollapse': function (x, t, b, c, d) {
            return -c * (t /= d) * (t - 2) + b;
        }
    });

    // Activate all accordions on the page
    $('.accordion').each(function(index) {
        var accordion = new Mozilla.Accordion(index, $(this));
        $(this).data('widget', accordion).addClass('activated');
        accordions.push(accordion);
    });

    // Save the expanded/collapsed state before the user leaves the page
    $(window).on('beforeunload', function() {
        $.each(accordions, function(index, accordion) {
            accordion.saveState();
        });
    });
});
