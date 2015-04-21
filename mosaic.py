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
# !! testing out a smaller resolutuon of image1.jpg
# src_img = cv2.imread("image1 copy.jpg", cv2.IMREAD_GRAYSCALE)
src_img = cv2.imread("image1.jpg")
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
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(image, (25, 17))
            cv2.imwrite(resize_dir + "/" + img, resized)

    # Returns array of resized images
    return images


# Average color of little image (not the source)
#   Args:
#    img (numpy.ndarray) : greyscale or color image represented as a
#                            numpy array
#   Returns:
#    avg (numpy.ndarray) : tuple with 4 values mean values of (BGR)
#                               (last value can be ignored)
def avgRGB(img):
    avg = cv2.mean(img)
    # avg = avg[0] # for grayscale
    avg = avg[:3]
    # print avg
    return avg


# ?? maybe make a method to find the average RGB of a block ??  


def bestMatchImage(mainImg, images):
    difference = 0
    bestMatchImage = images[0]
    # mosaic_img is array to store images for final image
    # ?? If output image is same as original, then ?? 
    # mosaic_img = np.zeros((mainImg.shape[0], maingImg.shape[1], 3))
    # mosaic_img = np.zeros((mainImg.shape[0]*17, mainImg.shape[1]*25,3))
    progress = 0 # lets me keep track of how long until program finishes
    image_size = mainImg.shape[0]*mainImg.shape[1]


    # Note: opencv stores image coordinates backwards (height, width)
    for x in range(0, mainImg.shape[1], 25):  # 0 to width of image (ex. 500)
        for y in range(0, mainImg.shape[0], 17):  # 0 to height of image (ex. 333)
            progress += 1
            # ?? Might be different since you're working with blocks ?? 
            print progress, "out of", image_size, "pixels"
            # smallest_difference = 255 # for grayscale
            smallest_difference = np.sqrt(3*np.power(255,2))

            for img in images:
                image_name = img
                img = cv2.imread("resized/"+img)
                difference = 0
                for j in range(25): #column of block
                    for k in range(17): #row of block
                        # print ' X:', x, 'J:', j, ' Y:', y, 'K:', k
                        difference += math.sqrt(np.power(mainImg[x+j, y+k, 0] - img[x, y, 0], 2) +
                                                np.power(mainImg[x+j, y+k, 1] - img[x, y, 1], 2) +
                                                np.power(mainImg[x+j, y+k, 2] - img[x, y, 2], 2))
                # difference = np.sqrt(np.power(mainImg[x,y,0]-avgRGB(img)[0],2) +
                #              np.power(mainImg[x,y,1]-avgRGB(img)[1],2) +
                #              np.power(mainImg[x,y,2]-avgRGB(img)[2],2))
                # difference = mainImg[i][j] - avgRGB(img) # for grayscale

                if difference < smallest_difference:
                    smallest_difference = difference
                    bestMatchImage = img

            for w in range(25):  # column of block
                    for z in range(17):  # row of block
                        print ' X:', x, 'W:', w, ' Y:', y, 'Z:', z
                        mainImg[x+w, y+z] = bestMatchImage[w, z]

            # index = (i, j)
            # insertImage(mosaic_img, bestMatchImage, index)


    return mainImg


# insert picture into pixel of original image
# ?? change to put image into block ?? 
def insertImage(mosaic_img, image, index):
    for i in range(index[0]*17, index[0]*17+17):
        for j in range(index[1]*25, index[1]*25+25):
            # print (i,j)
            mosaic_img[i, j] = image[i%17,j%25]


image_files = resizeImages(image_files)
mosaic = bestMatchImage(src_img, image_files)

# Saves mosaic image to computer
cv2.imwrite("mosaic.jpg", mosaic)



