#!/usr/bin/env bash

# Continuous deployment to solar.coala.io
# This script is meant to run on solar.coala.io

# Execute this script in a CI environment with
# the required SSH added to the agent, with
# this command:
# $ ssh solar.coala.io "bash -s" < /path/to/script

set -e -x

WORK_DIR=/opt/solar/corobo

fail() {
    echo "FAIL: $*"
    exit 1
}

cd $WORK_DIR || \
    fail "It looks like $WORK_DIR doesn't exist"

docker-compose pull || \
    fail "An error has occured during updating the image(s)"

docker-compose up --force-recreate -d || \
    fail "An error has occured during deploying the container(s)"

sleep 5s

docker-compose ps
