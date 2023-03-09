# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

MAX_MESSAGES_PER_QUEUE_POLL = 10

# Specific content types we need to target in DB lookups
CONTENT_TYPE_CONNECT_HOMEPAGE = "connectHomepage"
CONTENT_TYPE_PAGE_RESOURCE_CENTER = "pagePageResourceCenter"
CONTENT_TYPE_PAGE_GENERAL = "pageGeneral"
CONTENT_TYPE_PAGE_VERSATILE = "pageVersatile"
CONTENT_TYPE_PAGE_PRODUCT_STORY = "pageProductJournalismStory"

DEFAULT_CONTENT_TYPES = ",".join(
    [
        CONTENT_TYPE_CONNECT_HOMEPAGE,  # The Connect-based approach, currently used for the homepage
        CONTENT_TYPE_PAGE_RESOURCE_CENTER,  # New-era Compose page with a dedicated type
        CONTENT_TYPE_PAGE_PRODUCT_STORY,  # Compose page for Product Stories
    ]
)


LOCALISATION_COMPLETENESS_CHECK_CONFIG = {
    # The values in the 'data' field on the ContentfulPage we need to check to
    # decide whether the ContentfulPage record is complete for the locale it is in.
    #
    # Tip: to explore the data structure we get, if you can't readily infer it from the
    # syncing code, you can look at the JSON in the data column of the
    # contentful_contentfulentry DB table after an initial sync.
    CONTENT_TYPE_PAGE_RESOURCE_CENTER: [
        ".entries[].body",  # get the 'body' key from every dict in the 'entries' list
        ".info.seo.description",  # deep nested dictionaries
        ".info.seo.image",
    ],
    CONTENT_TYPE_PAGE_PRODUCT_STORY: [
        ".entries[].body",  # get the 'body' key from every dict in the 'entries' list
        ".info.seo.description",
        ".info.seo.name",
        ".info.image",
        ".info.title",
        # NB: if we start localising this, we may need to experiment with tuning this to make
        # sure we cover all the components that can be translated. It might also be that
        # .entries[].body is too high level to be able to check things like translated embeds
        # and instead we'll need a different approach altogether :-/
    ],
    # TO COME, once we've refactored them in Contentful
    # CONTENT_TYPE_PAGE_GENERAL: [],
    # CONTENT_TYPE_PAGE_VERSATILE: [],
}


CONTENT_CLASSIFICATION_VPN = "VPN"  # Matches string in Contentful for VPN as `product`

ARTICLE_CATEGORY_LABEL = "category"  # for URL-param filtering

ACTION_DELETE = "delete"
ACTION_ARCHIVE = "archive"
ACTION_UNARCHIVE = "unarchive"
ACTION_PUBLISH = "publish"
ACTION_UNPUBLISH = "unpublish"
ACTION_CREATE = "create"
ACTION_SAVE = "save"
ACTION_AUTO_SAVE = "auto_save"

VRC_ROOT_PATH = "/products/vpn/resource-center/"
PRODUCT_STORY_ROOT_PATH = "/stories/"
