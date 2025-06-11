#!/usr/bin/env python3
"""Basic quality control utilities."""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
from skimage.metrics import structural_similarity as ssim
import logging


def calculate_ssim(image1, image2) -> float:
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    if gray1.shape != gray2.shape:
        gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))
    score, _ = ssim(gray1, gray2, full=True)
    return float(score)


def calculate_edge_density(image) -> int:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return int(cv2.countNonZero(edges))


def deduplicate_images(input_folder: Path, output_folder: Path, similarity_threshold: float, edge_threshold: int) -> None:
    output_folder.mkdir(parents=True, exist_ok=True)
    images = [p for p in input_folder.iterdir() if p.suffix.lower() in {".jpg", ".png", ".jpeg"}]
    kept_images: list[Path] = []

    for image_path1 in images:
        image1 = cv2.imread(str(image_path1))
        duplicate_found = False
        for image_path2 in kept_images:
            image2 = cv2.imread(str(image_path2))
            score = calculate_ssim(image1, image2)
            if score > similarity_threshold:
                duplicate_found = True
                break
        if not duplicate_found:
            edge_density = calculate_edge_density(image1)
            if edge_density > edge_threshold:
                kept_images.append(image_path1)
                output_path = output_folder / image_path1.name
                cv2.imwrite(str(output_path), image1)
                logging.info("Saved: %s", output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Perform quality control on images")
    parser.add_argument("--base-dir", default="./", help="Base directory for input/output")
    parser.add_argument("--ssim", type=float, default=0.95, help="SSIM threshold for duplicates")
    parser.add_argument("--edge", type=int, default=100, help="Minimum edge density")
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    input_dir = base_dir / "5.quali_input"
    output_dir = base_dir / "6.quali_output"
    task_file = base_dir / "00.scripts" / "task_running_QualityCheck"

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.info("Starting Quality Control...")
    task_file.touch()
    try:
        deduplicate_images(input_dir, output_dir, args.ssim, args.edge)
    finally:
        task_file.unlink(missing_ok=True)
    logging.info("Quality Control completed. Results saved in the output folder.")


if __name__ == "__main__":
    main()
