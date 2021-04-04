#!/usr/bin/env bash
# maloja_install.sh
#
# Installs, starts, and stops the server to setup local files. This can't be done in Dockerfiles because the persistent volumes are mounted after build.

#
python setup.py install
sleep 5
maloja start
sleep 5

# Import scrobbles if a scrobbles.csv file exists
FILE=scrobbles.csv
if test -f "$FILE"; then
    maloja import $FILE
fi

maloja stop

# Remove build artifacts. They are not used in local development
rm -rf dist/ build/ malojaserver.egg-info/

# Change ownership of data_files to local user.
chown -R 1000:1000 .local