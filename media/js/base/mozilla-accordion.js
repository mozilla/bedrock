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

// {{{ Mozilla.Accordion

/**
 * Accordion widget
 *
 * @param jQueryObject $accordion - jQuery representation of element
 *          containing the accordion.
 * @param Object options - Object literal containing optional
 *          functionality:
 *              onExpand: function to execute when expanding
 *              onCollapse: function to execute when collapsing
 */
Mozilla.Accordion = function Accordion($accordion, options) {
    'use strict';

    // If the potential accordion has already been initialized, just return
    // a reference to the existing Mozilla.Accordion object.
    if ($accordion.hasClass('accordion-initialized')) {
        return Mozilla.Accordion.findAccordionById($accordion.prop('id'));
    }

    // Make sure the accordion container has an ID.
    if (!$accordion.prop('id')) {
        $accordion.prop('id', 'mozilla-accordion-' + Mozilla.Accordion.currentAccordionId);
        Mozilla.Accordion.currentAccordionId++;
    }

    // Mark accordion as initialized.
    $accordion.addClass('accordion-initialized');

    var accordionId = this.id = $accordion.prop('id');
    var sections = this.sections = [];
    var state = this.loadState() || {};

    // set callbacks for expand/collapse
    this.onExpand = null;
    this.onCollapse = null;

    if (typeof options === 'object') {
        if (typeof options.onExpand === 'function') {
            this.onExpand = options.onExpand;
        }

        if (typeof options.onCollapse === 'function') {
            this.onCollapse = options.onCollapse;
        }
    }

    // add ARIA attributes
    $accordion.attr({
        'role': 'tablist',
        'aria-multiselectable': 'true'
    });

    /// {{{ Section

    function Section(accordionId, index, $header) {
        var section = this;
        var $parent = $header.parent();
        var headerId = $header.prop('id');
        var panelId = $header.attr('aria-controls');

        this.accordionId = accordionId;

        // Use the parent node's ID or generate an unique ID
        this.id = (!$parent.is($accordion) && $parent.prop('id'))
                ? $parent.attr('id')
                : accordionId + '-' + (index + 1);

        if (!headerId) {
            headerId = this.id + '-header';
            $header.prop('id', headerId);
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

        // Store the title of the section for potential use in callbacks.
        this.title = this.$header.text();

        $header.on('focus.' + Mozilla.Accordion.EVENT_NAMESPACE + ' blur.' + Mozilla.Accordion.EVENT_NAMESPACE, function(event) {
            $header.attr('aria-selected', event.type === 'focus');
        });

        $header.on('click.' + Mozilla.Accordion.EVENT_NAMESPACE, function(event) {
            // Expand or close the section
            section.toggle(true, true);
            event.preventDefault();
        });

        $header.on('keydown.' + Mozilla.Accordion.EVENT_NAMESPACE, function(event) {
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
                next.$header.trigger('focus');
                event.preventDefault();
            }
        });

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

    // }}}
    // {{{ expand()

    Section.prototype.expand = function(animation, interaction) {
        var section = this;

        section.$panel.slideDown({
            'duration': (animation) ? 'fast' : 0,
            'easing': 'accordionExpand',
            'complete': function() {
                section.expanded = true;
                section.$header.attr('aria-expanded', 'true');
                section.$panel.attr('aria-hidden', 'false');
            }
        });

        if (interaction) {
            var accordion = Mozilla.Accordion.findAccordionById(this.accordionId);

            // If an expand callback has been specified, call it and pass the
            // expanding section as a param.
            if (typeof accordion.onExpand === 'function') {
                accordion.onExpand(this);
            }

            // If global expand listener is defined, call it.
            if (typeof Mozilla.Accordion.globalOnExpand === 'function') {
                Mozilla.Accordion.globalOnExpand(this);
            }

            // Fire a custom event on the panel
            section.$panel.trigger('expand');
        }
    };

    // }}}
    // {{{ collapse()

    Section.prototype.collapse = function(animation, interaction) {
        var section = this;

        section.$panel.slideUp({
            'duration': (animation) ? 'fast' : 0,
            'easing': 'accordionCollapse',
            'complete': function() {
                section.expanded = false;
                section.$header.attr('aria-expanded', 'false');
                section.$panel.attr('aria-hidden', 'true');
            }
        });

        if (interaction) {
            var accordion = Mozilla.Accordion.findAccordionById(this.accordionId);

            // If a collapse callback has been specified, call it and pass the
            // collapsing section as a param.
            if (typeof accordion.onCollapse === 'function') {
                accordion.onCollapse(this);
            }

            // If global collapse listener is defined, call it.
            if (typeof Mozilla.Accordion.globalOnCollapse === 'function') {
                Mozilla.Accordion.globalOnCollapse(this);
            }

            // Fire a custom event on the panel
            section.$panel.trigger('collapse');
        }
    };

    // }}}
    // {{{ toggle()

    Section.prototype.toggle = function(animation, interaction) {
        if (this.expanded) {
            this.collapse(animation, interaction);
        } else {
            this.expand(animation, interaction);
        }
    };

    // }}}

    // Find the header elements from grandchild nodes
    $('> * > [data-accordion-role="tab"]', $accordion).each(function(index) {
        sections.push(new Section(accordionId, index, $(this)));
    });

    Mozilla.Accordion.accordions.push(this);

    Mozilla.Accordion.updateBeforeUnloadListener();

    return this;
};

// }}}

Mozilla.Accordion.monitoringBeforeUnload = false;

Mozilla.Accordion.currentAccordionId  = 1;
Mozilla.Accordion.currentSectionId = 1;
Mozilla.Accordion.accordions = [];

Mozilla.Accordion.globalOnCollapse = null;
Mozilla.Accordion.globalOnExpand = null;
Mozilla.Accordion.EVENT_NAMESPACE = 'mozaccordion'; // targeted event (un)binding

// {{{ createAccordions()

/**
 * Initializes accordions.
 *
 * @param Boolean autoOnly - If true, only initializes accordions with
 *     'accordion-auto-init' class.
 */
Mozilla.Accordion.createAccordions = function(autoOnly) {
    'use strict';

    // Activate all auto-init accordions on the page
    $('.accordion').not('.accordion-initialized').each(function(index, accordionNode) {
        var $accordionNode = $(accordionNode);

        if ((autoOnly && $accordionNode.hasClass('accordion-auto-init')) || !autoOnly) {
            new Mozilla.Accordion($accordionNode);
        }
    });
};

// }}}
// {{{ findAccordionById()

Mozilla.Accordion.findAccordionById = function(accordionId) {
    'use strict';

    var accordion = $.grep(Mozilla.Accordion.accordions, function(elem) {
        return elem.id === accordionId;
    });

    return accordion.length > 0 ? accordion[0] : null;
};

// }}}
// {{{ expandAll ()

Mozilla.Accordion.prototype.expandAll = function(animation, interaction) {
    'use strict';

    $.each(this.sections, function(index, section) {
        section.expand(animation, interaction);
    });
};

// }}}
// {{{ collapseAll()

Mozilla.Accordion.prototype.collapseAll = function(animation, interaction) {
    'use strict';

    $.each(this.sections, function(index, section) {
        section.collapse(animation, interaction);
    });
};

// }}}
// {{{ loadState()

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

// }}}
// {{{ saveState()

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

// }}}
// {{{ updateBeforeUnloadMonitor()

Mozilla.Accordion.updateBeforeUnloadListener = function() {
    'use strict';

    if (Mozilla.Accordion.accordions.length === 0) {
        $(window).off('beforeunload.' + Mozilla.Accordion.EVENT_NAMESPACE);

        Mozilla.Accordion.monitoringBeforeUnload = false;
    } else if (Mozilla.Accordion.monitoringBeforeUnload === false) {
        // Save the expanded/collapsed state before the user leaves the page
        $(window).on('beforeunload.' + Mozilla.Accordion.EVENT_NAMESPACE, function() {
            $.each(Mozilla.Accordion.accordions, function(index, accordion) {
                accordion.saveState();
            });
        });

        Mozilla.Accordion.monitoringBeforeUnload = true;
    }
};

// }}}
// {{{ destroyAccordions()

Mozilla.Accordion.destroyAccordions = function() {
    'use strict';

    var accordionIds = [];
    var i;

    for (i = 0; i < Mozilla.Accordion.accordions.length; i++) {
        accordionIds.push(Mozilla.Accordion.accordions[i].id);
    }

    for (i = 0; i < accordionIds.length; i++) {
        Mozilla.Accordion.destroyAccordionById(accordionIds[i]);
    }
};

// {{{ destroyAccordionById()

Mozilla.Accordion.destroyAccordionById = function(accordionId) {
    'use strict';

    var accordion = Mozilla.Accordion.findAccordionById(accordionId);

    if (!accordion) {
        return false;
    }

    // save accordion state
    accordion.saveState();

    // reference to accordion container element
    var $container = $('#' + accordion.id);

    // remove ARIA stuff
    $container.removeAttr('role aria-multiselectable');

    // for each section
    var section;
    for (var i = 0; i < accordion.sections.length; i++) {
        section = accordion.sections[i];

        // remove ARIA from header
        section.$header.removeAttr('aria-controls tabindex aria-selected aria-expanded role');

        // remove event listeners from header
        section.$header.off('.' + Mozilla.Accordion.EVENT_NAMESPACE);

        // remove ARIA from panel & make visible
        section.$panel.removeAttr('role aria-labelledby aria-hidden').show();
    }

    // remove initialized class
    $container.removeClass('accordion-initialized');

    // remove from array of accordions
    var accordionIndex = $.inArray(accordion, Mozilla.Accordion.accordions);
    Mozilla.Accordion.accordions.splice(accordionIndex, 1);

    Mozilla.Accordion.updateBeforeUnloadListener();

    return true;
};

// }}}

$(function() {
    'use strict';

    // Discard old browsers, notably IE6 and IE7, where CSS attribute selectors
    // are not properly supported. The content looks plain but is totally
    // accessible.
    if (/MSIE\s[1-7]\./.test(navigator.userAgent)) {
        return;
    }

    // Add easing functions
    $.extend($.easing, {
        'accordionExpand': function (x) {
            return 1 * Math.pow(x, 2);
        },
        'accordionCollapse': function (x) {
            return -1 * x * (x - 2);
        }
    });

    // Activate all auto-init accordions on the page
    Mozilla.Accordion.createAccordions(true);
});
