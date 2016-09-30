#!/bin/bash -xe

enable_proc() {
  ln -s "../supervisor_available/$1.conf" "etc/supervisor_enabled/$1.conf"
}

DB_CRON=$(echo "$DB_CRON" | tr '[:upper:]' '[:lower:]')
L10N_CRON=$(echo "$L10N_CRON" | tr '[:upper:]' '[:lower:]')

enable_proc bedrock
[[ "$L10N_CRON" == "true" ]] && enable_proc cron_l10n || true
[[ "$DB_CRON" == "true" ]] && enable_proc cron_db || true

exec supervisord -c etc/supervisord.conf
