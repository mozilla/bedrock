# Adapted from django-mozilla-product-details
version_re = (r"\d+"         # major (x in x.y)
              "\.\d+"        # minor1 (y in x.y)
              "\.?(?:\d+)?"  # minor2 (z in x.y.z)
              "\.?(?:\d+)?"  # minor3 (w in x.y.z.w)
              "(?:[a|b]?)"   # alpha/beta
              "(?:\d*)"      # alpha/beta version
              "(?:pre)?"     # pre release
              "(?:\d)?")     # pre release version
