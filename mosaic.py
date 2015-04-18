import cv2
import numpy as np
import os

image_dir = "images" # Folder for original images 
resize_dir = "resized" # Folder for resized images 
output_dir = "output" 
image_files = os.listdir(image_dir)
file_extensions = ["jpg", "jpeg", "png"]

# Resizes input images to 25 x 25 pixels
def resizeImages(images):
	for img in images:
		extension = img.split(".")[-1].lower()
		if extension not in file_extensions:
			images.remove(img) 
		else:
			image = cv2.imread(os.path.join(image_dir,img))
			resized = cv2.resize(image, (25,25))
			cv2.imwrite(resize_dir + "/" + img, resized)

	# Returns array of resized images
	return images

resizeImages(image_files)

