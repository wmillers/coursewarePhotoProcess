from matplotlib import pyplot as plt
from PIL.Image import frombytes
import cv2
import numpy as np

'''
    Toolkit for image process
    with the method from cv2,plt,np
    个人工具包，对一些需要调用多次函数的
    过程打包，主要用于图像的处理和输出，
    使用的库为cv2,matplotlib,PIL,numpy
'''

class errorProcess(object):
    def __init__(self):
        # 动态生成错误类型统计表
        self.errorType = ['NONE', 'FILE', 'IMAGE', 'WRITE']
        self.errorCount = [0 for x in range(0, len(self.errorType))]
        # 形成一个由列表组成的有序字典
        self.__errorInfoName = ['tag', 'file', 'info']
        self.__errorLastInfoValue = [self.errorType[0], '', '']
        self.errorInfo = []
        self.errorTotalCount = 0

    def index(self, name):
        return self.__errorInfoName.index(name)

    def add(self, tagindex, file, info):
        if tagindex not in range(0,len(self.errorType)):
            tagindex=0
        self.__errorLastInfoValue[self.index('tag')] =self.errorType[tagindex]
        self.__errorLastInfoValue[self.index('file')]=file
        self.__errorLastInfoValue[self.index('info')]=info
        self.errorInfo.append(self.__errorLastInfoValue[:])
        self.errorCount[tagindex]+=1
        self.errorTotalCount+=1

    def last_index(self):
        return self.errorTotalCount-1

    def show(self, index):
        print('[ERROR][%03d:%2d:%5s][Where]%s:[At]%s' %
              (index + 1,
               self.errorType.index(self.errorInfo[index][self.index('tag')]),
               self.errorInfo[index][self.index('tag')],
               self.errorInfo[index][self.index('file')],
               repr(self.errorInfo[index][self.index('info')])))

    def show_all(self):
        for i in range(0,self.last_index()+1):
            self.show(i)

    def show_last(self):
        self.show(self.last_index())

    def show_all_type(self):
        for i in range(0, self.errorTotalCount):
            if self.errorCount[i] != 0:
                print(self.errorType[i] + ' error:' + str(self.errorCount[i]))

    def is_empty(self):
        if self.errorTotalCount==0:
            return True
        else:
            return False

    def error_file_list(self):
        errorFileList=[]
        for i in range(0, self.last_index() + 1):
            errorFileList.append(self.errorInfo[i][self.index('file')])
        return errorFileList


cv_series= 0

def cv_show(*from_imgs, name="'L': next, 'A': back, 'E': exit"):
    """ Basic usage:cv_show(cv2_img),
        show a image with default name "Unnamed".
    """
    global cv_series
    cv_series+= 1
    i= 0
    while True:
        if(len(from_imgs)>1):
            cv2.imshow(name + " - " + str(i) + " - " +str(cv_series), from_imgs[i])
        else:
            cv2.imshow("Press 'E' to exit" + " - " +str(cv_series), from_imgs[i])
        if cv2.waitKey(0) == ord('l'):
            i+= 1
            cv2.destroyAllWindows()
        elif cv2.waitKey(0) == ord('a'):
            i-= 1
            cv2.destroyAllWindows()
        elif cv2.waitKey(0) == ord('e'):
            cv2.destroyAllWindows()
            break
        if i>=len(from_imgs):i=0
        elif i<0:i=len(from_imgs)-1


def cv_resize(from_img,max=800):
    """ Basic usage:cv_show(cv2_img),
        the maximum height/width of the image is limited to 800px
        if only has one argument.
    """
    if from_img.shape[0] <= max and from_img.shape[1] <= max:return 1, from_img
    ratio=max/from_img.shape[0] if from_img.shape[0]>from_img.shape[1] else max/from_img.shape[1]
    return ratio, cv2.resize(from_img, None, fx=ratio, fy=ratio)  # resize since image is huge


def cv_BoxPoints(rect):
    """
    """
    box= cv2.boxPoints(rect)
    #box = cv2.cv.BoxPoints(rect)  # for OpenCV 2.x
    box= [np.int0(box)]
    return box


def plt_show(*from_imgs):
    """ Basic usage:plt_show(cv2_img),
        show a image with default name "Unnamed".
    """

    row_a= int(np.sqrt(len(from_imgs)))
    col_a= int(len(from_imgs)/row_a) + len(from_imgs)%row_a
    if row_a>col_a:
        ratio_a= row_a/col_a
        row_b= row_a-1
        col_b= int(len(from_imgs)/row_b) + len(from_imgs)%row_b
        ratio_b= row_b/col_b if row_b>col_b else col_b/row_b
    elif row_a<col_a:
        ratio_a= col_a/row_a
        col_b= col_a-1
        row_b= int(len(from_imgs)/col_b) + len(from_imgs)%col_b
        ratio_b= row_b/col_b if row_b>col_b else col_b/row_b
    else:
        row_b, col_b=row_a, col_a
        ratio_a=ratio_b=1
    row= row_a if ratio_a<ratio_b else row_b
    col= col_a if ratio_a<ratio_b else col_b

    plt_series = 0
    for from_img in from_imgs:
        plt_series+= 1
        plt.subplot(row,col,plt_series)
        plt.title(str(plt_series))
        plt.imshow(from_img)
        #plt.axis('off')
        #plt.tight_layout()
    plt.show()


def plt_dotshow(dots):
    xx=[x for x in range(0,len(dots))]
    plt.plot(xx,dots)
    plt.grid()
    plt.show()



def bytearray_toimg(*datas,show=1):
    """ Basic usage:bytearray_toimg(np_array),
        convert a numpy array to image and show it
        if the last argument is set to 1 by default or by user.
        This function accept multiple arrays, show
        all of them or return the first one converted.
    """
    if show==1:
        for data in datas:
            frombytes(mode='1', size=data.shape[::-1], data=np.packbits(data, axis=1)).show()
    else:
        for data in datas:
            return frombytes(mode='1',size=data.shape[::-1],data=np.packbits(data,axis=1))


def del_isolatedot(square,nearby_ratio = 1/1000,white_ratio = 0.7,colour_ratio=1):
    """ Basic usage:del_isolatedot(cv2_img),
        find isolated black dots surrounded by white dots
        and fill this area with white,
        notice that cv2_img should be gray
        and both three ratios should be positive integer
        which is less than or equal to 1.

        USELESS BY NOW, but the experience learnt from here is useful.
    """
    square=np.copy(square)
    # black = 0
    white = 255
    nearby = int(max(min(square.shape[0] * nearby_ratio, square.shape[1] * nearby_ratio), 1))
    colournearby=int(max(min(nearby*colour_ratio,nearby),1))
    # the ratio that white pixel should take
    white_value = int(white * (nearby * 2 + 1) ** 2 * white_ratio)
    i = j = 0
    for x in range(nearby, square.shape[0], colournearby * 2):
        for y in range(nearby, square.shape[1], colournearby * 2):
            i += 1
            if np.sum(square[x - nearby:x + nearby + 1, y - nearby:y + nearby + 1]) >= white_value:
                j+=1
                square[x - colournearby:x + colournearby + 1, y - colournearby:y + colournearby + 1] = white
    print(j,"/",i)
    return square



def prints(*datas):
    for data in datas:
        print(data)
        print("="*20)


def corner_points(points):
    """
    Transform a random quadrilateral to a rectangle
    Accept a four-points array generated by cv2.approxPolyDP
    and return the arranged one with same format.

    min--> 0-a-1
           d\   \b
             3-c-2 <--max
    """
    distances=[cv2.norm(points[x]) for x in range(0, 4)]
    transform_distance=[]
    points_index=[0, 1, 2, 3]
    arrange_points_index=[0]*4

    arrange_points_index[0]=distances.index(min(distances))  # find the "0" point
    arrange_points_index[2]=distances.index(max(distances))  # find the "2" point
    points_index.remove(arrange_points_index[0])
    points_index.remove(arrange_points_index[2])
    if np.absolute(points[points_index[0]][0][0]-points[distances.index(min(distances))][0][0]) > \
            np.absolute(points[points_index[1]][0][0]-points[distances.index(min(distances))][0][0]):
        # find the "1" point <-- points_index[0], "3" point <-- points_index[1]
        arrange_points_index[1]=points_index[0]
        arrange_points_index[3]=points_index[1]
    else:
        arrange_points_index[3]=points_index[0]
        arrange_points_index[1]=points_index[1]

    line_length=[cv2.norm(points[arrange_points_index[0]][0],points[arrange_points_index[1]][0]),  # 0-a-1
                cv2.norm(points[arrange_points_index[1]][0], points[arrange_points_index[2]][0]),  # 1-b-2
                cv2.norm(points[arrange_points_index[2]][0], points[arrange_points_index[3]][0]),  # 2-c-3
                cv2.norm(points[arrange_points_index[3]][0], points[arrange_points_index[0]][0])]  # 3-d-0
    test= cv2.norm(points[arrange_points_index[3]][0], points[arrange_points_index[0]][0])
    x= int(line_length[0] if line_length[0] > line_length[2] else line_length[2])
    y= int(line_length[1] if line_length[1] > line_length[3] else line_length[3])

    # original format is counterclockwise
    transform_distance.append([[0, 0]])
    transform_distance.append([[0, y]])
    transform_distance.append([[x, y]])
    transform_distance.append([[x, 0]])

    return np.array(transform_distance)

