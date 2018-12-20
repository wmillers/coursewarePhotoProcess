import file_p, image_p
from toolkit import errorProcess, count_show

'''
大致轮廓（主要涉及外部处理流程）

首先，循环调用course_time_classify将文件夹里的所有文件按照reconstrut_filename
重命名后的文件名记录入该目录下的课程子目录列表中（无法分类的放入特殊子目录）。其次，
通过前面获得的课程子目录列表，分目录列表拼接源文件路径循环调用图像处理oldPath。注意，
传入的oldPath=源文件,NewPath=源文件根目录+output+课程名+源文件名字。最后保存文件前，
根据生成的课程子目录列表生成文件夹，将dst图像存入NewPath，同时，即屏幕输出显示为：
用户输入||处理过程中的error||产生error的文件名||总结。因此整个过程中仅有copy操作，
无move操作，共两次循环（生成课程目录列表、根据列表处理文件）。有一个情况暂时无法处理，
如果ppt上包含的颜色与背景有很大的深浅度差别，识别出的结果质量基本不高，且无法人工检测。
'''
#TODO(LONGTERM):算法改进，例如自动侦测高亮度区域（ppt左上方日光灯导致的），动态生成过滤阈值，
#TODO(LONGTERM):对常见ppt背景颜色样本存储，防止将内嵌图片计算入模型，造成结果产生大的偏差
debug=False
#image_p.dc=True
hard_count=0

if debug:
    fileDir=''
    newFileDir=''
    showErrorFile=True
    moveDoneFiles=True
else:
    # 用户输入
    # 图片所在目录
    fileDir=input("File path(origin):")
    # 处理完成存放的文件夹，空表示存放在源文件目录内的output文件夹
    newFileDir=input("File path(output):")
    # 是否要将处理失败的文件复制到指定的文件夹（/output/error/）
    showErrorFile=True if input('Show the file name list when an error occured?(Y/N)').lower()=='y' else False
    # 通常情况下可能会因为处理的区域比周围暗（如墙面）导致错误地识别了墙面
    # 将已分类的文件移动到已完成
    moveDoneFiles=True if input('Move files when done?(Y/N)').lower()=='y' else False
if debug:print('--Debug on--')
print('=============')
# 默认参数列表
fileDir=r'C:\Users\Administrator\Desktop\m' if fileDir=='' else fileDir   # 待处理的图片所在的文件夹
errorLog=errorProcess(debug)
file_count=count_show()


# 读取文件列表，不读取子目录
try:
    files_done=[]
    files=[]
    root, files=file_p.fileDirList(fileDir)
    lastName={}
    compatibleList={}

    for file in files:
        filePath=root + '\\' + file
        try:
            lastName[file]=file_p.reconstrut_filename(filePath,'',withPath=False)
        except Exception as e:
            errorLog.add_show(2,file,e)
            continue

    cour_list=file_p.course_time(root, 'output', lastName.values())
    cour_list.process()
    compatible=True
    print('Processing...('+str(len(files))+')')

    i=0
    for key in cour_list.course_filename.keys():
        i+=1
        if key!=cour_list.Undefined:
            if compatible:
                compatibleList['%03d' % i]=key
                new_key='%03d' % i
            else:
                new_key=key
            for value in cour_list.course_filename[key]:
                filePath=cour_list.fileNameRender('', value)[0]
                newRelaPath=cour_list.fileNameRender(new_key,'')[1]
                newFilePath=file_p.newFilePath(root, '', newRelaPath)+'\\'+lastName[value]
                try:
                    img= image_p.loadImgUnicode(filePath)
                except Exception as e:
                    errorLog.add_show(3,value,e)
                    continue
                try:
                    angle=file_p.getExifOrientation(filePath)
                    if angle!=0:
                        dst= image_p.rotateProperly(img, angle)
                    else:
                        dst=img
                except Exception as e:
                    errorLog.add_show(4,value,e)
                    continue
                try:
                    dst, hard_to_recognize= image_p.stretchProperly(dst)
                except AssertionError as e:
                    if str(e)!='Unable to recognize the valid area, size of the result is too small.':
                        errorLog.add_show(5,value,e)
                    else:
                        errorLog.add_show(5,value,e)
                    continue
                except Exception as e:
                    errorLog.add_show(5,value,e)
                    continue
                try:
                    hard_to_recognize=True
                    if hard_to_recognize:
                        hard_count+=1
                        dst= image_p.threshBackground(dst)
                    else:
                        dst= image_p.threshProperly(dst)
                except Exception as e:
                    errorLog.add_show(6,value,e)
                    continue

                try:
                    image_p.writeImg(newFilePath, dst)
                    files_done.append(value)
                except Exception as e:
                    errorLog.add_show(7,file,e)
                    continue
                del dst
                file_count.add_show()

except Exception as e:
    errorLog.add_show(1, fileDir, e)
    errorLog.error_exit()


if compatible:
    for akey, avalue in compatibleList.items():
        try:
            ascii_path=file_p.delEndSlash(root) + '\\' + cour_list.fileNameRender(akey, '')[1]+ '\\'
            unicode_path=file_p.delEndSlash(root) + '\\' + cour_list.fileNameRender(avalue, '')[1]+ '\\'
            if not file_p.os.path.exists(ascii_path):continue
            file_p.os.rename(ascii_path, unicode_path)
        except Exception as e:
            errorLog.add_show(8, fileDir, e)
            continue

if moveDoneFiles:
    moved_path=file_p.newFilePath(root, '', 'done')
    for file in files_done:
        try:
            file_old_path=cour_list.fileNameRender('', file)[0]
            file_p.shutil.move(file_old_path, moved_path+'\\'+file)
        except Exception as e:
            errorLog.add_show(8, fileDir, e)
            continue

print('===============')
if not errorLog.is_empty():
    if showErrorFile:
        errorLog.show_error_file_list()
        print('===============')
    errorLog.show_all_type()
    print("Error/Total:"+str(errorLog.errorTotalCount)+'/'+str(len(files)))
else:
    print('Done!')
print(hard_count)
exit(errorLog.error_code())