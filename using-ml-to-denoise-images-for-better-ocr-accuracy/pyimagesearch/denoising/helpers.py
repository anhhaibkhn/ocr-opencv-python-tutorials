""" This file contains a single function: blur_and_threshold, 
which applies a combination of smoothing and thresholding as a pre-processing step for our documents. """
# import the necessary packages
import numpy as np
import cv2

def blur_and_threshold(image, eps = 1e-7):
    """ Blur and Threshold Helper Function
    @para: image: The input image that we’ll pre-process.
    @para: eps: An epsilon value used to prevent division by zero

    """
    # apply a median blur to the image and then subtract the blurred
    # image from the original image to approximately the foreground 
    blur = cv2.medianBlur(image, 5)
    fore_ground = image.astype("float") - blur 

    # threshold the foreground image by setting any pixels with a value greater than zero to zero
    fore_ground[fore_ground > 0 ] = 0

    # apply min/max scaling to bring the pixel intensities to the range [0, 1]
    minVal = np.min(fore_ground)
    maxVal = np.max(fore_ground)
    fore_ground = (fore_ground - minVal) / (maxVal - minVal + eps)
    # return the foreground-approximated image
    return fore_ground
