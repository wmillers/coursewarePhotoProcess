import file_p, image_p
from toolkit import errorProcess,plt_show,cv_show

'''
快速测试单张图片
'''
error=errorProcess(True)
filePath='C:\\Users\\Administrator\\Desktop\\m\\12.jpg'
file=filePath
dst=[]
#image_p.dc=True
# file_p.getExifOrientation()

try:
    img = image_p.loadImgUnicode(filePath)
    angle = file_p.getExifOrientation(filePath)
    if angle != 0:
        dst.append(image_p.rotateProperly(img, angle))
    else:
        dst.append(img)
    #image_p.colourRange(img)
    dst.append([])
    dst[len(dst) - 1], hard_to_recognize=image_p.stretchProperly(dst[len(dst)-2])
    hard_to_recognize=True
    if hard_to_recognize:
        dst.append(image_p.threshBackground(dst[len(dst)-1]))
    else:
        dst.append(image_p.threshProperly(dst[len(dst)-1]))
except Exception as e:
    error.add_show(0,filePath,e)
# image_p.writeImg('C:\\Users\\Administrator\\Desktop\\OutPUTa.jpg',dst2)
plt_show(img,*dst)
cv_show(dst[len(dst)-1])
pass