import cv2
import numpy as np

# load image
img = cv2.imread(r'im\1.jpg')
rsz_img = cv2.resize(img, None, fx=0.25, fy=0.25) # resize since image is huge
gray = cv2.cvtColor(rsz_img, cv2.COLOR_BGR2GRAY) # convert to grayscale

# threshold to get just the signature
retval, thresh_gray = cv2.threshold(gray, thresh=100, maxval=255, type=cv2.THRESH_BINARY)

# find where the signature is and make a cropped region
points = np.argwhere(thresh_gray==0) # find where the black pixels are
points = np.fliplr(points) # store them in x,y coordinates instead of row,col indices
x, y, w, h = cv2.boundingRect(points) # create a rectangle around those points
x, y, w, h = x-10, y-10, w+20, h+20 # make the box a little bigger
crop = gray[y:y+h, x:x+w] # create a cropped region of the gray image

# get the thresholded crop
retval, thresh_crop = cv2.threshold(crop, thresh=200, maxval=255, type=cv2.THRESH_BINARY)

# display
cv2.imshow("Cropped and thresholded image", thresh_crop) 
cv2.waitKey(0)



#cv2.fillPoly(rsz_img, max_contour,1)
# Output


# 去除噪声
#square = ndimage.binary_erosion(square,iterations=3) #腐蚀
#square = ndimage.gaussian_filter1d(square,sigma=5)
#square = ndimage.binary_dilation(square,iterations=2)
#reconstruction = ndimage.binary_propagation(eroded_square, mask=square)
#square=np.asmatrix(1*square)

'''
# find where the signature is and make a cropped region
points = np.argwhere(thresh_gray==0) # find where the black pixels are
points = np.fliplr(points) # store them in x,y coordinates instead of row,col indices
x, y, w, h = cv2.boundingRect(points) # create a rectangle around those points
x, y, w, h = x-10, y-10, w+20, h+20 # make the box a little bigger
crop = gray[y:y+h, x:x+w] # create a cropped region of the gray image

# get the thresholded crop
retval, thresh_crop = cv2.threshold(crop, thresh=200, maxval=255, type=cv2.THRESH_BINARY)
cv_show(thresh_crop)
'''
'''

# Hough变换求线段
using=edges
lines = cv2.HoughLines(using,1,np.pi/180,200)
#print(lines)
i=0
for line in lines:
    i+=1
    #if ( i%20!=0):continue
    if ( i>1550 ):break
    for rho,theta in line:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        print(rho,theta)
        cv2.line(using,(x1,y1),(x2,y2),(100,200,100),2)
cv2.imshow("Cropped and thresholded image", using)
cv2.waitKey(0)



# Canny求边界
edges = cv2.Canny(thresh_gray, 50, 150, apertureSize=3)


# display
cv2.imshow("Cropped and thresholded image", thresh_gray)
cv2.waitKey(0)

'''


