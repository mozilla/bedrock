# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from django.templatetags.static import static

from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail_link_block.blocks import LinkBlock
from wagtail_thumbnail_choice_block import ThumbnailChoiceBlock

BASIC_TEXT_FEATURES = [
    "bold",
    "italic",
    "link",
    "superscript",
    "subscript",
    "strikethrough",
]


SECTION_THEME_INDEX = "index"
SECTION_THEME_TOP_GLOW = "top_glow"


ICON_CHOICES = [
    ("IRL", "IRL"),
    ("accessibility", "Accessibility"),
    ("accounts", "Accounts"),
    ("add-search-engine", "Add Search Engine"),
    ("ai", "AI"),
    ("alert", "Alert"),
    ("arrow-down", "Arrow Down"),
    ("arrow-left-white", "Arrow Left White"),
    ("arrow-left", "Arrow Left"),
    ("arrow-right-white", "Arrow Right White"),
    ("arrow-right", "Arrow Right"),
    ("arrow-up", "Arrow Up"),
    ("audio-card", "Audio Card"),
    ("audio-mute", "Audio Mute"),
    ("audio", "Audio"),
    ("auto-play-block", "Auto Play Block"),
    ("back", "Back"),
    ("bell", "Bell"),
    ("beta", "Beta"),
    ("blog", "Blog"),
    ("bookmark-menu", "Bookmark Menu"),
    ("bookmark-narrow", "Bookmark Narrow"),
    ("bookmark-remove", "Bookmark Remove"),
    ("bookmark", "Bookmark"),
    ("brightness", "Brightness"),
    ("browser", "Browser"),
    ("calendar", "Calendar"),
    ("careers", "Careers"),
    ("caret-down-white", "Caret Down White"),
    ("caret-down", "Caret Down"),
    ("caret-up", "Caret Up"),
    ("chat", "Chat"),
    ("check", "Check"),
    ("close-white", "Close White"),
    ("close", "Close"),
    ("cloud", "Cloud"),
    ("command-console", "Command Console"),
    ("command-noautohide", "Command Noautohide"),
    ("common-voice", "Common Voice"),
    ("copy", "Copy"),
    ("customize", "Customize"),
    ("cut", "Cut"),
    ("data-collection", "Data Collection"),
    ("data-insights", "Data Insights"),
    ("data-pie", "Data Pie"),
    ("default-browser", "Default Browser"),
    ("delete", "Delete"),
    ("desktop", "Desktop"),
    ("dev-edition", "Dev Edition"),
    ("developer-innovations", "Developer Innovations"),
    ("developer", "Developer"),
    ("dictionaries", "Dictionaries"),
    ("dock-bottom", "Dock Bottom"),
    ("dock-left", "Dock Left"),
    ("dock-right", "Dock Right"),
    ("dock-undock", "Dock Undock"),
    ("download-white", "Download White"),
    ("download", "Download"),
    ("earth", "Earth"),
    ("edit-write", "Edit Write"),
    ("email", "Email"),
    ("enterprise", "Enterprise"),
    ("event", "Event"),
    ("expand-white", "Expand White"),
    ("expand", "Expand"),
    ("experiments", "Experiments"),
    ("extension-available-update", "Extension Available Update"),
    ("extension-recent-updates", "Extension Recent Updates"),
    ("extensions-legacy", "Extensions Legacy"),
    ("extensions", "Extensions"),
    ("external-link-white", "External Link White"),
    ("external-link", "External Link"),
    ("eye-closed", "Eye Closed"),
    ("eye-open", "Eye Open"),
    ("facebook-container", "Facebook Container"),
    ("features", "Features"),
    ("feeback", "Feeback"),
    ("file-code", "File Code"),
    ("file-image", "File Image"),
    ("file-lock", "File Lock"),
    ("file-music", "File Music"),
    ("file-text", "File Text"),
    ("file", "File"),
    ("fire-tv", "Fire TV"),
    ("firefox-reality", "Firefox Reality"),
    ("folder-open", "Folder Open"),
    ("folder-plus", "Folder Plus"),
    ("folder-save", "Folder Save"),
    ("folder", "Folder"),
    ("font", "Font"),
    ("forget", "Forget"),
    ("form fill", "Form Fill"),
    ("forward", "Forward"),
    ("full-screen-disabled", "Full Screen Disabled"),
    ("full-screen-exit", "Full Screen Exit"),
    ("full-screen", "Full Screen"),
    ("gear", "Gear"),
    ("get-involved", "Get Involved"),
    ("globe-white", "Globe White"),
    ("globe", "Globe"),
    ("hashtag-narrow", "Hashtag Narrow"),
    ("hashtag", "Hashtag"),
    ("headphone", "Headphone"),
    ("heart-white", "Heart White"),
    ("heart", "Heart"),
    ("help", "Help"),
    ("highlight", "Highlight"),
    ("history", "History"),
    ("home", "Home"),
    ("hubs", "Hubs"),
    ("identity-notification", "Identity Notification"),
    ("identity", "Identity"),
    ("image", "Image"),
    ("import", "Import"),
    ("inbox", "Inbox"),
    ("info", "Info"),
    ("labs", "Labs"),
    ("language", "Language"),
    ("library", "Library"),
    ("link", "Link"),
    ("listen", "Listen"),
    ("lite", "Lite"),
    ("location-disabled", "Location Disabled"),
    ("location-macos-disabled", "Location Macos Disabled"),
    ("location-macos", "Location Macos"),
    ("location-pin", "Location Pin"),
    ("location-windows-disabled", "Location Windows Disabled"),
    ("location-windows", "Location Windows"),
    ("location", "Location"),
    ("lock", "Lock"),
    ("lockbox", "Lockbox"),
    ("login", "Login"),
    ("mail", "Mail"),
    ("maximize", "Maximize"),
    ("megaphone", "Megaphone"),
    ("menu-white", "Menu White"),
    ("menu", "Menu"),
    ("microphone-disabled", "Microphone Disabled"),
    ("microphone", "Microphone"),
    ("midi", "Midi"),
    ("minimize", "Minimize"),
    ("minus", "Minus"),
    ("mobile-narrow", "Mobile Narrow"),
    ("mobile", "Mobile"),
    ("monitor", "Monitor"),
    ("more-horizontal", "More Horizontal"),
    ("more-vertical", "More Vertical"),
    ("mountain", "Mountain"),
    ("mouse-pointer-disabled", "Mouse Pointer Disabled"),
    ("mouse-pointer", "Mouse Pointer"),
    ("mozilla", "Mozilla"),
    ("new", "New"),
    ("nightly", "Nightly"),
    ("notes", "Notes"),
    ("notifications-disabled", "Notifications Disabled"),
    ("notifications", "Notifications"),
    ("open-in-new", "Open In New"),
    ("open", "Open"),
    ("opensource", "Opensource"),
    ("overflow", "Overflow"),
    ("paperclip-narrow", "Paperclip Narrow"),
    ("paperclip", "Paperclip"),
    ("paste", "Paste"),
    ("pause-white", "Pause White"),
    ("pause", "Pause"),
    ("performance", "Performance"),
    ("photon", "Photon"),
    ("pin-remove", "Pin Remove"),
    ("pin", "Pin"),
    ("play-white", "Play White"),
    ("play", "Play"),
    ("plugin-disabled", "Plugin Disabled"),
    ("plugin", "Plugin"),
    ("plus", "Plus"),
    ("pocket-list", "Pocket List"),
    ("pocket-remove", "Pocket Remove"),
    ("pocket", "Pocket"),
    ("popular", "Popular"),
    ("popup-block", "Popup Block"),
    ("preferences", "Preferences"),
    ("pricetag", "Pricetag"),
    ("pricetag-white", "Pricetag White"),
    ("printer", "Printer"),
    ("privacy", "Privacy"),
    ("private-browsing", "Private Browsing"),
    ("protocol", "Protocol"),
    ("proton", "Proton"),
    ("query", "Query"),
    ("quit", "Quit"),
    ("quote", "Quote"),
    ("read", "Read"),
    ("reader-mode", "Reader Mode"),
    ("redo", "Redo"),
    ("refresh", "Refresh"),
    ("release-notes", "Release Notes"),
    ("reminders", "Reminders"),
    ("report-narrow", "Report Narrow"),
    ("report", "Report"),
    ("resources", "Resources"),
    ("restore-session", "Restore Session"),
    ("rhombus-layers", "Rhombus Layers"),
    ("rhombus-layers-white", "Rhombus Layers White"),
    ("screen-share-disabled", "Screen Share Disabled"),
    ("screen-share", "Screen Share"),
    ("screenshot", "Screenshot"),
    ("search-white", "Search White"),
    ("search", "Search"),
    ("secure-broken", "Secure Broken"),
    ("secure-mixed", "Secure Mixed"),
    ("secure", "Secure"),
    ("security", "Security"),
    ("send-to-device", "Send To Device"),
    ("send", "Send"),
    ("settings", "Settings"),
    ("share-windows", "Share Windows"),
    ("share", "Share"),
    ("shield", "Shield"),
    ("sidebar", "Sidebar"),
    ("sign-in", "Sign In"),
    ("sign-up", "Sign Up"),
    ("sound-off", "Sound Off"),
    ("sound-on", "Sound On"),
    ("star", "Star"),
    ("stop", "Stop"),
    ("store-data-disabled", "Store Data Disabled"),
    ("store-data", "Store Data"),
    ("sub-item", "Sub Item"),
    ("subscribe", "Subscribe"),
    ("sync", "Sync"),
    ("tab-mobile", "Tab Mobile"),
    ("tab-new", "Tab New"),
    ("tab", "Tab"),
    ("tablet", "Tablet"),
    ("thumbs-up-narrow", "Thumbs Up Narrow"),
    ("thumbs-up", "Thumbs Up"),
    ("toggle-off", "Toggle Off"),
    ("toggle-on", "Toggle On"),
    ("toolbar", "Toolbar"),
    ("top-sites", "Top Sites"),
    ("tracing-protection-disabled", "Tracing Protection Disabled"),
    ("tracking-protection", "Tracking Protection"),
    ("trash-narrow", "Trash Narrow"),
    ("trash", "Trash"),
    ("turbo-mode", "Turbo Mode"),
    ("undo", "Undo"),
    ("update", "Update"),
    ("user", "User"),
    ("video-card", "Video Card"),
    ("video-recoder-disabled", "Video Recoder Disabled"),
    ("video-recorder", "Video Recorder"),
    ("warning", "Warning"),
    ("watch", "Watch"),
    ("web-of-things", "Web Of Things"),
    ("web-vr", "Web Vr"),
    ("window-new", "Window New"),
    ("window", "Window"),
    ("zoom-in", "Zoom In"),
    ("zoom-out", "Zoom Out"),
]


# The location of non-mozilla-protocal icons.
NON_PROTOCOL_ICONS_DIRS = {
    "pricetag": "img/icons",
    "pricetag-white": "img/icons",
    "rhombus-layers": "img/icons",
    "rhombus-layers-white": "img/icons",
}


def get_icon_choices():
    """
    Get the icon choices for a ThumbnailChoiceBlock.
    """
    return [(icon_choice[0], icon_choice[1]) for icon_choice in ICON_CHOICES]


def get_icon_thumbnails():
    """
    Get the icon thumbnails for a ThumbnailChoiceBlock.

    This function is called during ThumbnailChoiceBlock initialization at module import time.
    We use try/except because static() requires the staticfiles manifest, which doesn't
    exist during migrations. The expected behavior is:
      - During runtime: URLs via static()
      - During migrations: Direct paths that work without the manifest
    """
    result = {}
    for icon_choice in ICON_CHOICES:
        icon_key = icon_choice[0]

        # Determine the icon base_url.
        base_url = "protocol/img/icons"
        if icon_key in NON_PROTOCOL_ICONS_DIRS:
            base_url = NON_PROTOCOL_ICONS_DIRS[icon_key]

        icon_key = icon_key.lower()
        try:
            result[icon_key] = static(f"{base_url}/{icon_key}.svg")
        except (ValueError, OSError):
            # Fallback when staticfiles manifest doesn't exist (during migrations/collectstatic)
            result[icon_key] = f"/static/{base_url}/{icon_key}.svg"
    return result


class FigureBlockSettings(blocks.StructBlock):
    make_full_width = blocks.BooleanBlock(
        required=False,
        default=False,
        label="Make Full Width",
        inline_form=True,
        help_text="The Default width is constrained to the layout grid with a max-width, centered on the page.",
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "Full width: {make_full_width}"
        form_classname = "compact-form struct-block"


class FigureBlock(blocks.StructBlock):
    settings = FigureBlockSettings()
    image = ImageChooserBlock()

    class Meta:
        template = "mozorg/cms/anonym/blocks/figure.html"
        label = "Figure"


class LinkWithTextBlock(blocks.StructBlock):
    label = blocks.CharBlock(label="Link Text")
    link = LinkBlock()

    class Meta:
        label = "Link"
        label_format = "Link - {label}"


class StatBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    heading = blocks.CharBlock(label="Heading")
    statistic1_value = blocks.RichTextBlock(features=BASIC_TEXT_FEATURES)
    statistic1_label = blocks.RichTextBlock(features=BASIC_TEXT_FEATURES)
    statistic2_value = blocks.RichTextBlock(features=BASIC_TEXT_FEATURES)
    statistic2_label = blocks.RichTextBlock(features=BASIC_TEXT_FEATURES)

    class Meta:
        template = "mozorg/cms/anonym/blocks/stat-item.html"
        label = "Statistic"
        label_format = "Statistic - {heading}"


class StatsListBlock(blocks.StructBlock):
    stats = blocks.StreamBlock(
        [
            ("stat", StatBlock()),
        ]
    )

    class Meta:
        template = "mozorg/cms/anonym/blocks/stats-list.html"
        label = "Stats List"


class PeopleListBlock(blocks.StructBlock):
    people_photos = blocks.ListBlock(ImageChooserBlock(), min_num=1, max_num=8, default=[])
    text = blocks.RichTextBlock(features=BASIC_TEXT_FEATURES)

    class Meta:
        template = "mozorg/cms/anonym/blocks/people-list.html"
        label = "People List"


class CardListSettings(blocks.StructBlock):
    scrollable_on_mobile = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text="The default behavior is stacked",
    )
    dividers_between_cards_on_desktop = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text="Add divider lines between cards on desktop",
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "Scroll on mobile: {scrollable_on_mobile} - Dividers on desktop: {dividers_between_cards_on_desktop}"
        form_classname = "compact-form struct-block"


class IconCardBlock(blocks.StructBlock):
    icon = ThumbnailChoiceBlock(
        required=False,
        choices=get_icon_choices,
        thumbnails=get_icon_thumbnails,
        default="outlined",
        inline_form=True,
    )
    heading = blocks.CharBlock(label="Heading")
    text = blocks.RichTextBlock(features=BASIC_TEXT_FEATURES)

    class Meta:
        template = "mozorg/cms/anonym/blocks/icon-card.html"
        label = "Icon Card"
        label_format = "Icon Card - {heading}"


class LogoCardBlock(blocks.StructBlock):
    logo = ImageChooserBlock()
    heading = blocks.CharBlock(label="Heading")
    text = blocks.RichTextBlock(features=BASIC_TEXT_FEATURES)
    button = blocks.ListBlock(LinkWithTextBlock(), min_num=0, max_num=1, default=[])

    class Meta:
        template = "mozorg/cms/anonym/blocks/logo-card.html"
        label = "Logo Card"
        label_format = "Logo Card - {heading}"


class PersonCardBlock(blocks.StructBlock):
    person = SnippetChooserBlock("mozorg.Person")
    link = blocks.ListBlock(LinkWithTextBlock(), min_num=0, max_num=1, default=[])

    class Meta:
        template = "mozorg/cms/anonym/blocks/person-card.html"
        label = "Person Card"
        label_format = "Person Card - {person}"


class CardsListBlock(blocks.StructBlock):
    settings = CardListSettings()
    cards = blocks.StreamBlock(
        [
            ("icon_card", IconCardBlock()),
            ("logo_card", LogoCardBlock()),
            ("person_card", PersonCardBlock()),
        ],
        min_num=1,
        max_num=4,
    )

    class Meta:
        template = "mozorg/cms/anonym/blocks/cards-list.html"
        label = "Cards List"
        label_format = "Cards List - {heading}"


class SectionBlockSettingsValue(blocks.StructValue):
    """Custom value class to make properties available in templates."""

    @property
    def has_index_theme(self) -> bool:
        return self.get("theme") == SECTION_THEME_INDEX

    @property
    def has_top_glow_theme(self) -> bool:
        return self.get("theme") == SECTION_THEME_TOP_GLOW


class SectionBlockSettings(blocks.StructBlock):
    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable from navigation (e.g., 'overview', 'features')",
    )
    theme = ThumbnailChoiceBlock(
        choices=(
            (SECTION_THEME_INDEX, "Index"),
            (SECTION_THEME_TOP_GLOW, "Top Glow"),
        ),
        thumbnails={
            SECTION_THEME_INDEX: "/media/img/icons/index.svg",
            SECTION_THEME_TOP_GLOW: "/media/img/icons/top_glow.svg",
        },
        inline_form=True,
        required=False,
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "ID: {anchor_id} - Theme: {theme}"
        form_classname = "compact-form struct-block"
        value_class = SectionBlockSettingsValue


class ListItemBlock(blocks.StructBlock):
    heading_text = blocks.CharBlock(label="Heading")
    supporting_text = blocks.RichTextBlock(features=BASIC_TEXT_FEATURES)

    class Meta:
        label = "List Item"
        label_format = "{heading_text}"
        template = "mozorg/cms/anonym/blocks/list-item.html"
        form_classname = "compact-form struct-block"


class TwoColumnBlock(blocks.StructBlock):
    heading_text = blocks.CharBlock(label="Heading")
    subheading_text = blocks.RichTextBlock(features=BASIC_TEXT_FEATURES)
    second_column = blocks.ListBlock(ListItemBlock(), min_num=0)

    class Meta:
        label = "Two Column Block"
        label_format = "Two Column - {heading_text}"
        template = "mozorg/cms/anonym/blocks/two-column.html"
        form_classname = "compact-form struct-block"


class SectionBlock(blocks.StructBlock):
    is_section_block = True

    settings = SectionBlockSettings()
    superheading_text = blocks.RichTextBlock(features=BASIC_TEXT_FEATURES, required=False)
    heading_text = blocks.RichTextBlock(
        features=BASIC_TEXT_FEATURES,
        help_text="Use Bold to make parts of this text black.",
    )
    subheading_text = blocks.RichTextBlock(features=BASIC_TEXT_FEATURES, required=False)

    section_content = blocks.StreamBlock(
        [
            ("figure_block", FigureBlock()),
            ("cards_list", CardsListBlock()),
            ("stats_list_block", StatsListBlock()),
            ("people_list", PeopleListBlock()),
            ("table", TableBlock()),
            ("two_column", TwoColumnBlock()),
        ],
        required=False,
    )
    action = blocks.ListBlock(LinkWithTextBlock(), min_num=0, max_num=1, default=[])

    class Meta:
        template = "mozorg/cms/anonym/blocks/section.html"
        label = "Section"
        label_format = "{heading_text}"


class TwoSectionBlock(blocks.StructBlock):
    first_section = SectionBlock()
    second_section = SectionBlock()

    class Meta:
        template = "mozorg/cms/anonym/blocks/two-sections.html"
        label = "Two Sections"


class ToggleableItemBlock(blocks.StructBlock):
    icon = ThumbnailChoiceBlock(
        required=True,
        choices=get_icon_choices,
        thumbnails=get_icon_thumbnails,
        default="outlined",
        inline_form=True,
    )
    toggle_text = blocks.CharBlock()
    toggle_content = blocks.StreamBlock(
        [
            ("two_column_block", TwoSectionBlock()),
        ],
        required=True,
    )

    class Meta:
        label = "Toggle Item"
        label_format = "Toggle Item - {toggle_text}"


class ToggleableItemsBlockSettings(blocks.StructBlock):
    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable from navigation",
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "ID: {anchor_id}"
        form_classname = "compact-form struct-block"


class ToggleableItemsBlock(blocks.StructBlock):
    settings = ToggleableItemsBlockSettings()
    toggle_items = blocks.StreamBlock(
        [
            ("toggle_items", ToggleableItemBlock()),
        ],
        required=True,
    )

    class Meta:
        template = "mozorg/cms/anonym/blocks/toggleable-items.html"
        label = "Toggle Items"


class CallToActionBlockSettings(blocks.StructBlock):
    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable from navigation",
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "ID: {anchor_id}"
        form_classname = "compact-form struct-block"


class CallToActionBlock(blocks.StructBlock):
    settings = CallToActionBlockSettings()
    heading = blocks.RichTextBlock(
        features=BASIC_TEXT_FEATURES,
        help_text="Use <strong>bold</strong> to make parts of this text black.",
    )
    button = blocks.ListBlock(LinkWithTextBlock(), min_num=0, max_num=1, default=[])

    class Meta:
        template = "mozorg/cms/anonym/blocks/call-to-action.html"
        label = "Call To Action"
        label_format = "{heading}"
