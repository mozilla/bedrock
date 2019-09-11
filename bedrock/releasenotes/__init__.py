# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Adapted from django-mozilla-product-details
version_re = (r"\d+"               # major (x in x.y)
              r"\.\d+"             # minor1 (y in x.y)
              r"\.?(?:\d+)?"       # minor2 (z in x.y.z)
              r"\.?(?:\d+)?"       # minor3 (w in x.y.z.w)
              r"(?:a|b(?:eta)?)?"  # alpha/beta
              r"(?:\d*)"           # alpha/beta version
              r"(?:pre)?"          # pre release
              r"(?:\d)?"           # pre release version
              r"(?:esr)?")         # extended support release
