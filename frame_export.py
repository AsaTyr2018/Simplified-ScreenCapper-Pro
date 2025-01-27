import cv2
import os
from tqdm import tqdm

# Base directories
base_dir = "./"
cap_input_dir = os.path.join(base_dir, "1.cap_input")
cap_output_dir = os.path.join(base_dir, "2.cap_output")

# Ensure directories exist
os.makedirs(cap_input_dir, exist_ok=True)
os.makedirs(cap_output_dir, exist_ok=True)

def extract_frames():
    # Search for video files in the input folder
    video_files = [f for f in os.listdir(cap_input_dir) if f.lower().endswith((".mp4", ".avi", ".mkv"))]

    if not video_files:
        print("No videos found in the input folder.")
        return

    for video_file in tqdm(video_files, desc="Overall Progress", unit="Video"):
        video_path = os.path.join(cap_input_dir, video_file)
        video_name = os.path.splitext(video_file)[0]

        # Open video file
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        with tqdm(total=total_frames, desc=f"Processing: {video_file}", unit="Frame") as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Save frame directly to 2.cap_output
                frame_path = os.path.join(cap_output_dir, f"{video_name}_frame_{frame_count:05d}.jpg")
                cv2.imwrite(frame_path, frame)

                frame_count += 1
                pbar.update(1)

        cap.release()
        print(f"Frames extracted: {frame_count} frames saved to {cap_output_dir}")

if __name__ == "__main__":
    print("Starting frame extraction for anime videos...")
    extract_frames()
    print("All videos have been processed.")
