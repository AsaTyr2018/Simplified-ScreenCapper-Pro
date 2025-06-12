#!/bin/bash
set -e

# Install script for Simplified ScreenCapper Pro

# Define base directory
read -p "Enter the base directory for installation (default: current directory): " USER_DIR
BASE_DIR="${USER_DIR:-$(pwd)}"
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Define folder structure
FOLDERS=(
    "${BASE_DIR}/00.scripts"
    "${BASE_DIR}/00.scripts/model"
    "${BASE_DIR}/1.cap_input"
    "${BASE_DIR}/2.cap_output"
    "${BASE_DIR}/3.face_input"
    "${BASE_DIR}/4.face_output"
    "${BASE_DIR}/5.quali_input"
    "${BASE_DIR}/6.quali_output"
    "${BASE_DIR}/output"
    "${BASE_DIR}/archiv/1.cap"
    "${BASE_DIR}/archiv/2.face"
    "${BASE_DIR}/archiv/3.quali"
)

# Required Python packages
REQUIREMENTS=(
    "opencv-python-headless"
    "tqdm"
    "ultralytics"
    "scikit-image"
    "psutil"
    "flask"
    "requests"
)

# Required system packages
SYSTEM_PACKAGES=(
    "zip"
    "unzip"
)

# Create folder structure
echo "Creating folder structure..."
for folder in "${FOLDERS[@]}"; do
    mkdir -p "$folder"
    echo "Created: $folder"
done

echo "Folder structure created."

# Move script files into the new 00.scripts directory
SCRIPT_FILES=(
    "master.sh"
    "frame_export.py"
    "face_recognition.py"
    "quality_check.py"
    "transfer-cap-face.sh"
    "transfer-face-quali.sh"
    "transfer-output.sh"
    "pruning.sh"
)

echo "Moving scripts to ${BASE_DIR}/00.scripts..."
for script in "${SCRIPT_FILES[@]}"; do
    if [ -f "${SCRIPT_DIR}/${script}" ]; then
        mv "${SCRIPT_DIR}/${script}" "${BASE_DIR}/00.scripts/"
        echo "Moved: ${script}"
    fi
done
echo "Scripts moved."

# Install system packages
echo "Installing required system packages..."
sudo apt update -y
for pkg in "${SYSTEM_PACKAGES[@]}"; do
    sudo apt install -y "$pkg"
done
echo "System packages installed."

# Install Python requirements
echo "Installing required Python packages..."
pip install "${REQUIREMENTS[@]}"
echo "Python packages installed."

# Ensure all scripts are executable
chmod -R +x "${BASE_DIR}/00.scripts"

# Display completion message
echo "Installation complete!"
echo "Please download the YOLOv8 model from https://github.com/SoulflareRC/AniRef-yolov8"
echo "Place the downloaded model file (AniRef40000-l-epoch50.pt) into ${BASE_DIR}/00.scripts/model"
