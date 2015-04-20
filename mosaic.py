import cv2
import numpy as np
import os
import math
import pdb

image_dir = "images"  # Folder for original images
resize_dir = "resized"  # Folder for resized images
output_dir = "output"
image_files = os.listdir(image_dir)
file_extensions = ["jpg", "jpeg", "png"]
# testing out a smaller resolutuon of image1.jpg
src_img = cv2.imread("image1 copy.jpg", cv2.IMREAD_GRAYSCALE)
# mosaic_img = np.zeros((src_img.shape[0]*17, src_img.shape[1]*25,3))

# Input images are 500 * 333 pixels
# Resizes input images to 25 x 17 pixels
# Keeps image dimensions but when comparing blocks
#   last 10 rows will not be compared
def resizeImages(images):
    for img in images:
        extension = img.split(".")[-1].lower()
        if (extension not in file_extensions) or img.startswith('.'):
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
    avg = avg[0]
    # avg = avg[:3]
    # print avg
    return avg


def bestMatchImage(mainImg, images):
    difference = 0
    bestMatchImage = images[0]
    mosaic_img = np.zeros((mainImg.shape[0]*17, mainImg.shape[1]*25,3))
    # progress = 0 # lets me keep track of how long until program finishes

    for i in range(mainImg.shape[0]): 
        for j in range(mainImg.shape[1]): 
            # progress += 1
            # print progress
            smallest_difference = 255

            for img in images:
                image_name = img
                img = cv2.imread("resized/"+img)
                difference = mainImg[i][j] - avgRGB(img)
                # print "Difference: ",image_name, " ", progress

                if abs(difference) < smallest_difference:
                    smallest_difference = abs(difference)
                    bestMatchImage = img
                    # print smallest_difference, " ", progress

            # print best_name, " ", progress
            index = (i,j)
            insertImage(mosaic_img, bestMatchImage, index)


    return mosaic_img


# insert picture into pixel
def insertImage(mosaic_img, image, index):
    for i in range(index[0]*17, index[0]*17+17):
        for j in range(index[1]*25, index[1]*25+25):
            print (i,j)
            mosaic_img[i,j] = image[i%17,j%25]


image_files = resizeImages(image_files)
mosaic = bestMatchImage(src_img, image_files)
cv2.imwrite("mosaic.jpg",mosaic)



