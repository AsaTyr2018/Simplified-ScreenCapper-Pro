#!/bin/bash
set -e

# Folder structure relative to the base directory
BASE_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

QUEUES=(
    "${BASE_DIR}/1.cap_input"
    "${BASE_DIR}/2.cap_output"
    "${BASE_DIR}/3.face_input"
    "${BASE_DIR}/4.face_output"
    "${BASE_DIR}/5.quali_input"
    "${BASE_DIR}/6.quali_output"
)

read -r -p "This will remove all files in the queue folders. Continue? [y/N] " CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "Pruning cancelled."
    exit 0
fi

for DIR in "${QUEUES[@]}"; do
    echo "Clearing folder: $DIR"
    rm -rf "$DIR/"*
    mkdir -p "$DIR"
done

echo "All queues have been pruned."
