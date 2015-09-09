#!/bin/bash
# Uploads maxmind_db to S3
#
# Needs S3_ACCESS_KEY, S3_SECRET_KEY, S3_BUCKET, MAXMIND_S3_PATH,
# MAXMIND_USER_ID, MAXMIND_LICENSE, MAXMIND_PRODUCTS environment
# variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#
set -ex

# Setup
TDIR=`mktemp -d`
virtualenv $TDIR
. $TDIR/bin/activate
pip install tinys3


# Get database
TMAXMIND_LOCAL_PATH=`mktemp -d`
TMAXMINDCONF=`mktemp`
cat << EOF > $TMAXMINDCONF
UserId $MAXMIND_USER_ID
LicenseKey $MAXMIND_LICENSE
ProductIds $MAXMIND_PRODUCTS
EOF

geoipupdate -f $TMAXMINDCONF -d $TMAXMIND_LOCAL_PATH


# Upload database to S3
TPY=`mktemp`
cat << EOF > $TPY
from os import walk
from os.path import join
import tinys3

conn = tinys3.Connection("$S3_ACCESS_KEY", "$S3_SECRET_KEY", tls=True,
                         default_bucket="$S3_BUCKET",
                         endpoint='s3-us-west-2.amazonaws.com')

for root, dirs, files in walk("$TMAXMIND_LOCAL_PATH"):
    for file in files:
        with open(join(root, file), 'rb') as f:
            conn.upload(join("$MAXMIND_S3_PATH", file), f)
EOF

python $TPY

# Cleanup
rm -rf $TPY $TDIR $TMAXMIND_LOCAL_PATH $TMAXMINDCONF
