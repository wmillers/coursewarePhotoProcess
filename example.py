import cv2
import numpy as np
from toolkit import *

# load image
img = cv2.imread(r'im\1.jpg')
rsz_img = cv2.resize(img, None, fx=0.25, fy=0.25)  # resize since image is huge
rsz_img=img # Block the change of resizing image
gray = cv2.cvtColor(rsz_img, cv2.COLOR_BGR2GRAY)  # convert to grayscale

# threshold to get just the signature
retval, thresh_gray = cv2.threshold(gray, thresh=130, maxval=255, type=cv2.THRESH_BINARY)


'''
0123456
...-...|...-...
total=7*7=49

'''
square = np.asarray(thresh_gray)

#square=del_isolatedot(square,0.01,0.8,1)
square=del_isolatedot(square, 0.005, 0.7, 0.8)

bytearray_toimg(square)
