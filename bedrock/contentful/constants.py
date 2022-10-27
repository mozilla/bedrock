# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

MAX_MESSAGES_PER_QUEUE_POLL = 10

# Specific content types we need to target in DB lookups
CONTENT_TYPE_CONNECT_HOMEPAGE = "connectHomepage"
CONTENT_TYPE_PAGE_RESOURCE_CENTER = "pagePageResourceCenter"
CONTENT_TYPE_PAGE_GENERAL = "pageGeneral"

DEFAULT_CONTENT_TYPES = ",".join(
    [
        CONTENT_TYPE_CONNECT_HOMEPAGE,  # The Connect-based approach, currently used for the homepage
        CONTENT_TYPE_PAGE_RESOURCE_CENTER,  # New-era Compose page with a dedicated type
    ]
)

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
