import cv2
import numpy as np
import os

image_dir = "images"  # Folder for original images
resize_dir = "resized"  # Folder for resized images
output_dir = "output"
image_files = os.listdir(image_dir)
file_extensions = ["jpg", "jpeg", "png"]
src_img = cv2.imread("image1.jpg")

# Input images are 500 * 333 pixels
# Resizes input images to 25 x 17 pixels
# Keeps image dimensions but when comparing blocks
#   last 10 rows will not be compared
def resizeImages(images):
    for img in images:
        extension = img.split(".")[-1].lower()
        if extension not in file_extensions:
            images.remove(img)
        else:
            image = cv2.imread(os.path.join(image_dir, img))
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(image, (25, 17))
            cv2.imwrite(resize_dir + "/" + img, resized)

    # Returns array of resized images
    return images


# Average color of image
#   Args:
#    img (numpy.ndarray) : greyscale or color image represented as a
#                            numpy array
#   Returns:
#    avg (numpy.ndarray) : tuple with 4 values mean values of (BGR)
#                               (last value can be ignored)
def avgRGB(img):
    avg = cv2.mean(img)
    avg = avg[:3]
    return avg


# Compares color of pixel with averages of images.
# Chooses image closet to pixel's color
def compareBlock(pixel, images):
    for x in range(0, 500, 25):
        for y in range(0, 333, 17):
    # Return image
    return


# Put pictures together 
def putTogether(src, images):
    height, width, depth = src.shape

    for row in range(len(src)):
        for col in range(len(src[row])):
            px = src[row, col]
            compareBlock(px, images)

        # Insert code to put images from compareColor together


image_files = resizeImages(image_files)
putTogether(src_img, image_files)


