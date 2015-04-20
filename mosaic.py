import cv2
import numpy as np
import os
import math

image_dir = "images"  # Folder for original images
resize_dir = "resized"  # Folder for resized images
output_dir = "output"
image_files = os.listdir(image_dir)
file_extensions = ["jpg", "jpeg", "png"]
src_img = cv2.imread("image1.jpg", cv2.IMREAD_GRAYSCALE)

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
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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


# compares all resized images (25x17)  with a 25x17 block on the main Image
# the image with the smallest color difference from the block on the image
# will be used to fill in the mosaic
#   Args:
#      mainImg (numpy.ndarray) : greyscale or color image represented as a
#                            numpy array
#      images (nump.ndarray list) : list of images to be used in the mosaic
#
#   Returns:
#       mainImg (numpy.ndarray) : the final mosaic

def mosaic(mainImg, images):

    for x in range(0, mainImg.shape[0], 25): #starting x coordinate of block
        for y in range(0, mainImg.shape[1], 17): #starting y coordinate of block
            smallest_difference = 110000
            bestMatchImage = images[0]
            for img in images:
                difference = 0
                for j in range(25): #column of block
                    for k in range(17): #row of block
                        difference += math.sqrt(pow(img[j][k] - mainImg[x+j][y+k], 2))
                if difference < smallest_difference:
                    smallest_difference = difference
                    bestMatchImage = img
            for w in range(25): #column of block
                    for z in range(17): #row of block
                        mainImg[x+w][y+z] = bestMatchImage[w][z]

    # Return image
    return mainImg


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


