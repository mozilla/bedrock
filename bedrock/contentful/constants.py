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

# Certain content types we only want to sync for a single locale - most likely en-US.
# (This is because if localisation is NOT enabled for a field in Contentful, a request
# to their API for something other than the default en-US locale will just return the
# en-US strings - resulting in, say, English content in a ContentfulEntry where the
# locale field is `fr` :o( Therefore, it's better for us to simply not have that
# mis-localed data in the Bedrock database at all, so that we retain our
# fallback-to-en-US behaviour when a page is requested in a locale for which we have no data

SINGLE_LOCALE_CONTENT_TYPES = {
    CONTENT_TYPE_PAGE_PRODUCT_STORY: "en-US",
}

LOCALISATION_COMPLETENESS_CHECK_CONFIG = {
    # ONLY NEEDED FOR PAGES WHERE LOCALISATION IS ENABLED
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
