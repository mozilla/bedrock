msFilterList
#
# This tracking protection list only serves to enable the DNT: 1 http header
# without actually blocking anything.
#
# From Mozilla, March 2011
#
# Check for updates every month (maximum value allowed by the spec).
: Expires=30
#
# Whitelist hosting domain so when querying for updates, the request is not
# blocked.
#
+d dnt.mozilla.org
+d mozilla.org
+d mozilla.com

