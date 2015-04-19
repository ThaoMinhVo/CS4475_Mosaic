import cv2
import numpy as np
import os

image_dir = "images" # Folder for original images 
resize_dir = "resized" # Folder for resized images 
output_dir = "output" 
image_files = os.listdir(image_dir)
file_extensions = ["jpg", "jpeg", "png"]
src_img = cv2.imread("image1.jpg")

# Resizes input images to 25 x 25 pixels
def resizeImages(images):
	for img in images:
		extension = img.split(".")[-1].lower()
		if extension not in file_extensions:
			images.remove(img) 
		else:
			image = cv2.imread(os.path.join(image_dir,img))
			# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			resized = cv2.resize(image, (25,25))
			cv2.imwrite(resize_dir + "/" + img, resized)

	# Returns array of resized images
	return images

# Average color of image
def avgRGB(img):
	avg = cv2.mean(img)
	avg = avg[:3]
	return avg

# Compares color of pixel with averages of images. 
# Chooses image closet to pixel's color
def compareColor(pixel,images):

	# Return image 
	return 

# Put pictures together 
def putTogether(src, images):
	height, width, depth = src.shape

	for row in range(len(src)):
		for col in range(len(src[row])):
			px = src[row,col]
			compareColor(px,images)

	# Insert code to put images from compareColor together 


image_files = resizeImages(image_files)
putTogether(src_img, image_files)


