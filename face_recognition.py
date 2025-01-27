import os
import cv2
from tqdm import tqdm
from ultralytics import YOLO

# Base directories
base_dir = "./"
model_dir = os.path.join(base_dir, "00.scripts/model")
face_input_dir = os.path.join(base_dir, "3.face_input")
face_output_dir = os.path.join(base_dir, "4.face_output")

# YOLOv8 model path
yolo_model_path = os.path.join(model_dir, "AniRef40000-l-epoch50.pt")

# Ensure directories exist
os.makedirs(face_input_dir, exist_ok=True)
os.makedirs(face_output_dir, exist_ok=True)

# Lazy loader for YOLO model
def load_yolo_model():
    if not os.path.exists(yolo_model_path):
        raise FileNotFoundError(f"YOLO model not found: {yolo_model_path}")
    return YOLO(yolo_model_path)

# Function: Detect faces using YOLOv8
def detect_faces(frame, frame_count, yolo_model):
    results = yolo_model(frame)
    detected_faces = []

    # Results as bounding boxes
    for i, box in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Bounding box coordinates
        conf = box.conf[0]  # Confidence
        if conf >= 0.5:  # Confidence threshold
            face_image = frame[y1:y2, x1:x2]
            output_path = os.path.join(face_output_dir, f"frame_{frame_count}_face_{i}.jpg")
            cv2.imwrite(output_path, face_image)
            detected_faces.append(output_path)

    return detected_faces

# Function: Process frames
def process_faces():
    frame_files = [f for f in os.listdir(face_input_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    if not frame_files:
        print("No frames found in the input directory.")
        return

    yolo_model = load_yolo_model()
    print(f"YOLO model loaded successfully: {yolo_model_path}")

    print(f"\nProcessing frames from: {face_input_dir}")
    for frame_file in tqdm(frame_files, desc="Processing", unit="Frame"):
        frame_path = os.path.join(face_input_dir, frame_file)
        frame = cv2.imread(frame_path)
        frame_count = int(os.path.splitext(frame_file)[0].split('_')[-1])  # Optional: Extract frame index

        # Detect faces
        detect_faces(frame, frame_count, yolo_model)

    print(f"Processing complete: Results in {face_output_dir}")

# Main program
if __name__ == "__main__":
    # Task indicator
    task_file = "./00.scripts/task_running_Face01"
    open(task_file, 'w').close()  # Start task

    try:
        print("Starting face detection with YOLOv8...")
        process_faces()
    finally:
        # Remove task indicator
        if os.path.exists(task_file):
            os.remove(task_file)

    print("All frames have been processed.")