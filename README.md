# Simplified ScreenCapper Pro

## Overview

Simplified ScreenCapper Pro is a modular and automated pipeline for processing video files into high-quality frames and images. This updated version of the original Simplified ScreenCapper includes enhanced output quality, advanced features, and greater customization options. The pipeline follows a step-by-step process with separate scripts for each stage, ensuring flexibility and ease of extension.

---

## Features

- **High-Quality Output**: Improved precision for frame extraction and face recognition.
- **Modular Design**: Independent scripts for each step allow easy replacement or extension.
- **Automation-Friendly**: Supports manual execution or optional daemon automation.
- **Archiving and Cleanup**: Automatically archives intermediate results and cleans up temporary files after processing.
- **Customizable Quality Metrics**: Use SSIM and edge detection thresholds to filter out duplicates and blurry images.

---

## Workflow Pipeline

### 1. Frame Extraction (`frame_export.py`)
- **Input**: Video files from `1.cap_input/`.
- **Output**: Extracted frames in `2.cap_output/`.
- **Task Indicator**: `task_running_Cap01`.

### 2. Frame Transfer (`transfer-cap-face.sh`)
- **Input**: Frames from `2.cap_output/`.
- **Output**: Frames moved to `3.face_input/`.
- **Archive**: Zipped frames saved in `archiv/1.cap/`.
- **Task Indicator**: `task_running_TransferCapToFace`.

### 3. Face Recognition (`face_recognition.py`)
- **Input**: Frames from `3.face_input/`.
- **Output**: Detected faces saved in `4.face_output/`.
- **Model**: YOLOv8 (`AniRef40000-l-epoch50.pt`).
- **Model Source**: The YOLOv8 model must be downloaded from [AniRef YOLOv8 GitHub Repository](https://github.com/SoulflareRC/AniRef-yolov8). Ensure you download the `AniRef40000-l-epoch50.pt` file and place it in the `00.scripts/model/` directory.
- **Task Indicator**: `task_running_Face01`.

### 4. Face Transfer (`transfer-face-quali.sh`)
- **Input**: Detected faces from `4.face_output/`.
- **Output**: Faces moved to `5.quali_input/`.
- **Archive**: Zipped faces saved in `archiv/2.face/`.
- **Task Indicator**: `task_running_TransferFaceToQuali`.

### 5. Quality Control (`quality_check.py`)
- **Input**: Faces from `5.quali_input/`.
- **Output**: Filtered, high-quality images in `6.quali_output/`.
- **Task Indicator**: `task_running_QualityCheck`.

### 6. Final Transfer and Cleanup (`transfer-output.sh`)
- **Input**: Final images from `6.quali_output/`.
- **Output**: Images moved to `output/`.
- **Archive**: Zipped final images saved in `archiv/3.quali/`.
- **Cleanup**: Clears all process folders (`1.cap_input` to `6.quali_output`).
- **Task Indicator**: `task_running_TransferOutput`.

### 7. Queue Pruning (`pruning.sh`)
- **Purpose**: Manually clear all queue folders.
- **Safety**: Asks for confirmation before deleting files.

---

## Folder Structure

```plaintext
<Base Directory>/
├── 00.scripts/                # Contains all scripts
│   ├── master.sh              # Master script to control the pipeline
│   ├── frame_export.py        # Frame extraction
│   ├── face_recognition.py    # Face recognition
│   ├── quality_check.py       # Quality control
│   ├── transfer-cap-face.sh   # Transfer: CAP -> FACE
│   ├── transfer-face-quali.sh # Transfer: FACE -> QUALI
│   ├── transfer-output.sh     # Transfer: QUALI -> OUTPUT
│   ├── pruning.sh            # Clear all queue folders
│   └── model/                 # YOLOv8 model file
│       └── AniRef40000-l-epoch50.pt
├── 1.cap_input/               # Input folder for raw videos
├── 2.cap_output/              # Extracted frames
├── 3.face_input/              # Frames for face recognition
├── 4.face_output/             # Detected faces
├── 5.quali_input/             # Faces for quality control
├── 6.quali_output/            # High-quality output
├── output/                    # Final processed images
└── archiv/                    # Archive folders
    ├── 1.cap/
    ├── 2.face/
    └── 3.quali/
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Required Python libraries:
  ```bash
  pip install opencv-python-headless tqdm ultralytics scikit-image
  ```
- System packages:
  ```bash
  sudo apt update
  sudo apt install zip unzip
  ```

### Automated Installation with `install.sh`
To simplify the setup process, an `install.sh` script is provided. This script will:

1. Create the necessary folder structure.
2. Move all pipeline scripts into the `00.scripts` directory.
3. Install required Python libraries.
4. Install necessary system packages.
5. Set executable permissions for the scripts.

#### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/AsaTyr2018/Simplified-ScreenCapper-Pro
   cd Simplified-ScreenCapper-Pro
   ```
2. Run the installation script:
   ```bash
   ./install.sh
   ```
3. Follow the prompts:
   - You can specify a custom base directory or use the current directory as the default.

4. Download the YOLOv8 model:
   - Visit the [AniRef YOLOv8 GitHub Repository](https://github.com/SoulflareRC/AniRef-yolov8).
   - Download the `AniRef40000-l-epoch50.pt` model.
   - Place the model in the `00.scripts/model/` directory.
5. The installation script automatically sets execute permissions for all scripts.

---

## Running the Pipeline

### Manual Execution
Run the pipeline manually using:
```bash
<Base Directory>/00.scripts/master.sh
```

### Optional Daemon
You can optionally set up a **systemd daemon** to automate the pipeline. The daemon will check the `1.cap_input/` folder every 5 minutes and trigger the pipeline if files are detected. Refer to the `import-checker.timer` and `import-checker.service` configuration for details.

## Telemetry Dashboard

Start the dashboard server:
```bash
python3 dashboard.py
```

Agents post metrics using:
```bash
python3 telemetry_agent.py --server http://<dashboard-host>:5000/telemetry
```

The dashboard shows RAM, CPU, connected users and root storage for each agent.


---

## Planned Features

- **Classifier Integration**: Add a character classifier for identifying specific characters within frames.
- **Tagging System**: Automate metadata tagging for processed images.

If you are experienced in these areas and want to contribute, feel free to open an issue or submit a pull request!

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
