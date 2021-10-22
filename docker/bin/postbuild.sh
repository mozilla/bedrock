#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -ex

# Docker-Compose does not remove the running database instace. We cannot use docker-compose
# rm here because we re-tagged the image while uploading to DockerHub.
docker rm -f `echo jenkins${JOB_NAME}${BUILD_NUMBER}| sed s/_//g`_db_1
