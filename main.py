import file_p
import image_p

#参数列表
fileDir=r'C:\Users\Administrator\Desktop\Documents\python_work\cours_image\im'     # 待处理的图片所在的文件夹
newFileDir=''  # 处理完成存放的文件夹，空表示存放在源文件目录内的output文件夹
errorFlag=[]
#strictMode=False # 默认关闭，出现非关键错误时跳过当前文件，继续执行


#读取文件列表，不读取子目录
files=[]
root, files=file_p.fileDirList(fileDir)

newPath=file_p.newFilePath(root,newFileDir)

for file in files:
    filePath=root + '\\' + file
    try:
        newFilePath=file_p.reconstrut_filename(filePath,newPath)
    except Exception as e:
        errorFlag.append([1,"[error] [FILE]:[FileName] "+file,e])
        continue

    try:
        dst= image_p.stretchProperly(filePath)
        dst= image_p.threshProperly(dst)
    except Exception as e:
        errorFlag.append([2,"[error][IMAGE]:[FileName] "+file,e])
        continue

    try:
        image_p.cv2.imwrite(newFilePath, dst)
    except Exception as e:
        errorFlag.append([3,"[error][WRITE]:[FileName] "+file,e])
        continue

if errorFlag!=[]:
    print('===============')
    for i in range(0,len(errorFlag)):
        print(errorFlag[i][1]+' [Message]'+repr(errorFlag[i][2]))
    print("Error Count:"+str(len(errorFlag)))
