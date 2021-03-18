#!/bin/bash -xe

# ensure the app will start while run from supervisor
# mostly for demos
STARTUP_FILES=(
    "data/last-run-update_locales"
    "data/last-run-download_database"
)
for fname in "${STARTUP_FILES[@]}"; do
    touch "$fname"
done

exec supervisord -c etc/supervisord.conf
