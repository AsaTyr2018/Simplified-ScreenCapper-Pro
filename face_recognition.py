#!/usr/bin/env python3
"""Face detection using YOLOv8."""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
from tqdm import tqdm
from ultralytics import YOLO


def load_yolo_model(model_path: Path) -> YOLO:
    """Load the YOLOv8 model."""
    if not model_path.exists():
        raise FileNotFoundError(f"YOLO model not found: {model_path}")
    return YOLO(str(model_path))


def detect_faces(frame, frame_index: int, model: YOLO, output_dir: Path) -> None:
    """Detect faces in a single frame and write them to *output_dir*."""
    results = model(frame)
    for i, box in enumerate(results[0].boxes):
        conf = float(box.conf[0])
        if conf < 0.5:
            continue
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        face_img = frame[y1:y2, x1:x2]
        out_path = output_dir / f"frame_{frame_index}_face_{i}.jpg"
        cv2.imwrite(str(out_path), face_img)


def process_faces(input_dir: Path, output_dir: Path, model_path: Path) -> None:
    """Process all frames in *input_dir* and save faces to *output_dir*."""
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = [f for f in input_dir.iterdir() if f.suffix.lower() in {".jpg", ".png", ".jpeg"}]
    if not files:
        print("No frames found in the input directory.")
        return

    model = load_yolo_model(model_path)
    print(f"YOLO model loaded successfully: {model_path}")
    print(f"\nProcessing frames from: {input_dir}")

    for frame_file in tqdm(files, desc="Processing", unit="frame"):
        frame = cv2.imread(str(frame_file))
        frame_index = int(frame_file.stem.split("_")[-1])
        detect_faces(frame, frame_index, model, output_dir)

    print(f"Processing complete: Results in {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect faces using YOLOv8")
    parser.add_argument("--base-dir", default="./", help="Base directory for input/output")
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    model_path = base_dir / "00.scripts" / "model" / "AniRef40000-l-epoch50.pt"
    input_dir = base_dir / "3.face_input"
    output_dir = base_dir / "4.face_output"
    task_file = base_dir / "00.scripts" / "task_running_Face01"

    task_file.touch()
    try:
        process_faces(input_dir, output_dir, model_path)
    finally:
        task_file.unlink(missing_ok=True)
    print("All frames have been processed.")


if __name__ == "__main__":
    main()
