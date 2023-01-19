import os
import cv2

# Define the path to the directory containing the original images
input_dir = "/home/hafeez/Desktop/all_images"

# Define the path to the directory where the cropped images will be saved
output_dir = "/home/hafeez/Desktop/cropped_images"
'''
# Create the output directory if it doesn't already exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
'''
# Loop through all the files in the input directory
for file_name in os.listdir(input_dir):
    # Check if the file is an image
    if file_name.endswith(".jpg"):
        # Load the image
        img = cv2.imread(os.path.join(input_dir, file_name))

        # Get image dimensions
        height, width, _ = img.shape

        # Define the height to crop from the bottom
        crop_height = 800

        # Crop the image
        cropped_img = img[:height-crop_height, :width]
        '''
        img[:height-crop_height, :width]: is the same as img[:1920-100, :1080], it will select the slice of the image from the first pixel (0th index) of the height to the 1820th pixel of the height, and from the first 
        pixel (0th index) of the width to the 1080th pixel of the width. So, this slicing operation will select the portion of the image from the top to height-crop_height, which is the same as removing the last crop_height
        pixels of the image.
        '''
        # Save the cropped image to the output directory
        cv2.imwrite(os.path.join(output_dir, file_name), cropped_img)