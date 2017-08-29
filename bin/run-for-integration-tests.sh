#!/bin/bash -xe

python manage.py migrate --noinput --database bedrock
python manage.py update_product_details_files --database bedrock
exec bin/run-prod.sh
