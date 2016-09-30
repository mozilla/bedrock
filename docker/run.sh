#!/bin/bash -xe

RUN_SUPERVISOR=$(echo "$RUN_SUPERVISOR" | tr '[:upper:]' '[:lower:]')

if [[ "$RUN_SUPERVISOR" == "true" ]]; then
  exec docker/run-supervisor.sh
else
  exec docker/run-prod.sh
fi
