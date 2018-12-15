import cv2
import numpy as np
from toolkit import *

dc=True  # Debug Code
dc=False
if __name__=='__main__':print("Debug Code:",dc)

'''
With the help of the documents on https://docs.opencv.org
therefore I can finish the project.And also thanks the help
from stackoverflow.com for solving some of the problems.
'''

def loadImgUnicode(img_name=r'im\1.jpg'):
    '''
    Default
    '''
    if dc:print(type(img_name))
    stream = open(img_name, "rb")
    bytes = bytearray(stream.read())
    nparray = np.asarray(bytes, dtype=np.uint8)
    return cv2.imdecode(nparray, cv2.IMREAD_UNCHANGED)

def loadImgCompatible(img_name=r'im\1.jpg'):
    '''
    Not support whitespaces and unicode characters
    in file name, but it is much more compatible.
    '''
    return cv2.imread(img_name)

def writeImg(file_path, dst):
    '''
    解决了opencv2处理文件名unicode的问题
    但是路径还是不能带空格和unicode
    '''
    file_path=file_path.encode('ascii', 'ignore').decode('ascii')
    if not cv2.imwrite(file_path, dst):raise UnicodeTranslateError


'''旋转图片，（暂时）仅支持90度的倍数旋转'''
def rotateProperly(img, angle=0):
    return np.rot90(img, -int(angle/90))


'''
对ppt区域进行识别、还原原文变形
'''
def stretchProperly(img, max_size=800):
    img_ratio, rsz_img = cv_resize(img,max_size)  # resize since image is huge
    #rsz_img=img # Block the change of resizing image
    loop_count=0
    while True:
        if loop_count==0:
            gray = cv2.cvtColor(rsz_img, cv2.COLOR_BGR2GRAY)  # convert to grayscale
        else:
            gray= 255-gray

        # threshold
        retval, thresh_gray = cv2.threshold(gray, thresh=140, maxval=255, type=cv2.THRESH_BINARY)

        im2, contours, hierarchy = cv2.findContours(thresh_gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        # 寻找面积最大的区域
        max_contour= max(contours, key=lambda x:abs(cv2.contourArea(x)))
        # 发现黑板区，尝试反色识别
        if abs(cv2.contourArea(max_contour))>=(len(gray)*0.6)**2:
            loop_count+=1
        if loop_count>=1: break
        loop_count+=1
    # 黑板区并且有与黑板直接连接的深色物体导致识别异常
    assert abs(cv2.contourArea(max_contour)) < (len(gray)*0.9)**2,\
        'Unable to deal with this image which may contain dark boards.'

    # 绘制近似四边形
    # 不能使用minAreaRect，其返回值是最小面积的矩形，
    # 与要求的四边形不符
    approx_points=cv2.approxPolyDP(max_contour,0.1 * cv2.arcLength(max_contour, True),True)
    # 但是有时候这里只会包含一个点，或者多于四个点，因此前者只能用矩形解决
    if len(approx_points)<4:approx_points=cv_BoxPoints(cv2.minAreaRect(max_contour))

    if dc:
        con_img=np.copy(rsz_img)
        cv2.drawContours(con_img, contours, -1, (0,255,255), 3)
        cv2.drawContours(con_img, cv_BoxPoints(cv2.minAreaRect(max_contour)), -1, (0,255,0), 2)
        # cv2.drawContours(con_img, approx_points, -1, (255,0,0), 1)
        cv_show(con_img)
        del con_img
    # 计算拉伸后的矩形定位点并图形变换
    stretched_points=stretch_points(approx_points)
    M= cv2.getPerspectiveTransform(np.asarray(rearrange_points(approx_points), np.float32),
                                   np.asarray(stretched_points, np.float32))
    dst= cv2.warpPerspective(rsz_img, M,
                             (stretched_points[2][0][0],
                              stretched_points[1][0][1]))

    if dc:plt_show(rsz_img, dst)
    return dst



'''
对指定区域（尽量保持纯色背景）的内容清晰化、二值化处理
并对其中带图形的区域尽最大可能保留信息量
'''
def threshProperly(img, limit=0.1, area=2):
    '''
    If corners of the image that was after thresh_gray-ed
    is too dark, the best solution is to reduce the thresh level.
    '''
    #default (also recommended) one is 1/4
    area=1/(area+2)
    img_x, img_y=img.shape[0], img.shape[1]

    # black = 0
    white = 255
    length_x=int(area*img_x)
    length_y=int(area*img_y)
    #图形说明见f2.png
    #mx^2+ny^2=1
    #numpy解二元一次方程
    known_pos=[[img_x, img_y - length_y],   # 相邻的两个交点
               [img_x - length_x, img_y]]
    m, n=np.linalg.solve([[known_pos[0][0]**2, known_pos[0][1]**2],
                          [known_pos[1][0]**2, known_pos[1][1]**2]],
                         [1,1])*5
    #通过同时平移椭圆和矩形，使得矩形的左下端位于(0,0)得到的
    #函数计算得到椭圆区域，并反转取值，得到黑色遮罩区域
    #但是注意遮罩True表示区域
    outside_ellipse=np.fromfunction(lambda x,y :m*(x-img_x/2)**2+n*(y-img_y/2)**2<=1,
                                    [img_x, img_y])
    #prints(img_x,img_y,m,n,outside_ellipse)

    #不同过滤值下的图片
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    thresh_gray=[]
    corner_area=[]
    corner_mean=[]
    j=0
    #150~190
    for i in list(range(130,190,10))+list(range(190,230,5)):
        retval, temp = cv2.threshold(gray, thresh=i, maxval=white, type=cv2.THRESH_BINARY)
        thresh_gray.append(temp)
        corner_area.append(np.ma.array(thresh_gray[j],mask=outside_ellipse))
        corner_mean.append(corner_area[j].mean()/white)
        if(j>0 and corner_mean[j]<=0.5 and corner_mean[j-1]>0.5):
            del corner_area[j]
            del corner_mean[j]
            break
        j+=1
    if dc:plt_show(*thresh_gray[-4:])
    corner_mean=np.array(corner_mean)
    corner_baseline=corner_mean.max()-(corner_mean.max()-corner_mean.min())*limit
    corner_baseline=0.85 if corner_baseline>0.85 else corner_baseline    #尽量保持最多的信息量
    for i in range(0,len(corner_mean)):
        if(corner_mean[i]<corner_baseline):
            if(i>0):
                i-=1
            break
    '''
    corner_mean_k=[corner_mean[k]>=corner_baseline for k in range(0,len(corner_mean))]
    plt_dotshow(corner_mean)
    print(corner_mean_k)
    cv_show(*corner_area)'''
    return thresh_gray[i]


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
文件处理模块，遍历指定根目录，并将文件经过p1、p2处理，
保存至指定文件夹（默认根目录下的output文件夹）
'''



# Test area

if __name__=='__main__':
    dst_sp= stretchProperly(r'C:\Users\Administrator\Desktop\Documents\python_work\cours_image\im\1.jpg')
    print(dst_sp)