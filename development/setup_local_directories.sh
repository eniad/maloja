#!/usr/bin/env bash
# setup_local_direcories.sh
#
# Setup local files for local development.

# Check for .env file
FILE=.env
if test -f "$FILE"; then
    echo "$FILE exist"
else
    echo "$FILE does not exist"
    exit 1
fi

# Make a local data_files directory
DIR=.local/data_files
if test -d $DIR; then
    echo "$DIR already exists"
else
    mkdir -p $DIR
    cp -r maloja/data_files .local/
fi

# Build and run the container once to setup local files.
docker build -f Dockerfile --target dev_setup -t maloja_dev .
docker run -it --rm -p 42010:42010 -v /home/$USER/git/maloja:/usr/src/app -v /home/$USER/git/maloja/.local:/data --env-file .env maloja_dev

# Check that the server successfully shut down within the last minute.
# This check only works because the log files are over written at build.
DATE=$(date +"%Y/%m/%d")
TESTSTRING="Server shutting down..."
TESTFILE=".local/data_files/logs/main.log"
if grep -q -E "$DATE.*$TESTSTRING" "$TESTFILE"; then
    msg="$DIR setup is complete. Use docker run to start your local dev server."
else
    msg="WARNING: Expecting \"$TESTSTRING\" at $DATE logged to $TESTFILE. Check local data_files."
    echo $msg
    exit 1
fi

# Re-build the container to change the entrypoint.
docker build -f Dockerfile --target dev -t maloja_dev .

echo $msg