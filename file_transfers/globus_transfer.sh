#!/bin/bash

# Set your source and destination Globus endpoints
# Endpoint values can be found within the Globus GUI for a collection
SOURCE_GLOBUS_COLLECTION_ID="XXX"
DEST_GLOBUS_COLLECTION_ID="XXX"

# Set source and destination directories
SOURCE_DIR="path/to/source/directory/"
DEST_DIR="path/to/destination/directory/"

# Submit batch Globus transfer request using file_list.txt
# Include option to preserve source timestamps
# Only transfer over files that either do not yet exist in the destination directory
# or have a more recent timestamp of the version of files that do exist
globus transfer $SOURCE_GLOBUS_COLLECTION_ID:$SOURCE_DIR $DEST_GLOBUS_COLLECTION_ID:$DEST_DIR \
    --label "CLI Batch" \
    --batch file_list.txt \
    --preserve-timestamp \
    --sync-level mtime

echo "Transfer submitted!"
