import cv2
import os
from skimage.metrics import structural_similarity as ssim

# =================== Configuration ===================
BASE_DIR = "./"
INPUT_FOLDER = os.path.join(BASE_DIR, "5.quali_input")  # Input folder with raw images
OUTPUT_FOLDER = os.path.join(BASE_DIR, "6.quali_output")  # Output directory for deduplicated images
SIMILARITY_THRESHOLD = 0.95  # SSIM threshold for duplicate detection (0.0 - 1.0)
EDGE_THRESHOLD = 100  # Minimum edge density for sharp images
# =====================================================

def calculate_ssim(image1, image2):
    """
    Calculates the SSIM (Structural Similarity Index) between two images.

    Args:
        image1 (numpy.ndarray): First image.
        image2 (numpy.ndarray): Second image.

    Returns:
        float: SSIM value (0.0 - 1.0).
    """
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Resize the second image if necessary
    if gray1.shape != gray2.shape:
        gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))

    score, _ = ssim(gray1, gray2, full=True)
    return score

def calculate_edge_density(image):
    """
    Calculates the edge density of an image using Canny edge detection.

    Args:
        image (numpy.ndarray): Input image.

    Returns:
        int: Number of edge pixels in the image.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return cv2.countNonZero(edges)

def deduplicate_images(input_folder, output_folder, similarity_threshold, edge_threshold):
    """
    Removes duplicates based on SSIM and edge density.

    Args:
        input_folder (str): Directory containing raw images.
        output_folder (str): Directory to store high-quality unique images.
        similarity_threshold (float): SSIM threshold for duplicate detection.
        edge_threshold (int): Minimum edge density value for sharp images.
    """
    os.makedirs(output_folder, exist_ok=True)
    images = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    kept_images = []

    for i, image_path1 in enumerate(images):
        image1 = cv2.imread(image_path1)
        duplicate_found = False

        # Check for duplicates with already saved images
        for image_path2 in kept_images:
            image2 = cv2.imread(image_path2)
            score = calculate_ssim(image1, image2)

            if score > similarity_threshold:
                duplicate_found = True
                break

        # Save the image if it is not a duplicate and meets quality criteria
        if not duplicate_found:
            edge_density = calculate_edge_density(image1)
            if edge_density > edge_threshold:
                kept_images.append(image_path1)
                output_path = os.path.join(output_folder, os.path.basename(image_path1))
                cv2.imwrite(output_path, image1)
                print(f"Saved: {output_path}")

if __name__ == "__main__":
    print("Starting Quality Control...")
    deduplicate_images(INPUT_FOLDER, OUTPUT_FOLDER, SIMILARITY_THRESHOLD, EDGE_THRESHOLD)
    print("Quality Control completed. Results saved in the output folder.")
