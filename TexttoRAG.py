import cv2
import pytesseract
from PIL import Image
import os

# Get the current directory
current_directory = "/mnt/g/My Drive/Eileen"

# Create 'txt_conversion' folder if it doesn't exist
output_folder = os.path.join(current_directory, "txt_conversion")
os.makedirs(output_folder, exist_ok=True)

# Supported image formats (add more if needed)
supported_formats = [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]

# Loop through all files in the directory
for file_name in os.listdir(current_directory):
    file_path = os.path.join(current_directory, file_name)
    base_name, file_extension = os.path.splitext(file_name)

    # Skip files that are not images or already processed
    if file_extension.lower() not in supported_formats:
        continue

    txt_file_path = os.path.join(output_folder, f"{base_name}.txt")

    # Skip files that already have a corresponding text file
    if os.path.exists(txt_file_path):
        print(f"Skipping {file_name}, already processed.")
        continue

    try:
        # Load and pre-process the image
        image = cv2.imread(file_path)

        # Check if the image is loaded successfully
        if image is None:
            raise ValueError(f"Unable to load image at {file_path}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Save the pre-processed image (optional step, you can skip this)
        processed_image_path = "processed.png"
        cv2.imwrite(processed_image_path, threshold)

        # Perform OCR
        text = pytesseract.image_to_string(Image.open(processed_image_path))

        # Save the extracted text to a .txt file in the 'txt_conversion' folder
        with open(txt_file_path, "w") as f:
            f.write(text)

        print(f"Processed {file_name}, result saved to {txt_file_path}")

    except Exception as e:
        # If there's an error, save the error message in a .txt file with the same base name
        error_txt_file_path = os.path.join(output_folder, f"{base_name}_error.txt")
        with open(error_txt_file_path, "w") as f:
            f.write(f"Error processing {file_name} ({file_extension}): {str(e)}\n")
            f.write(f"File format: {file_extension}\n")

        print(f"Error processing {file_name}. Error details saved to {error_txt_file_path}")
