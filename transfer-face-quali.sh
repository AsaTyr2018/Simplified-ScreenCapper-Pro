#!/bin/bash
set -e

# Folder structure relative to the base directory
BASE_DIR="$(dirname "$(dirname "$(realpath "$0")")")"
SOURCE_DIR="${BASE_DIR}/4.face_output"
TARGET_DIR="${BASE_DIR}/5.quali_input"
ARCHIVE_DIR="${BASE_DIR}/archiv/2.face"
TASK_FILE="${BASE_DIR}/00.scripts/task_running_TransferFaceToQuali"

echo "Starting transfer script: FACE -> QUALI"

# Create task indicator
touch "$TASK_FILE"
trap 'rm -f "$TASK_FILE"' EXIT

# Ensure the archive folder exists
mkdir -p "$ARCHIVE_DIR"

# Archive: Zip the folder and transfer it to the archive
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ZIP_NAME="${ARCHIVE_DIR}/face_output_${TIMESTAMP}.zip"
echo "Creating ZIP archive: $ZIP_NAME"
zip -r "$ZIP_NAME" "$SOURCE_DIR" >/dev/null

# Move files to the target directory
shopt -s nullglob
files=("$SOURCE_DIR"/*)
if [ ${#files[@]} -gt 0 ]; then
    mv "${files[@]}" "$TARGET_DIR/"
else
    echo "No files to move."
fi
shopt -u nullglob
echo "Transfer completed: FACE -> QUALI"
