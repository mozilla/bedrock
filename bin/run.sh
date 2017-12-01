#!/bin/bash -xe

RUN_SUPERVISOR=$(echo "${RUN_SUPERVISOR:-true}" | tr '[:upper:]' '[:lower:]')

if [[ "$RUN_SUPERVISOR" == "true" ]]; then
  exec bin/run-supervisor.sh
else
  exec bin/run-prod.sh
fi
