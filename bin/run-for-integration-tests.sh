#!/bin/bash -xe

python manage.py migrate --noinput
python manage.py update_product_details_files
exec bin/run-prod.sh
