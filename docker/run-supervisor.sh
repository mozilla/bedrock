#!/bin/bash

set -xe

enable_proc() {
  cp "etc/supervisor_available/$1.conf" "etc/supervisor_enabled/$1.conf"
}

DEV=$(echo "$DEV" | tr '[:upper:]' '[:lower:]')
DB_CRON=$(echo "$DB_CRON" | tr '[:upper:]' '[:lower:]')

enable_proc bedrock
[[ "$DEV" == "true" ]] && enable_proc cron_l10n || true
[[ "$DB_CRON" == "true" ]] && enable_proc cron_db || true

exec supervisord -c etc/supervisord.conf
