#!/bin/bash
set -e

# Folder structure relative to the base directory
BASE_DIR="$(dirname "$(dirname "$(realpath "$0")")")"
SOURCE_DIR="${BASE_DIR}/6.quali_output"
FINAL_OUTPUT_DIR="${BASE_DIR}/output"
ARCHIVE_DIR="${BASE_DIR}/archiv/3.quali"
TASK_FILE="${BASE_DIR}/00.scripts/task_running_TransferOutput"

echo "Starting transfer script: QUALI -> OUTPUT"

# Create task indicator
touch "$TASK_FILE"

# Ensure the archive folder exists
mkdir -p "$ARCHIVE_DIR"

# Archive: Zip the folder and transfer it to the archive
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ZIP_NAME="${ARCHIVE_DIR}/quali_output_${TIMESTAMP}.zip"
echo "Creating ZIP archive: $ZIP_NAME"
zip -r "$ZIP_NAME" "$SOURCE_DIR" >/dev/null

# Move files to the final output directory
mkdir -p "$FINAL_OUTPUT_DIR"
mv "$SOURCE_DIR/"* "$FINAL_OUTPUT_DIR/"
echo "Transfer completed: QUALI -> OUTPUT"

# Cleaner: Clear all processing folders (except archive)
for DIR in "${BASE_DIR}/1.cap_input" "${BASE_DIR}/2.cap_output" "${BASE_DIR}/3.face_input" "${BASE_DIR}/4.face_output" "${BASE_DIR}/5.quali_input" "${BASE_DIR}/6.quali_output"; do
    echo "Clearing folder: $DIR"
    rm -rf "$DIR/"*
done

echo "All processing folders have been cleared."

# Remove task indicator
rm "$TASK_FILE"
