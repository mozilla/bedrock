# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Internal replacement for the external `querystringsafe-base64==1.1.1` package.
# That package was pinned to 1.1.1 to preserve stub attribution signature encoding
# (see https://github.com/mozilla/bedrock/issues/11156). Since it's only ~15 lines
# of stdlib wrappers, we reimplement a solution here to eliminate the external
# dependency and the Dependabot noise it created.
#
# v1.1.1 replaces '=' padding with '.' to make the output safe for query strings.
# This is the key behavioral detail — do NOT change '.' to '=' or strip padding.

from base64 import urlsafe_b64decode, urlsafe_b64encode


def encode(to_encode):
    """URL-safe base64 encode, replacing '=' padding with '.'."""
    return urlsafe_b64encode(to_encode).replace(b"=", b".")


def decode(encoded):
    """URL-safe base64 decode, restoring '.' back to '=' padding."""
    remainder = len(encoded) % 4
    if remainder:
        encoded = encoded.ljust(len(encoded) + 4 - remainder, b".")
    return urlsafe_b64decode(encoded.replace(b".", b"="))
