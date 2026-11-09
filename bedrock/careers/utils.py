# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def generate_position_meta_description(position):
    suffix = "n" if position.position_type.lower().startswith(("a", "e", "i", "o", "u")) else ""
    meta = f"Mozilla is hiring a{suffix} {position.position_type.lower()} {position.title}"

    locations = position.location_list

    if len(locations) > 1:
        meta = meta + f" in {', '.join(locations[:-1])} and {locations[-1]}"
    elif locations:
        meta = meta + f" in {locations[0]}"

    return meta
