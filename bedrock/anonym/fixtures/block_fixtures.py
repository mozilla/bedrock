# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Block data generators for Anonym test fixtures.

Each function returns a list of block data dictionaries suitable for
assigning to Wagtail StreamField content fields.
"""


def get_figure_block_variants(image_id: int) -> list[dict]:
    """Return FigureBlock variants for testing.

    Args:
        image_id: ID of the placeholder image to use

    Returns:
        List of figure block data dictionaries
    """
    return [
        {
            "type": "figure_block",
            "value": {
                "settings": {"make_full_width": False},
                "image": image_id,
            },
            "id": "figure-variant-1",
        },
        {
            "type": "figure_block",
            "value": {
                "settings": {"make_full_width": True},
                "image": image_id,
            },
            "id": "figure-variant-2-full-width",
        },
    ]


def get_icon_card_variants() -> list[dict]:
    """Return IconCardBlock variants for testing.

    Returns:
        List of icon card block data dictionaries
    """
    return [
        {
            "type": "icon_card",
            "value": {
                "icon": "privacy",
                "heading": "Privacy First",
                "text": "<p>Your data stays <strong>yours</strong>.</p>",
            },
            "id": "icon-card-variant-1",
        },
        {
            "type": "icon_card",
            "value": {
                "icon": "security",
                "heading": "Built-in Security",
                "text": "<p>Enterprise-grade security by default.</p>",
            },
            "id": "icon-card-variant-2",
        },
        {
            "type": "icon_card",
            "value": {
                "icon": "performance",
                "heading": "High Performance",
                "text": "<p>Optimized for <em>speed</em> and efficiency.</p>",
            },
            "id": "icon-card-variant-3",
        },
    ]


def get_logo_card_variants(image_id: int) -> list[dict]:
    """Return LogoCardBlock variants for testing.

    Args:
        image_id: ID of the placeholder image to use

    Returns:
        List of logo card block data dictionaries
    """
    return [
        {
            "type": "logo_card",
            "value": {
                "logo": image_id,
                "heading": "Partner Company",
                "text": "<p>Trusted by leading brands worldwide.</p>",
                "button": [
                    {
                        "label": "Learn More",
                        "link": {
                            "link_to": "custom_url",
                            "custom_url": "https://example.com/partner",
                            "new_window": False,
                        },
                    }
                ],
            },
            "id": "logo-card-variant-1",
        },
        {
            "type": "logo_card",
            "value": {
                "logo": image_id,
                "heading": "Another Partner",
                "text": "<p>Building the future together.</p>",
                "button": [],
            },
            "id": "logo-card-variant-2-no-button",
        },
    ]


def get_person_card_variants(person_id: int) -> list[dict]:
    """Return PersonCardBlock variants for testing.

    Args:
        person_id: ID of the Person snippet to use

    Returns:
        List of person card block data dictionaries
    """
    return [
        {
            "type": "person_card",
            "value": {
                "person": person_id,
                "link": [
                    {
                        "label": "View Profile",
                        "link": {
                            "link_to": "custom_url",
                            "custom_url": "https://example.com/profile",
                            "new_window": False,
                        },
                    }
                ],
            },
            "id": "person-card-variant-1",
        },
        {
            "type": "person_card",
            "value": {
                "person": person_id,
                "link": [],
            },
            "id": "person-card-variant-2-no-link",
        },
    ]


def get_cards_list_variants(image_id: int, person_id: int = None) -> list[dict]:
    """Return CardsListBlock variants for testing.

    Args:
        image_id: ID of the placeholder image to use
        person_id: Optional ID of the Person snippet to use

    Returns:
        List of cards list block data dictionaries
    """
    icon_cards = get_icon_card_variants()[:2]
    logo_cards = get_logo_card_variants(image_id)[:1]

    variants = [
        # Variant with icon cards
        {
            "type": "cards_list",
            "value": {
                "settings": {
                    "scrollable_on_mobile": False,
                    "dividers_between_cards_on_desktop": False,
                },
                "cards": icon_cards,
            },
            "id": "cards-list-icon-cards",
        },
        # Variant with logo cards, scrollable
        {
            "type": "cards_list",
            "value": {
                "settings": {
                    "scrollable_on_mobile": True,
                    "dividers_between_cards_on_desktop": True,
                },
                "cards": logo_cards,
            },
            "id": "cards-list-logo-cards-scrollable",
        },
    ]

    # Add person card variant if person_id provided
    if person_id:
        person_cards = get_person_card_variants(person_id)[:2]
        variants.append(
            {
                "type": "cards_list",
                "value": {
                    "settings": {
                        "scrollable_on_mobile": False,
                        "dividers_between_cards_on_desktop": False,
                    },
                    "cards": person_cards,
                },
                "id": "cards-list-person-cards",
            }
        )

    return variants


def get_two_column_variants() -> list[dict]:
    """Return TwoColumnBlock variants for testing.

    Returns:
        List of two column block data dictionaries
    """
    return [
        {
            "type": "two_column",
            "value": {
                "heading_text": "Key Features",
                "subheading_text": "<p>Everything you need to know.</p>",
                "second_column": [
                    {
                        "heading_text": "Feature One",
                        "supporting_text": "<p>Description of feature one.</p>",
                    },
                    {
                        "heading_text": "Feature Two",
                        "supporting_text": "<p>Description of feature two with <strong>bold</strong> text.</p>",
                    },
                ],
            },
            "id": "two-column-variant-1",
        },
        {
            "type": "two_column",
            "value": {
                "heading_text": "How It Works",
                "subheading_text": "",
                "second_column": [
                    {
                        "heading_text": "Step 1",
                        "supporting_text": "<p>First, configure your settings.</p>",
                    },
                    {
                        "heading_text": "Step 2",
                        "supporting_text": "<p>Then, deploy your solution.</p>",
                    },
                    {
                        "heading_text": "Step 3",
                        "supporting_text": "<p>Finally, monitor and optimize.</p>",
                    },
                ],
            },
            "id": "two-column-variant-2",
        },
    ]


def get_section_block_variants(image_id: int, person_id: int = None) -> list[dict]:
    """Return SectionBlock variants for testing.

    Args:
        image_id: ID of the placeholder image to use
        person_id: Optional ID of the Person snippet to use

    Returns:
        List of section block data dictionaries
    """
    return [
        # Basic section with figure
        {
            "type": "section",
            "value": {
                "settings": {
                    "anchor_id": "overview",
                    "theme": "index",
                },
                "superheading_text": "<p>Introduction</p>",
                "heading_text": "<p>Welcome to <strong>Anonym</strong></p>",
                "subheading_text": "<p>Privacy-preserving attribution for the modern web.</p>",
                "section_content": get_figure_block_variants(image_id)[:1],
                "action": [
                    {
                        "label": "Get Started",
                        "link": {
                            "link_to": "custom_url",
                            "custom_url": "https://example.com/start",
                            "new_window": False,
                        },
                    }
                ],
            },
            "id": "section-with-figure",
        },
        # Section with cards
        {
            "type": "section",
            "value": {
                "settings": {
                    "anchor_id": "features",
                    "theme": "top_glow",
                },
                "superheading_text": "",
                "heading_text": "<p>Why Choose <strong>Anonym</strong></p>",
                "subheading_text": "<p>Built for privacy, designed for performance.</p>",
                "section_content": get_cards_list_variants(image_id, person_id)[:1],
                "action": [],
            },
            "id": "section-with-cards",
        },
        # Section with two column
        {
            "type": "section",
            "value": {
                "settings": {
                    "anchor_id": "details",
                    "theme": "",
                },
                "superheading_text": "",
                "heading_text": "<p>Key <strong>Details</strong></p>",
                "subheading_text": "",
                "section_content": get_two_column_variants()[:1],
                "action": [],
            },
            "id": "section-with-two-column",
        },
        # Section with rich text
        {
            "type": "section",
            "value": {
                "settings": {
                    "anchor_id": "about",
                    "theme": "",
                },
                "superheading_text": "",
                "heading_text": "<p>About <strong>Us</strong></p>",
                "subheading_text": "",
                "section_content": [
                    {
                        "type": "rich_text",
                        "value": (
                            "<p>Anonym is a privacy-preserving attribution platform.</p>"
                            "<p>We help advertisers measure campaign effectiveness without "
                            "compromising user privacy.</p>"
                        ),
                        "id": "rich-text-content",
                    }
                ],
                "action": [],
            },
            "id": "section-with-rich-text",
        },
    ]


def get_call_to_action_variants() -> list[dict]:
    """Return CallToActionBlock variants for testing.

    Returns:
        List of call to action block data dictionaries
    """
    return [
        {
            "type": "call_to_action",
            "value": {
                "settings": {"anchor_id": "contact-us"},
                "heading": "<p>Ready to get started? <strong>Contact us today.</strong></p>",
                "button": [
                    {
                        "label": "Contact Sales",
                        "link": {
                            "link_to": "custom_url",
                            "custom_url": "https://example.com/contact",
                            "new_window": False,
                        },
                    }
                ],
            },
            "id": "cta-variant-1",
        },
        {
            "type": "call_to_action",
            "value": {
                "settings": {"anchor_id": ""},
                "heading": "<p>Join the <strong>privacy revolution</strong></p>",
                "button": [],
            },
            "id": "cta-variant-2-no-button",
        },
    ]


def get_competitor_comparison_table_variants() -> list[dict]:
    """Return CompetitorComparisonTableBlock variants for testing.

    Returns:
        List of competitor comparison table block data dictionaries
    """
    return [
        {
            "type": "competitor_table",
            "value": {
                "heading_text": "How We Compare",
                "subheading_text": "<p>See how Anonym stacks up against traditional attribution methods.</p>",
                "rows": [
                    {
                        "text": "Privacy-preserving attribution",
                        "tradition_tracking": False,
                        "clean_rooms": True,
                        "anonym": True,
                    },
                    {
                        "text": "No user-level data exposure",
                        "tradition_tracking": False,
                        "clean_rooms": False,
                        "anonym": True,
                    },
                    {
                        "text": "Works without third-party cookies",
                        "tradition_tracking": True,
                        "clean_rooms": True,
                        "anonym": True,
                    },
                    {
                        "text": "Real-time measurement",
                        "tradition_tracking": True,
                        "clean_rooms": False,
                        "anonym": True,
                    },
                ],
            },
            "id": "comparison-table-variant-1",
        },
    ]


def get_toggleable_items_variants(image_id: int, person_id: int = None) -> list[dict]:
    """Return ToggleableItemsBlock variants for testing.

    Args:
        image_id: ID of the placeholder image to use
        person_id: Optional ID of the Person snippet to use

    Returns:
        List of toggleable items block data dictionaries
    """
    section_variants = get_section_block_variants(image_id, person_id)

    return [
        {
            "type": "toggle_items",
            "value": {
                "settings": {"anchor_id": "solutions"},
                "toggle_items": [
                    {
                        "type": "toggle_items",
                        "value": {
                            "icon": "privacy",
                            "toggle_text": "For Publishers",
                            "toggle_content": [
                                {
                                    "type": "two_column_block",
                                    "value": {
                                        "first_section": section_variants[0]["value"],
                                        "second_section": section_variants[1]["value"],
                                    },
                                    "id": "two-section-publishers",
                                }
                            ],
                        },
                        "id": "toggle-item-publishers",
                    },
                    {
                        "type": "toggle_items",
                        "value": {
                            "icon": "data-insights",
                            "toggle_text": "For Advertisers",
                            "toggle_content": [
                                {
                                    "type": "two_column_block",
                                    "value": {
                                        "first_section": section_variants[2]["value"],
                                        "second_section": section_variants[3]["value"],
                                    },
                                    "id": "two-section-advertisers",
                                }
                            ],
                        },
                        "id": "toggle-item-advertisers",
                    },
                ],
            },
            "id": "toggleable-items-variant-1",
        },
    ]


def get_stat_card_list_variants(page_ids: list[int]) -> list[dict]:
    """Return StatCardListBlock variants for testing.

    Args:
        page_ids: List of AnonymNewsItemPage or AnonymCaseStudyItemPage IDs to reference

    Returns:
        List of stat card list block data dictionaries
    """
    if not page_ids:
        return []

    return [
        {
            "type": "stat_card_list_block",
            "value": {
                "pages": page_ids[:3],
            },
            "id": "stat-card-list-variant-1",
        },
    ]


def get_case_study_list_variants(case_study_page_ids: list[int]) -> list[dict]:
    """Return CaseStudyListBlock variants for testing.

    Args:
        case_study_page_ids: List of AnonymCaseStudyItemPage IDs to reference

    Returns:
        List of case study list block data dictionaries
    """
    if not case_study_page_ids:
        return []

    return [
        {
            "type": "case_study_item_list_block",
            "value": {
                "case_study_items": case_study_page_ids[:3],
            },
            "id": "case-study-list-variant-1",
        },
    ]


def get_people_list_variants(person_ids: list[int]) -> list[dict]:
    """Return PeopleListBlock variants for testing.

    Args:
        person_ids: List of Person snippet IDs to reference

    Returns:
        List of people list block data dictionaries
    """
    if not person_ids:
        return []

    return [
        {
            "type": "people_list",
            "value": {
                "people": person_ids[:4],
            },
            "id": "people-list-variant-1",
        },
    ]


def get_stat_item_variants() -> list[dict]:
    """Return StatItemBlock variants for testing.

    Returns:
        List of stat item block data dictionaries
    """
    return [
        {
            "type": "stat",
            "value": {
                "statistic_value": "99%",
                "statistic_label": "Privacy Compliance",
            },
            "id": "stat-item-1",
        },
        {
            "type": "stat",
            "value": {
                "statistic_value": "50M+",
                "statistic_label": "Daily Events Processed",
            },
            "id": "stat-item-2",
        },
        {
            "type": "stat",
            "value": {
                "statistic_value": "24/7",
                "statistic_label": "Support Available",
            },
            "id": "stat-item-3",
        },
    ]


def get_form_field_variants() -> list[dict]:
    """Return form field block variants for testing.

    Returns:
        List of form field block data dictionaries
    """
    return [
        {
            "type": "text_field",
            "value": {
                "settings": {"internal_identifier": "full_name"},
                "label": "Full Name",
                "required": True,
            },
            "id": "text-field-name",
        },
        {
            "type": "text_field",
            "value": {
                "settings": {"internal_identifier": "company"},
                "label": "Company",
                "required": False,
            },
            "id": "text-field-company",
        },
        {
            "type": "email_field",
            "value": {
                "settings": {"internal_identifier": "email"},
                "label": "Email Address",
                "required": True,
            },
            "id": "email-field",
        },
        {
            "type": "phone_field",
            "value": {
                "settings": {"internal_identifier": "phone"},
                "label": "Phone Number",
                "required": False,
            },
            "id": "phone-field",
        },
        {
            "type": "select_field",
            "value": {
                "settings": {"internal_identifier": "interest"},
                "label": "Area of Interest",
                "required": True,
                "options": [
                    {"value": "attribution", "label": "Attribution"},
                    {"value": "measurement", "label": "Measurement"},
                    {"value": "privacy", "label": "Privacy Solutions"},
                    {"value": "other", "label": "Other"},
                ],
            },
            "id": "select-field",
        },
        {
            "type": "checkbox_group_field",
            "value": {
                "settings": {"internal_identifier": "services"},
                "label": "Services Interested In",
                "options": [
                    {"value": "consulting", "label": "Consulting"},
                    {"value": "implementation", "label": "Implementation"},
                    {"value": "support", "label": "Ongoing Support"},
                ],
            },
            "id": "checkbox-group-field",
        },
    ]


def get_navigation_link_variants() -> list[dict]:
    """Return navigation link block variants for testing.

    Returns:
        List of navigation link block data dictionaries
    """
    return [
        {
            "type": "link",
            "value": {
                "link_text": "Overview",
                "link": {
                    "link_to": "anchor",
                    "anchor": "overview",
                    "custom_url": "",
                },
            },
            "id": "nav-link-overview",
        },
        {
            "type": "link",
            "value": {
                "link_text": "Features",
                "link": {
                    "link_to": "anchor",
                    "anchor": "features",
                    "custom_url": "",
                },
            },
            "id": "nav-link-features",
        },
        {
            "type": "link",
            "value": {
                "link_text": "Contact",
                "link": {
                    "link_to": "custom_url",
                    "custom_url": "https://example.com/contact",
                    "new_window": False,
                },
            },
            "id": "nav-link-contact",
        },
    ]
