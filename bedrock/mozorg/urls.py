# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""URL paths which must be prefixed with a language code.

These are included in the main URLConf via i18n_patterns,
which will take care of the prefixing an appropriate language code

IMPORTANT: if a redirect is needed for a non-localed URL
it must go in base.nonlocale_urls, not this file

"""

urlpatterns = []
