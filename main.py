import file_p, image_p
from toolkit import errorProcess

debug=False
image_p.dc=False

if debug:
    fileDir=''
    newFileDir=''
    copyError=False
else:
    # 用户输入
    fileDir=input("File path(origin):")
    newFileDir=input("File path(output):")  # 处理完成存放的文件夹，空表示存放在源文件目录内的output文件夹
    copyError=True if input('Copy the original image when a error occured?(Y/N)').lower()=='y' else False

print('=============')
# 默认参数列表
fileDir=r'C:\Users\Administrator\Desktop\m' if fileDir=='' else fileDir   # 待处理的图片所在的文件夹
errorLog=errorProcess(debug)


# 读取文件列表，不读取子目录
try:
    files=[]
    root, files=file_p.fileDirList(fileDir)
    newPath=file_p.newFilePath(root, newFileDir, 'output')
    if copyError:errorPath=file_p.newFilePath(root, '', 'error')
except Exception as e:
    errorLog.add_show(1, fileDir, e)
    print('Exiting...')
    exit(errorLog.error_code())

print('Processing...('+str(len(files))+')')

for file in files:
    filePath=root + '\\' + file
    try:
        newFilePath=file_p.reconstrut_filename(filePath,newPath)
    except Exception as e:
        errorLog.add_show(2,file,e)
        continue

    try:
        dst= image_p.loadImgUnicode(filePath)
    except Exception as e:
        errorLog.add_show(3,file,e)
        continue
    try:
        angle=file_p.getExifOrientation(filePath)
        if angle!=0:
            dst= image_p.rotateProperly(dst, angle)
    except Exception as e:
        errorLog.add_show(4,file,e)
        continue
    try:
        dst= image_p.stretchProperly(dst)
    except Exception as e:
        errorLog.add_show(5,file,e)
        continue
    try:
        dst= image_p.threshProperly(dst)
    except Exception as e:
        errorLog.add_show(6,file,e)
        continue

    try:
        image_p.writeImg(newFilePath, dst)
    except Exception as e:
        errorLog.add_show(7,file,e)
        continue
    del dst

if copyError:
    file_p.copyFiles(root, errorPath, errorLog.error_file_list())

print('===============')
if not errorLog.is_empty():
    errorLog.show_all_type()
    print("Error/Total:"+str(errorLog.errorTotalCount)+'/'+str(len(files)))
else:
    print('Done!')

exit(errorLog.error_code())