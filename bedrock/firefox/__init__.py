# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Adapted from django-mozilla-product-details
version_re = (r"\d+"         # major (x in x.y)
              "\.\d+"        # minor1 (y in x.y)
              "\.?(?:\d+)?"  # minor2 (z in x.y.z)
              "\.?(?:\d+)?"  # minor3 (w in x.y.z.w)
              "(?:[a|b]?)"   # alpha/beta
              "(?:\d*)"      # alpha/beta version
              "(?:pre)?"     # pre release
              "(?:\d)?")     # pre release version
