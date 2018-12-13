import file_p, image_p
from toolkit import errorProcess

# 用户输入
fileDir=input("File path(origin):")
newFileDir=input("File path(output):")  # 处理完成存放的文件夹，空表示存放在源文件目录内的output文件夹
copyError=True if input('Copy the original image when a error occured?(Y/N)').lower()=='y' else False

print('=============')
# 默认参数列表
fileDir=r'C:\Users\Administrator\Desktop\m' if fileDir=='' else fileDir   # 待处理的图片所在的文件夹

# 读取文件列表，不读取子目录
files=[]
root, files=file_p.fileDirList(fileDir)
newPath=file_p.newFilePath(root, newFileDir, 'output')
errorPath=file_p.newFilePath(root, '', 'error')
print('Processing...('+str(len(files))+')')

errorLog=errorProcess()
for file in files:
    filePath=root + '\\' + file
    try:
        newFilePath=file_p.reconstrut_filename(filePath,newPath)
    except Exception as e:
        errorLog.add(1,file,e)
        errorLog.show_last()
        continue

    try:
        dst= image_p.loadImg(filePath)
        angle=file_p.getExifOrientation(filePath)
        if angle!=0:
            dst= image_p.rotateProperly(dst, angle)
        dst= image_p.stretchProperly(dst)
        dst= image_p.threshProperly(dst)
    except IndexError as e:
        errorLog.add(2,file,e)
        errorLog.show_last()
        continue

    try:
        image_p.cv2.imwrite(newFilePath, dst)
    except Exception as e:
        errorLog.add(3,file,e)
        errorLog.show_last()
        continue

    del dst

if copyError:
    file_p.copyFiles(root, errorPath, errorLog.error_file_list())

if not errorLog.is_empty():
    print('===============')
    errorLog.show_all_type()
    print("Error/Total:"+str(errorLog.errorTotalCount)+'/'+str(len(files)))
