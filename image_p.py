import cv2
import numpy as np
from toolkit import *
from scipy import ndimage
from file_p import *

dc=True  # Debug Code
# dc=False
if __name__=='__main__':print("Debug Code:",dc)

'''
With the help of the documents on https://docs.opencv.org
therefore I can finish the project.And also thanks the help
from stackoverflow.com for solving some of the problems.
'''


'''
Part 1

1) 对ppt区域进行识别、还原原文变形
'''

def stretchProperly(img_name=r'im\1.jpg', max_size=1200):

    # load image
    img = cv2.imread(img_name)
    img_ratio, rsz_img = cv_resize(img,max_size)  # resize since image is huge
    #rsz_img=img # Block the change of resizing image
    gray = cv2.cvtColor(rsz_img, cv2.COLOR_BGR2GRAY)  # convert to grayscale

    # threshold to get just the signature
    retval, thresh_gray = cv2.threshold(gray, thresh=140, maxval=255, type=cv2.THRESH_BINARY)

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
    dst= cv2.warpPerspective(rsz_img, M,
                                   (corner_points(approx_points)[2][0][0],
                                    corner_points(approx_points)[1][0][1]))

    if dc:plt_show(rsz_img, dst)
    return dst

'''
Part 2

2) 对指定区域（尽量保持纯色背景）的内容清晰化、二值化处理
   并对其中带图形的区域尽最大可能保留信息量
'''
def bestTheshFinder(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    if dc:
        thresh_gray=[]
        j=0
        for i in range(130,210,10):
            j+=1
            retval, temp = cv2.threshold(gray, thresh=i, maxval=255, type=cv2.THRESH_BINARY)
            thresh_gray.append(temp)
        plt_show(*thresh_gray)





'''
Notice that we don't need to get original-sized image,
what we need at last is a image print-friendly, which
means printable colour, fidelity and a proper size. 

Ideal thresh is 150~190
'''
def removeNoiseImg(img):
    if dc:print(print("Placeholder"))
    return img

'''
Part 3

3) 文件处理模块，遍历指定根目录，并将文件经过p1、p2处理，
   保存至指定文件夹（默认根目录下的output文件夹）
'''
def dirImageProcess(fileDir, newPath=''):
    error_list=[]
    for root, dirs, files in os.walk(fileDir):break
    root=delEndSlash(root)
    if newPath=='':
        newPath=root+'\\'+'output'+'\\'
        if not os.path.exists(newPath):os.mkdir(newPath)
    for file in files:
        try:
            dst= stretchProperly(root + '\\' + file)
            dst= removeNoiseImg(dst)
            cv2.imwrite(newPath+file, dst)
        except:
            error_list.append(file)
            continue

    if error_list!=[]:
        print("ERROR while processing the files.")
        print("fileDir="+fileDir)
        print("newPath="+newPath)
        print("fileName:")
        for i in error_list:
            print(i)
        return False
    else:
        return True



# Test area

if __name__=='__main__':
    dst_sp= stretchProperly(r'C:\Users\Administrator\Desktop\Documents\python_work\cours_image\im\1.jpg')
    print(dst_sp)