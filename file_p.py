import exifread
import os, time, shutil

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


def reconstrut_filename(filePath, newPath=''):
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
    return new_name



def fileDirList(fileDir):
    for root, dirs, files in os.walk(fileDir):break
    root=delEndSlash(root)
    return root, files


def newFilePath(root, newPath='', relaPath='output'):
    root=delEndSlash(root)
    if newPath=='':
        newPath=root+'\\'+relaPath+'\\'
    elif not os.path.isabs(newPath):raise Exception("You should use absolute path, not '"+newPath+"'")
    if not os.path.exists(newPath):os.mkdir(newPath)
    return newPath


def copyFiles(root, newPath, fileList):
    root=delEndSlash(root)+'\\'
    newPath=delEndSlash(newPath)+'\\'
    for file in fileList:
        shutil.copy(root+file,newPath+file)



if __name__=='__main__':
    fileDirList("C:\\Users\\Administrator\\Desktop\\Documents\\python_work\\cours_image\\im")