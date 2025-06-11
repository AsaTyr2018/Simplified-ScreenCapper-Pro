#!/bin/bash
set -e

# Folder structure relative to the base directory
BASE_DIR="$(dirname "$(dirname "$(realpath "$0")")")"
SOURCE_DIR="${BASE_DIR}/2.cap_output"
TARGET_DIR="${BASE_DIR}/3.face_input"
ARCHIVE_DIR="${BASE_DIR}/archiv/1.cap"
TASK_FILE="${BASE_DIR}/00.scripts/task_running_TransferCapToFace"

echo "Starting transfer script: CAP -> FACE"

# Create task indicator
touch "$TASK_FILE"
trap 'rm -f "$TASK_FILE"' EXIT

# Ensure the archive folder exists
mkdir -p "$ARCHIVE_DIR"

# Archive: Zip the folder and transfer it to the archive
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ZIP_NAME="${ARCHIVE_DIR}/cap_output_${TIMESTAMP}.zip"
echo "Creating ZIP archive: $ZIP_NAME"
zip -r "$ZIP_NAME" "$SOURCE_DIR" >/dev/null

shopt -s nullglob
files=("$SOURCE_DIR"/*)
if [ ${#files[@]} -gt 0 ]; then
    for file in "${files[@]}"; do
        mv "$file" "$TARGET_DIR/"
    done
else
    echo "No files to move."
fi
shopt -u nullglob
echo "Transfer completed: CAP -> FACE"
