import cv2
import numpy as np
from toolkit import *
from scipy import ndimage

dc=True  # Debug Code
print("Debug Code:",dc)

'''
With the help of the documents on https://docs.opencv.org
therefore I can finish the project.And also thanks the help
from stackoverflow.com for solving some of the problems.
'''


'''
Part 1

1) 对ppt区域进行识别、还原原文变形
'''



# load image
img = cv2.imread(r'im\t7.png')
rsz_img = cv_resize(img,756)  # resize since image is huge
#rsz_img=img # Block the change of resizing image
gray = cv2.cvtColor(rsz_img, cv2.COLOR_BGR2GRAY)  # convert to grayscale

# threshold to get just the signature
retval, thresh_gray = cv2.threshold(gray, thresh=130, maxval=255, type=cv2.THRESH_BINARY)

im2, contours, hierarchy = cv2.findContours(thresh_gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

# 寻找面积最大的区域
max_contour= max(contours, key= cv2.contourArea)

# 绘制近似四边形
# 不能使用minAreaRect，其返回值是最小面积的矩形，
# 与要求的四边形不符
# cv2.drawContours(rsz_img, cv_BoxPoints(cv2.minAreaRect(max_contour)), -1, (0,255,0), 2)
approx_points=cv2.approxPolyDP(max_contour,0.1 * cv2.arcLength(max_contour, True),True)


if dc:prints(approx_points, np.asarray(corner_points(approx_points)))
# 计算拉伸后的矩形定位点并图形变换
M= cv2.getPerspectiveTransform(np.asarray(approx_points, np.float32),
                               np.asarray(corner_points(approx_points), np.float32))
dst= cv2.warpPerspective(rsz_img, M, (corner_points(approx_points)[2][0][0], corner_points(approx_points)[1][0][1]))

if dc:plt_show(rsz_img, dst)


'''
Part 2

2) 对指定区域（尽量保持纯色背景）的内容清晰化、二值化处理
   并对其中带图形的区域尽最大可能保留信息量
'''