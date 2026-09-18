# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from wagtail import hooks


@hooks.register("register_icons")
def register_showcase_media_icons(icons):
    for icon in [
        "showcase-ultrawide.svg",
        "showcase-square.svg",
        "showcase-pair.svg",
        "showcase-row.svg",
    ]:
        icons.append(f"mozorg/icons/{icon}")
    return icons
