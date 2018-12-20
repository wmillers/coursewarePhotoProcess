import exifread
import numpy as np
import os, time, shutil
from datetime import datetime

'''
    获取文件夹中的文件信息，并依次传递入
    图片传递单元，并提供文件格式、拍摄日期
    （创建日期）、文件名等内容以供生成处理
    后的文件。
'''



def findEndSlash(s):
    if s=='':return 0
    for i in range(1,len(s)+1):
        if s[-i]!='\\':
            break
    if s[0]=='\\' and i==len(s):return i
    return int(i-1)


def delEndSlash(s):
    i=findEndSlash(s)
    if i==0:
        return s
    else:
        return s[:-i]


def getExifTime(pathname, FIELD = 'EXIF DateTimeOriginal'):
    fd = open(pathname, 'rb')
    tags = exifread.process_file(fd)
    fd.close()

    if FIELD in tags:
        time_name = str(tags[FIELD]).replace(':', '').replace(' ', '_').split(".")[0]
        return True, time_name
    else:
        return False, ""


def getExifOrientation(pathname, FIELD = 'Image Orientation'):
    fd = open(pathname, 'rb')
    tags = exifread.process_file(fd)
    fd.close()
    if FIELD in tags:
        a=tags[FIELD].values[0]
        if a in [3,6,8]:
            return [180,90,270][[3,6,8].index(a)]
    return 0



def TimeStampToTime(timestamp, asfilename=False):
    # 把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
    timeStruct = time.localtime(timestamp)
    s=time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)
    if asfilename:
        return s.replace('-','').replace(' ','_').replace(':','')
    else:
        return s


def get_FileCreateTime(filePath, asfilename=False):
    # 获取文件的创建时间
    filePath = str(filePath)
    t = os.path.getctime(filePath)
    return TimeStampToTime(t, asfilename)


def reconstrut_filename(filePath, newPath='', withPath=True):
    '''
    Due to the way Windows and Linux contruct the path differently,
    this function only works on Windows(r"C:\1\1",r"\root\1").

    1) call getExifTime()
    2) if 1 returns False: call get_FileCreateTime()->TimeStampToTime()
    3) collect first part(p2) name based on 1/2
    4) splice the p2 with pathname(p1) and original file name(p3)
    5) if name is duplicated, add a number(0-9) to the symbol position
       ==> p1\p2_(symbol:e for exif, p for replaced-by-timestamp)_p3
        eg.im\19700101_000000_e0_test.jpg
    6) rename old file with new name
    '''

    exif_valid, fname_p2= getExifTime(filePath)
    if not exif_valid:fname_p2= get_FileCreateTime(filePath, asfilename=True)

    if newPath=='':pname_p1 = os.path.split(filePath)[0]
    else:pname_p1=newPath
    pname_p1=delEndSlash(pname_p1)
    oname_p3 = os.path.split(filePath)[1]
    if exif_valid:symbol_code='e'
    else:symbol_code='p'
    duplicated=0
    while duplicated<=9:
        new_name= pname_p1 + '\\' +fname_p2+'_'+symbol_code+str(duplicated)+'_'+oname_p3
        if not os.path.exists(new_name):break
        duplicated+=1
    if duplicated>9:raise FileExistsError
    if withPath:
        return new_name
    else:
        return (fname_p2+'_'+symbol_code+str(duplicated)+'_'+oname_p3)



def decontruct_filename(file):
    if len(file.split('_')) > 3:
        return '_'.join(file.split('_')[3:])
    else:
        return file



def deconstruct_dirfile_rename(fileDir):
    root, files=fileDirList(fileDir)
    for file in files:
        if len(file.split('_'))>3:
            deconstruct_file=decontruct_filename(file)
            os.rename(root+'\\'+file, root+'\\'+deconstruct_file)


def fileDirList(fileDir):
    for root, dirs, files in os.walk(fileDir):break
    root=delEndSlash(root)
    return root, files


def newFilePath(root, newPath='', relaPath='output'):
    root=delEndSlash(root)
    if newPath=='':
        newPath=root+'\\'+relaPath+'\\'
    elif not os.path.isabs(newPath):raise Exception("You should use absolute path, not '"+newPath+"'")
    if not os.path.exists(newPath):os.makedirs(newPath)
    return delEndSlash(newPath)


def copyFiles(root, newPath, fileList):
    root=delEndSlash(root)+'\\'
    newPath=delEndSlash(newPath)+'\\'
    for file in fileList:
        shutil.copy(root+file,newPath+file)


class course_time(object):
    course_list = [{'name': '信息论',
                    'week': [1],
                    'time': [[1, 2]]},
                   {'name': '自动化',
                    'week': [4, 5],
                    'time': [[1, 2], [3, 4]]},
                   {'name': '通信',
                    'week': [2],
                    'time': [[1, 2]]},
                   {'name': '轨道',
                    'week': [3],
                    'time': [[1, 2, 3, 5, 6]]}]

    ctime_start = np.array([[8, 30], [9, 25], [10, 20], [11, 15],
                            [13, 30], [14, 25], [15, 20], [16, 15]])
    __ctime_h = ctime_start[:, 0].tolist()
    __ctime_m = ctime_start[:, 1].tolist()
    ctime_h_min=min(__ctime_h)
    ctime_h_max=max(__ctime_h)+1

    Undefined='Unknown'
    course_filename={x['name']:[] for x in course_list}
    course_filename[Undefined]=[]

    def __init__(self, fileOldPath, relaNewPath='output', files=[]):
        self.fileOldPath=delEndSlash(fileOldPath)
        self.newPath=delEndSlash(relaNewPath)
        if files==[]:
            self.files = fileDirList(self.fileOldPath)[1]
            self.filenameChanged=True
        else:
            self.files=files
            #self.oldFiles=fileDirList(self.fileOldPath)[1]
            self.filenameChanged=False
        pass

    def timeFileName_read(self, filename):
        autofill = 100
        fileTime = {'week': autofill,
                    'hour': autofill,
                    'minute': autofill,
                    'second': autofill, }
        re = filename.split('_')
        fileTime['week'] = datetime.strptime(re[0], '%Y%m%d').weekday() + 1
        fileTime['hour'] = datetime.strptime(re[1], '%H%M%S').hour
        fileTime['minute'] = datetime.strptime(re[1], '%H%M%S').minute
        fileTime['second'] = datetime.strptime(re[1], '%H%M%S').second
        return fileTime

    def course_time(self, fileTime):
        number = 0
        course_name = self.Undefined
        for course in self.course_list:
            if fileTime['week'] in course['week']:
                day = course['time'][course['week'].index(fileTime['week'])]
                if fileTime['hour'] in self.__ctime_h:
                    if fileTime['minute'] >= self.__ctime_m[self.__ctime_h.index(fileTime['hour'])]:
                        number = self.__ctime_h.index(fileTime['hour']) + 1
                    else:
                        number = self.__ctime_h.index(fileTime['hour'])
            if number != 0:
                if number in day:
                    course_name = course['name']
                    break
        if number == 0: course_name = self.Undefined
        return course_name

    def fileNameRender(self, course_name, filename):
        filePath = self.fileOldPath + '\\' + filename
        fileNewPath = self.newPath + '\\' + course_name + '\\' + filename
        return delEndSlash(filePath), delEndSlash(fileNewPath)

    def process(self):
        for file in self.files:
            fileTime = self.timeFileName_read(file)
            course_name = self.course_time(fileTime)
            if self.filenameChanged:
                self.course_filename[course_name].append(file)
            else:
                self.course_filename[course_name].append(decontruct_filename(file))
        return self.course_filename

if __name__=='__main__':
    fileDirList("C:\\Users\\Administrator\\Desktop\\Documents\\python_work\\cours_image\\im")