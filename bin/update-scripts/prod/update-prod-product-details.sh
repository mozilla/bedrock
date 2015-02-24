#!/bin/bash

cd /data/bedrock/src/www.mozilla.org-django

venv/bin/python bedrock/manage.py update_product_details

echo -e "finished at $(date)" > /data/bedrock/src/www.mozilla.org-django/bedrock/media/product_details_finished.txt
echo -e "finished at $(date)" > /data/bedrock/www/www.mozilla.org-django/bedrock/media/product_details_finished.txt
/data/bedrock/deploy www.mozilla.org-django/bedrock/lib/product_details_json &> /dev/null
exit 0
