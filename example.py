import cv2
import numpy as np
from image_p import *
from toolkit import *
from cv2 import imread as ir

dst=stretchProperly(r'C:\Users\Administrator\Desktop\Documents\python_work\cours_image\im\1.jpg')
dst=threshProperly(dst)
cv_show(dst)


#print(np.array([1,1])*5)