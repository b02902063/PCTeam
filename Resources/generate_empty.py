import os
import cv2
import numpy as np

border_width = 7

im = np.zeros((128, 128, 4), dtype=np.uint8)
for y in range(im.shape[0]):
    for x in range(im.shape[1]):
        if y < border_width or im.shape[0] - y < border_width or x < border_width or im.shape[1] - x < border_width:
            if im.shape[2] == 4:
                im[y, x, :] = [0, 0, 255, 255]
            else:
                im[y, x, :] = [0, 0, 255]
cv2.imwrite("./Selected.png", im)
         
im = np.zeros((128, 128, 4), dtype=np.uint8)         
for y in range(im.shape[0]):
    for x in range(im.shape[1]):
        if y < border_width or im.shape[0] - y < border_width or x < border_width or im.shape[1] - x < border_width:
            if im.shape[2] == 4:
                im[y, x, :] = [0, 0, 0, 255]
            else:
                im[y, x, :] = [0, 0, 0]          

cv2.imwrite("./Empty.png", im)