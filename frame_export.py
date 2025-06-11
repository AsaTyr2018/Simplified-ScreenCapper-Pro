#!/usr/bin/env python3
"""Extract frames from video files."""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
from tqdm import tqdm
import logging


def extract_frames(input_dir: Path, output_dir: Path) -> None:
    """Extract frames from all videos in *input_dir* into *output_dir*."""
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    video_files = [f for f in input_dir.iterdir() if f.suffix.lower() in {".mp4", ".avi", ".mkv"}]
    if not video_files:
        logging.info("No videos found in the input folder.")
        return

    for video_file in tqdm(video_files, desc="Overall Progress", unit="video"):
        cap = cv2.VideoCapture(str(video_file))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_count = 0
        video_name = video_file.stem

        with tqdm(total=total_frames, desc=f"Processing: {video_file.name}", unit="frame") as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame_path = output_dir / f"{video_name}_frame_{frame_count:05d}.jpg"
                cv2.imwrite(str(frame_path), frame)
                frame_count += 1
                pbar.update(1)
        cap.release()
        logging.info("Frames extracted: %d frames saved to %s", frame_count, output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract frames from videos")
    parser.add_argument("--base-dir", default="./", help="Base directory for input/output")
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    input_dir = base_dir / "1.cap_input"
    output_dir = base_dir / "2.cap_output"

    task_file = base_dir / "00.scripts" / "task_running_Cap01"
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    logging.info("Starting frame extraction for anime videos...")
    task_file.touch()
    try:
        extract_frames(input_dir, output_dir)
    finally:
        task_file.unlink(missing_ok=True)
    logging.info("All videos have been processed.")


if __name__ == "__main__":
    main()
