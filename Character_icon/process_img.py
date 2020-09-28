import os
import cv2
import numpy as np

border_width = 7

def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img
    
def cv_imwrite(filePath, image):
    cv2.imencode('.png', image)[1].tofile(filePath)

for name in os.listdir("./raw"):
    im = cv_imread("./raw/" + name)
    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            if y < border_width or im.shape[0] - y < border_width or x < border_width or im.shape[1] - x < border_width:
                if im.shape[2] == 4:
                    im[y, x, :] = [0, 0, 255, 255]
                else:
                    im[y, x, :] = [0, 0, 255]
    cv_imwrite("./selected/" + name, im)
              
    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            if y < border_width or im.shape[0] - y < border_width or x < border_width or im.shape[1] - x < border_width:
                if im.shape[2] == 4:
                    im[y, x, :] = [0, 0, 0, 255]
                else:
                    im[y, x, :] = [0, 0, 0]          

    cv_imwrite("./unselected/" + name, im)