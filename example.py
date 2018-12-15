import file_p, image_p
from toolkit import errorProcess,plt_show,cv_show

'''
快速测试单张图片
'''
filePath='C:\\Users\\Administrator\\Desktop\\m\\5.jpg'
file=filePath
#image_p.dc=True
# file_p.getExifOrientation()


img = image_p.loadImgUnicode(filePath)

angle = file_p.getExifOrientation(filePath)
if angle != 0:
    dst = image_p.rotateProperly(img, angle)
else:
    dst=img
dst1 = image_p.stretchProperly(dst)
dst2 = image_p.threshProperly(dst1)
# image_p.writeImg('C:\\Users\\Administrator\\Desktop\\OutPUTa.jpg',dst2)
plt_show(img,dst,dst1)
