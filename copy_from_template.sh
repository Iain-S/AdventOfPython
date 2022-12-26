#!/bin/bash

# Map positional args
DAY="$1"
PATH_USERNAME_AND_LANG="$2"
SOURCE_PATH="$3"
DEST_PATH="$4"

# Make destination
DEST_PATH_WITH_SUBPATH="${DEST_PATH}/day-$DAY/$PATH_USERNAME_AND_LANG"

# Print constructed destination path
echo "Source path: ${SOURCE_PATH}"
echo "Destination path: ${DEST_PATH_WITH_SUBPATH}"
echo ""
read -rp "Press enter if ok..."

# Make path
mkdir -p  "$DEST_PATH_WITH_SUBPATH"

# Sync minimal files for the day
rsync \
    ./**/*"$DAY".py \
    "$DEST_PATH_WITH_SUBPATH"
