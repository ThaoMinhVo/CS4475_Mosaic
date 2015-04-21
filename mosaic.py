import cv2
import numpy as np
import os
import math
import pdb

image_dir = "images"  # Folder for original images
resize_dir = "resized"  # Folder for resized images
image_files = os.listdir(image_dir)
file_extensions = ["jpg", "jpeg", "png"]
# !! testing out a smaller resolutuon of image1.jpg
# src_img = cv2.imread("image1 copy.jpg", cv2.IMREAD_GRAYSCALE)
src_img = cv2.imread("image.jpg")


# Resizes input images to 25 x 17 pixels
# Keeps image dimensions but when comparing blocks
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


def avgRGBofBlock(mainImg,index):
    pixelsum = np.array([0,0,0])
    count = 0 # number of pixels

    difference_y = mainImg.shape[0] - index[0]
    difference_x = mainImg.shape[1] - index[1]

    if difference_y > 17 and difference_x > 25:
        for i in range(index[0], index[0]+17):
            for j in range(index[1], index[1]+25):
                count += 1
                pixelsum = np.add(pixelsum,mainImg[i,j])
    elif difference_y <= 17 and difference_x > 25: 
        for i in range(index[0], index[0]+difference_y):
            for j in range(index[1], index[1]+25):
                count += 1
                pixelsum = np.add(pixelsum,mainImg[i,j])
    elif difference_y > 17 and difference_x <= 25:
        for i in range(index[0], index[0]+17):
            for j in range(index[1], index[1]+difference_x):
                count += 1
                pixelsum = np.add(pixelsum,mainImg[i,j])
    else:
        for i in range(index[0], index[0]+difference_y):
            for j in range(index[1], index[1]+difference_x):
                count += 1
                pixelsum = np.add(pixelsum,mainImg[i,j])

    average = pixelsum / count
    # print "Average: ",average
    return average

def bestMatchImage(mainImg, images):
    difference = 0
    bestMatchImage = images[0]
    # mosaic_img is array to store images for final image
    mosaic_img = np.zeros((mainImg.shape[0], mainImg.shape[1],3)) 
    # progress = 0 # lets me keep track of how long until program finishes
    image_size = mainImg.shape[0]*mainImg.shape[1]
    num_blocks = (mainImg.shape[0] / 17) * (mainImg.shape[1] / 25)
    block_count = 0

    
    # Note: opencv stores image coordinates backwards (height, width)
    for i in range(0,mainImg.shape[0],17): # 0 to height of image 
        for j in range(0,mainImg.shape[1],25):  # 0 to width of image 
            # progress += 1
            # print progress, "out of", image_size, "pixels"  
            # smallest_difference = 255 # for grayscale
            smallest_difference = np.sqrt(3*np.power(255,2))

            block_index = (i,j)
            block_avg = avgRGBofBlock(mainImg, block_index)
            # print block_avg[0], block_avg[1], block_avg[2]

            for img in images:
                image_name = img
                img = cv2.imread("resized/"+img)
                difference = np.sqrt(np.power(block_avg[0]-avgRGB(img)[0],2) +
                    np.power(block_avg[1]-avgRGB(img)[1],2) +
                    np.power(block_avg[2]-avgRGB(img)[2],2))

                # difference = mainImg[i][j] - avgRGB(img) # for grayscale

                if difference < smallest_difference:
                    smallest_difference = difference
                    bestMatchImage = img

            index = (i,j)
            insertImage(mosaic_img, bestMatchImage, index)
            # print count, "out of", num_blocks



    return mosaic_img


# insert picture into pixel of original image
def insertImage(mosaic_img, image, index):

    difference = mosaic_img.shape[0] - index[0]
    d = mosaic_img.shape[1] - index[1]
    if difference > 17 and d > 25:
        for i in range(index[0], index[0]+17):
            for j in range(index[1], index[1]+25):
                mosaic_img[i,j] = image[i%17,j%25]
    elif difference <= 17 and d > 25:
        for i in range(index[0], index[0]+difference):
            for j in range(index[1], index[1]+25):
                mosaic_img[i,j] = image[i%difference,j%25]
    elif difference > 17 and d <= 25:
        for i in range(index[0], index[0]+17):
            for j in range(index[1], index[1]+d):
                mosaic_img[i,j] = image[i%17,j%d]
    else:
        for i in range(index[0], index[0]+difference):
            for j in range(index[1], index[1]+d):
                mosaic_img[i,j] = image[i%difference,j%d]



image_files = resizeImages(image_files)
mosaic = bestMatchImage(src_img, image_files)

# Saves mosaic image to computer
cv2.imwrite("mosaic.jpg",mosaic)



