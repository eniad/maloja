#!/usr/bin/env bash
# cleanup.sh
#
# Remove local development files and container
rm -rf .local/
docker image rm maloja_dev