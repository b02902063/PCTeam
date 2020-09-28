import os
import tkinter as tk
import cv2
import numpy as np


def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img

class allIcons:
    
       
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(allIcons, cls).__new__(cls, *args, **kwargs)
            cls._instance.init = False
        return cls._instance
    
    def __init__(self):
        if self.init:
            return
        self.init  = True

        self.all_selected_icons = {"empty": tk.PhotoImage(file='./Resources/Selected.png')}
        self.all_unselected_icons = {"empty": tk.PhotoImage(file='./Resources/Unselected.png')}
        self.all_images_array = {"empty": cv2.imread("./Resources/Empty.png")}
        self.all_names = []

        for filename in os.listdir("./Character_icon/raw"):
            selected_path = os.path.join("./Character_icon/selected", filename)
            unselected_path = os.path.join("./Character_icon/unselected", filename)
            raw_path = os.path.join("./Character_icon/raw", filename)
            
            basename = os.path.splitext(filename)[0]
            self.all_selected_icons[basename] = tk.PhotoImage(file=selected_path)
            self.all_unselected_icons[basename] = tk.PhotoImage(file=unselected_path)
            self.all_images_array[basename] = cv_imread(raw_path)[:, :, :3]
            self.all_names.append(basename)
                
        
        