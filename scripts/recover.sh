#!/usr/bin/env bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#
# Database recovery for Bedrock.
#
#   recover.sh prepare --env=prod --gcp-project=P --bucket=B --database=D \
#                      --backup=latest
#   recover.sh prepare --env=prod --gcp-project=P --bucket=B --database=D \
#                      --pitr=2026-09-03T14:19:00Z
#   recover.sh restore --env=prod --gcp-project=P --bucket=B --database=D \
#                      --dump=gs://B/recovery/bedrock-prod-202609041530.sql.gz \
#                      --confirm-destructive-action
#   recover.sh cleanup --env=prod --gcp-project=P [--dump=gs://...] [--scratch=I]
#
#   recover.sh resume-replication --env=prod --gcp-project=P
#   recover.sh allow-connections  --env=prod --gcp-project=P --bucket=B --database=D
#
# prepare  builds a throwaway instance from a backup or a point in time and exports a SQL
#          dump. Changes nothing on the live instance. Safe to run on suspicion.
# restore  drops and reimports the live database from that dump. Not reversible.
# cleanup  deletes throwaway instances and the dump. Keeps the backups. Sweeps every
#          <instance>-recover-* by default; pass --scratch to delete just one, which is
#          what you want if another recovery may be in flight.
#
# Postgres instance names are derived from --env. The GCP project ID, bucket name, and
# database name are not in this file: pass --gcp-project, --bucket, and --database.
# Nothing here can reach production by itself.
#
# --backup takes a backup ID or "latest". --pitr takes a full timestamp with an explicit
# zone, e.g. 2026-09-03T14:19:00Z or 2026-09-03T15:19:00+01:00.
#
# restore does not need the CMS stopped — that would mean a values.yaml change and a CI
# round trip. It sets CONNECTION LIMIT 0 on the app role for the drop, and lifts it again
# for the import.
#
# Dumps go to a db_sync bucket (passed via --bucket) under a recovery/ prefix. That bucket
# only exists in the production Bedrock project, so a dev or stage recovery reaches across
# projects and needs bucket IAM rights there.

set -euo pipefail

# ══════════════════════════════════════════════════════════════════ configuration

config() {
  case "$ENV" in
    dev | stage) TIER=nonprod ;;
    prod) TIER=prod ;;
    *) die "unknown env: $ENV (expected dev, stage or prod)" ;;
  esac

  INSTANCE="bedrock-${TIER}-${ENV}-v1"
  DB_USER="bedrock_rw_user"

  # US always; EU as well in stage and prod, on a separate cluster.
  REPLICAS=("${INSTANCE}-replica-0")
  [[ "$ENV" == dev ]] || REPLICAS+=("bedrock-${TIER}-${ENV}-eu-replica-0")
}

# ══════════════════════════════════════════════════════════════════ helpers

log() { printf '\n[%s] %s\n' "$(date -u +%H:%M:%SZ)" "$*" >&2; }
warn() { printf '[%s] WARN  %s\n' "$(date -u +%H:%M:%SZ)" "$*" >&2; }
die() {
  printf '[%s] ERROR %s\n' "$(date -u +%H:%M:%SZ)" "$*" >&2
  exit 1
}

# Every gcloud sql call goes through here so --project can never be forgotten, which would
# otherwise silently target whatever the local default happens to be.
sql() { gcloud sql "$@" --project="$PROJECT"; }

require_gcloud() {
  command -v gcloud >/dev/null || die "gcloud not on PATH"
  OPERATOR="$(gcloud auth list --filter=status:ACTIVE --format='value(account)' 2>/dev/null | head -1)"
  [[ -n "$OPERATOR" ]] || die "no active credentials. Run: gcloud auth login"
}

wait_runnable() {
  local instance="$1" waited=0 state
  log "waiting for $instance to become RUNNABLE"
  while :; do
    state="$(gcloud sql instances describe "$instance" \
      --project="$PROJECT" --format='value(state)' 2>/dev/null || echo PENDING)"
    [[ "$state" == RUNNABLE ]] && {
      log "$instance RUNNABLE after ${waited}s"
      return 0
    }
    [[ "$state" == FAILED || "$state" == SUSPENDED ]] && die "$instance is $state"
    ((waited >= 1800)) && die "$instance still $state after 30m. Check: gcloud sql operations list --instance=$instance --project=$PROJECT"
    sleep 15
    waited=$((waited + 15))
  done
}

# Each Cloud SQL instance has its own service account, and a new one has no bucket access.
# Miss this and the export or import fails with a permissions error that looks like your
# own IAM. Note the bucket is always in the app's *prod* project, so for a dev or stage
# recovery this binds IAM across projects and needs rights there.
grant_bucket_access() {
  local instance="$1" role="$2" sa
  sa="$(sql instances describe "$instance" --format='value(serviceAccountEmailAddress)')"
  [[ -n "$sa" ]] || die "could not read service account for $instance"
  gcloud storage buckets add-iam-policy-binding "gs://$BUCKET" \
    --member="serviceAccount:${sa}" --role="$role" >/dev/null ||
    die "could not grant $sa $role on gs://$BUCKET"
  log "granted $sa $role on gs://$BUCKET"
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    local arg="${1%%=*}" val=""
    [[ "$1" == *=* ]] && val="${1#*=}"
    case "$arg" in
      --env)        ENV="${val:-${2:?}}" ;;
      --gcp-project) PROJECT="${val:-${2:?}}" ;;
      --bucket)     BUCKET="${val:-${2:?}}" ;;
      --database)   DATABASE="${val:-${2:?}}" ;;
      --backup)     BACKUP="${val:-${2:?}}" ;;
      --pitr)       PITR="${val:-${2:?}}" ;;
      --dump)       DUMP="${val:-${2:?}}" ;;
      --scratch)    SCRATCH="${val:-${2:?}}" ;;
      --confirm-destructive-action) CONFIRMED=true && val=x ;;
      *) die "unknown argument: $1" ;;
    esac
    [[ -n "$val" ]] && shift || shift 2
  done
}

require_arg() {
  local name="$1" value="$2" hint="${3:-}"
  [[ -n "$value" ]] || die "$name is required${hint:+ ($hint)}"
}

# ══════════════════════════════════════════════════════════════════ safety

set_replication() {
  local mode="$1" replica flag
  [[ "$mode" == on ]] && flag=--enable-database-replication || flag=--no-enable-database-replication
  for replica in "${REPLICAS[@]}"; do
    if sql instances patch "$replica" "$flag" --quiet >/dev/null 2>&1; then
      log "replication $mode: $replica"
    else
      warn "could not turn replication $mode for $replica — check it by hand"
    fi
  done
}

# Runs SQL by importing it as a file, which is the only way in without a database password.
run_sql() {
  local sql_text="$1" label="$2" uri="gs://${BUCKET}/recovery/sql-$(date +%s%N).sql" tmp rc=0
  tmp="$(mktemp)"
  printf '%s\n' "$sql_text" >"$tmp"
  gcloud storage cp "$tmp" "$uri" >/dev/null || die "could not stage SQL for $label"
  rm -f "$tmp"
  # As the superuser against the system database, so it can act on $DATABASE.
  sql import sql "$INSTANCE" "$uri" --database=postgres --user=postgres --quiet >/dev/null || rc=$?
  # Always delete the staged file — it contains role and database names.
  gcloud storage rm "$uri" >/dev/null 2>&1 || true
  [[ "$rc" -eq 0 ]] || die "$label failed"
  log "$label done"
}

# Refuses new connections from the app role so the drop cannot lose a race against
# reconnecting pods. Needs no deployment and no cluster access. The revokes alone would not
# do it: a role that owns the database, or holds CONNECT directly rather than via PUBLIC, is
# unaffected by them. This script is unaffected because run_sql connects as postgres to the
# postgres database, not as the app role to the app database.
block_connections() {
  CONNECTIONS_BLOCKED=true
  run_sql "ALTER ROLE \"$DB_USER\" CONNECTION LIMIT 0;
REVOKE CONNECT ON DATABASE \"$DATABASE\" FROM PUBLIC;
REVOKE CONNECT ON DATABASE \"$DATABASE\" FROM \"$DB_USER\";
SELECT pg_terminate_backend(pid) FROM pg_stat_activity
  WHERE datname = '$DATABASE' AND pid <> pg_backend_pid();" "blocking connections from $DB_USER"
}

allow_connections() {
  run_sql "ALTER ROLE \"$DB_USER\" CONNECTION LIMIT -1;" "restoring connections for $DB_USER"
  CONNECTIONS_BLOCKED=false
}

# Registered the moment anything is paused or blocked. If the script dies, is cancelled, or
# the runner is torn down, both come back. A paused replica accumulates WAL on the primary
# and serves stale reads; a role left at CONNECTION LIMIT 0 keeps the CMS locked out even
# once the database is fine.
resume_trap() {
  local code=$?
  # Guard against re-entry: if allow_connections → run_sql → die fires inside this trap,
  # die calls exit, which would re-enter the trap and recurse until stack overflow.
  trap - EXIT INT TERM
  warn "exiting unexpectedly — restoring access and replication before anything else"

  # Replication first: set_replication only warns, it never dies, so it cannot strand the
  # rest of the trap. A paused replica serves stale content to the public site, which is
  # worse than the CMS being locked out.
  set_replication on

  # In a subshell, because allow_connections → run_sql → die calls exit. Outside a subshell
  # that exit would end the trap here, and anything after it would never run.
  if [[ "${CONNECTIONS_BLOCKED:-false}" == true ]]; then
    (allow_connections) || warn "could not restore connections — run: $0 allow-connections --env=$ENV --gcp-project=$PROJECT --bucket=$BUCKET --database=$DATABASE"
  fi

  cat >&2 <<EOF

Access and replication restored, but the database may be mid-restore. Check:

  gcloud sql databases list --instance=$INSTANCE --project=$PROJECT
  gcloud sql operations list --instance=$INSTANCE --project=$PROJECT --limit=5

If $DATABASE is missing or partial, re-run restore. The pre-import backup is your way back.
EOF
  exit "$code"
}

# ══════════════════════════════════════════════════════════════════ prepare

cmd_prepare() {
  BACKUP="" PITR=""
  parse_args "$@"

  require_arg "--env" "${ENV:-}" "dev, stage or prod"
  require_arg "--gcp-project" "${PROJECT:-}" "this file holds no project IDs"
  require_arg "--bucket" "${BUCKET:-}" "the db_sync bucket name"
  require_arg "--database" "${DATABASE:-}" "the database name"
  [[ -n "${BACKUP:-}" || -n "${PITR:-}" ]] || die "one of --backup or --pitr is required"
  [[ -z "${BACKUP:-}" || -z "${PITR:-}" ]] || die "--backup and --pitr are mutually exclusive"

  # Strict on purpose. A timestamp with no zone, or local time passed as UTC, silently
  # recovers to the wrong moment.
  if [[ -n "${PITR:-}" ]] &&
    [[ ! "$PITR" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})$ ]]; then
    cat >&2 <<'FMT'
--pitr must be a full timestamp with an explicit zone. Accepted:

  2026-09-03T14:19:00Z            UTC, whole seconds
  2026-09-03T14:19:00.094Z        UTC, with fraction
  2026-09-03T15:19:00+01:00       with offset (BST)

Rejected: 2026-09-03T14:19 (no zone), 2026-09-03 14:19:00Z (space), 14:19 (no date).

Working in BST or CEST? Convert to UTC or use the offset form. Never pass local time
with a Z.
FMT
    exit 1
  fi

  config
  require_gcloud

  local state
  state="$(sql instances describe "$INSTANCE" --format='value(state)' 2>/dev/null)" ||
    die "cannot read $INSTANCE in $PROJECT — wrong name, wrong project, or missing roles/cloudsql.admin"
  [[ "$state" == RUNNABLE ]] || die "$INSTANCE is $state, expected RUNNABLE"

  gcloud storage buckets describe "gs://$BUCKET" >/dev/null 2>&1 ||
    die "cannot access gs://$BUCKET — check the bucket exists and you have storage access"

  local run_id scratch dump_uri source_desc
  run_id="$(date -u +%Y%m%d%H%M)"
  # Cloud SQL blocks reuse of an instance name for days after deletion, so the timestamp is
  # load-bearing.
  scratch="${INSTANCE}-recover-${run_id}"
  dump_uri="gs://${BUCKET}/recovery/bedrock-${ENV}-${run_id}.sql.gz"

  log "operator=$OPERATOR project=$PROJECT instance=$INSTANCE"

  # ---- resolve what we are recovering to
  if [[ -n "${PITR:-}" ]]; then
    log "PITR window: $(sql instances get-latest-recovery-time "$INSTANCE" 2>/dev/null | tr -d '\n' || echo unknown)"
    source_desc="pitr:$PITR"
  else
    if [[ "$BACKUP" == latest ]]; then
      BACKUP="$(sql backups list --instance="$INSTANCE" --filter='status=SUCCESSFUL' \
        --sort-by='~windowStartTime' --limit=1 --format='value(id)')"
      [[ -n "$BACKUP" ]] || die "no successful backups on $INSTANCE"
    fi
    local taken
    taken="$(sql backups describe "$BACKUP" --instance="$INSTANCE" \
      --format='value(windowStartTime)' 2>/dev/null)" ||
      die "backup $BACKUP not found on $INSTANCE"
    log "using backup $BACKUP taken $taken"
    source_desc="backup:${BACKUP}@${taken}"
  fi

  # ---- snapshot the current state, for forensics, before anything else
  log "backing up $INSTANCE as it currently stands"
  sql backups create --instance="$INSTANCE" \
    --description="recover.sh discovery $OPERATOR" >/dev/null
  local discovery_backup
  discovery_backup="$(sql backups list --instance="$INSTANCE" \
    --sort-by='~windowStartTime' --limit=1 --format='value(id)')"
  log "discovery backup: $discovery_backup"

  # ---- build the throwaway instance
  if [[ -n "${PITR:-}" ]]; then
    log "cloning $INSTANCE to $scratch at $PITR"
    sql instances clone "$INSTANCE" "$scratch" --point-in-time="$PITR" >/dev/null ||
      die "clone failed — if the timestamp was rejected, the error above names the actual limit"
    wait_runnable "$scratch"
    # Clones inherit deletion protection from the source. Turn it off — this instance is
    # disposable and cleanup needs to delete it.
    sql instances patch "$scratch" --no-deletion-protection --quiet >/dev/null ||
      warn "could not disable deletion protection on $scratch — cleanup will need it done by hand"
  else
    # `backups restore` overwrites an existing instance and cannot create one, so the target
    # is built first. It must match the source's major version or the restore is refused. HA
    # and backups off: this instance lives for minutes.
    local version tier region network
    read -r version tier region network <<<"$(sql instances describe "$INSTANCE" \
      --format='value[separator=" "](databaseVersion,settings.tier,region,settings.ipConfiguration.privateNetwork)')"
    [[ -n "$network" ]] || die "could not read the private network of $INSTANCE"

    log "creating $scratch to match $version $tier $region"
    sql instances create "$scratch" --database-version="$version" --tier="$tier" \
      --region="$region" --network="$network" --no-assign-ip \
      --availability-type=ZONAL --no-backup --no-deletion-protection \
      >/dev/null || die "could not create $scratch"
    wait_runnable "$scratch"

    log "restoring backup $BACKUP into $scratch"
    sql backups restore "$BACKUP" --restore-instance="$scratch" \
      --backup-instance="$INSTANCE" --quiet >/dev/null || die "restore into $scratch failed"
    wait_runnable "$scratch"
  fi

  # ---- export
  grant_bucket_access "$scratch" roles/storage.objectAdmin

  log "exporting $DATABASE to $dump_uri"
  # No --offload: that spares a live instance the load, and this one has no traffic.
  sql export sql "$scratch" "$dump_uri" --database="$DATABASE" ||
    die "export failed. $scratch still exists for inspection"

  cat >&2 <<EOF

──────────────────────────────────────────────────────────────────────
Prepare complete. Nothing on $INSTANCE has changed.

  recovering to    $source_desc
  throwaway        $scratch
  dump             $dump_uri
  discovery backup $discovery_backup

Verify the dump is what you want before going further. Open Cloud SQL Studio in the
GCP console for $scratch and check that the damage is absent and the content you need
is present. If not, run prepare again against an earlier backup — the throwaway instance
is disposable.

Then:

  $0 restore --env=$ENV --gcp-project=$PROJECT --bucket=$BUCKET \\
             --database=$DATABASE --dump=$dump_uri \\
             --confirm-destructive-action

That drops and recreates $DATABASE on $INSTANCE, and is not reversible.

When done:

  $0 cleanup --env=$ENV --gcp-project=$PROJECT --dump=$dump_uri --scratch=$scratch
──────────────────────────────────────────────────────────────────────
EOF

}

# ══════════════════════════════════════════════════════════════════ restore

cmd_restore() {
  CONFIRMED=false
  parse_args "$@"

  require_arg "--env" "${ENV:-}" "dev, stage or prod"
  require_arg "--gcp-project" "${PROJECT:-}" "this file holds no project IDs"
  require_arg "--bucket" "${BUCKET:-}" "the db_sync bucket name"
  require_arg "--database" "${DATABASE:-}" "the database name"
  require_arg "--dump" "${DUMP:-}" "the dump URI from prepare"
  [[ "$DUMP" =~ ^gs://[a-zA-Z0-9._-]+/.+ ]] || die "dump URI must be a gs:// path (got: $DUMP)"

  config

  # The flag is an acknowledgement rather than a check. Kept long and awkward so it cannot
  # be reached by reflex or shell history without noticing.
  if [[ "${CONFIRMED:-false}" != true ]]; then
    cat >&2 <<EOF
This drops and recreates the '$DATABASE' database on $INSTANCE ($PROJECT) and reimports it
from $DUMP. It is not reversible.

Re-run with --confirm-destructive-action to proceed.
EOF
    exit 1
  fi

  require_gcloud

  local state
  state="$(sql instances describe "$INSTANCE" --format='value(state)' 2>/dev/null)" ||
    die "cannot read $INSTANCE in $PROJECT"
  [[ "$state" == RUNNABLE ]] || die "$INSTANCE is $state, expected RUNNABLE"

  gcloud storage ls "$DUMP" >/dev/null 2>&1 || die "dump not found: $DUMP"

  local replica
  for replica in "${REPLICAS[@]}"; do
    sql instances describe "$replica" --format='value(name)' >/dev/null 2>&1 ||
      die "replica $replica not found — check the names before continuing"
  done

  log "replacing $DATABASE on $INSTANCE — replicas ${REPLICAS[*]}, operator $OPERATOR"

  # ---- last snapshot before anything destructive
  log "backing up $INSTANCE immediately before the import"
  sql backups create --instance="$INSTANCE" \
    --description="recover.sh pre-import $OPERATOR" >/dev/null
  local pre_import
  pre_import="$(sql backups list --instance="$INSTANCE" \
    --sort-by='~windowStartTime' --limit=1 --format='value(id)')"
  log "pre-import backup: $pre_import"

  # ---- pause replicas so they do not serve the drop-and-recreate window
  trap resume_trap EXIT INT TERM
  set_replication off

  block_connections

  log "dropping and recreating $DATABASE"
  sql databases delete "$DATABASE" --instance="$INSTANCE" --quiet >/dev/null ||
    die "could not drop $DATABASE"
  # A fresh database carries default privileges, so the revokes above do not survive it.
  sql databases create "$DATABASE" --instance="$INSTANCE" >/dev/null ||
    die "could not recreate $DATABASE — the database is now missing, restore backup $pre_import"

  # The import connects as $DB_USER, so the block has to come off first. From here until the
  # import finishes, CMS pods can reconnect — they will error against the empty schema
  # rather than write anything useful.
  allow_connections

  log "importing $DUMP (this is the long part)"
  sql import sql "$INSTANCE" "$DUMP" --database="$DATABASE" --user="$DB_USER" --quiet >/dev/null ||
    die "import failed — $DATABASE is partial. Re-run, or restore backup $pre_import"

  # ---- replication back on, and the trap retired
  trap - EXIT INT TERM
  set_replication on

  for replica in "${REPLICAS[@]}"; do wait_runnable "$replica"; done

  cat >&2 <<EOF

──────────────────────────────────────────────────────────────────────
Import complete. Access and replication are back on.

Replica reads break while each replica replays the drop and reload — expected, not a
fault. Lag is not readable from gcloud; watch it in Cloud Monitoring:

  database/postgresql/replication/replica_byte_lag   (filter to $INSTANCE)

Then follow the verification steps in the runbook: check CMS pods, the primary, a
replica-served page, and media rendering. A page visible on the primary but not the
replica means replication has not caught up yet.

Backups kept: $pre_import (pre-import) and the discovery backup from the prepare step.
Keep both until this is signed off.

When done:

  $0 cleanup --env=$ENV --gcp-project=$PROJECT --dump=$DUMP
──────────────────────────────────────────────────────────────────────
EOF

}

# ══════════════════════════════════════════════════════════════════ cleanup

cmd_cleanup() {
  parse_args "$@"

  require_arg "--env" "${ENV:-}" "dev, stage or prod"
  require_arg "--gcp-project" "${PROJECT:-}" "this file holds no project IDs"

  config
  require_gcloud

  # Deliberately does not touch the backups. They are the only way back if a problem shows
  # up days later, and they cost almost nothing.
  local orphans
  if [[ -n "${SCRATCH:-}" ]]; then
    # Named explicitly. Use this when another recovery may be in flight — the sweep below
    # would take its throwaway instance with it.
    [[ "$SCRATCH" == "${INSTANCE}-recover-"* ]] ||
      die "--scratch must be a throwaway instance of $INSTANCE (expected ${INSTANCE}-recover-*, got: $SCRATCH)"
    orphans="$SCRATCH"
  else
    orphans="$(sql instances list --filter="name ~ ^${INSTANCE}-recover-" \
      --format='value(name)' 2>/dev/null)" || true
  fi

  if [[ -n "$orphans" ]]; then
    local inst
    while IFS= read -r inst; do
      log "deleting throwaway instance $inst"
      sql instances delete "$inst" --quiet >/dev/null ||
        warn "could not delete $inst — delete it by hand, it is billable"
    done <<<"$orphans"
  else
    log "no throwaway instances to delete"
  fi

  if [[ -n "${DUMP:-}" ]] && gcloud storage ls "$DUMP" >/dev/null 2>&1; then
    log "deleting $DUMP"
    gcloud storage rm "$DUMP" >/dev/null || warn "could not delete $DUMP"
  fi

  cat >&2 <<EOF

Cleanup done for $INSTANCE.

Kept on purpose: the discovery and pre-import backups. Both are on $INSTANCE under its
normal retention.
EOF
}

# ══════════════════════════════════════════════════════════════════ break-glass

cmd_resume_replication() {
  parse_args "$@"
  require_arg "--env" "${ENV:-}" "dev, stage or prod"
  require_arg "--gcp-project" "${PROJECT:-}" "this file holds no project IDs"
  config
  require_gcloud
  set_replication on
  log "done. Confirm lag is falling in Cloud Monitoring: database/postgresql/replication/replica_byte_lag"
}

cmd_allow_connections() {
  parse_args "$@"
  require_arg "--env" "${ENV:-}" "dev, stage or prod"
  require_arg "--gcp-project" "${PROJECT:-}" "this file holds no project IDs"
  require_arg "--bucket" "${BUCKET:-}" "the db_sync bucket name"
  require_arg "--database" "${DATABASE:-}" "the database name"
  config
  require_gcloud
  allow_connections
}

# ══════════════════════════════════════════════════════════════════ dispatch

case "${1:-}" in
  prepare) shift && cmd_prepare "$@" ;;
  restore) shift && cmd_restore "$@" ;;
  cleanup) shift && cmd_cleanup "$@" ;;
  resume-replication) shift && cmd_resume_replication "$@" ;;
  allow-connections) shift && cmd_allow_connections "$@" ;;
  # Prints the usage block: from its first line to the blank line that ends it. Anchored
  # on the title rather than a line number, so neither the licence header above it nor
  # anything else inserted at the top of the file can truncate it.
  -h | --help | "") sed -n '/^# Database recovery for Bedrock\./,/^$/p' "$0" | sed 's/^#$//; s/^# \{0,1\}//' >&2 ;;
  *) die "unknown command: $1 (expected prepare, restore, cleanup, resume-replication or allow-connections)" ;;
esac
