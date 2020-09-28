import cv2
import numpy as np
from util.data import allIcons


class Image:

    _instance = None

    def __new__(cls, *args, **kwargs):  
        if cls._instance is None:  
            cls._instance = super(Image, cls).__new__(cls, *args, **kwargs)  
            cls._instance.init = False  
        return cls._instance  

    def __init__(self, *args, **kwargs):
        if self.init:
            return
        self.init = True
        super().__init__(*args, **kwargs)
    
        self.image = None
        data = allIcons()
        self.all_images_array = data.all_images_array
        
    def reset(self):
        del self.image
        self.image = None
        
    def add_new_team(self, images, stars, ranks, type_, damage):
        image = np.ones((128, 820, 3), dtype=np.uint8) * 255
        attribute_zone_line = np.ones((120, 820, 3), dtype=np.uint8) * 255
        x = 0
        for i in images:
            image[:,x:x+128, :] = self.all_images_array[i]
            x += 133
            
        x = 0
        for star in stars:
            string = ""
            for s in star:
                string += str(s+1) + ","
            cv2.putText(attribute_zone_line, "Star:" + string[:-1], (x, 20), cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)
            x += 133
            
        x = 0
        for rank in ranks:
            string1 = ""
            string2 = ""
            string3 = ""
            for r in rank[:6]:
                string1 += str(r+1) + ","
            for r in rank[6:12]:
                string2 += str(r+1) + ","
            for r in rank[12:]:
                string3 += str(r+1) + ","
            cv2.putText(attribute_zone_line, "Rank:", (x, 40), cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(attribute_zone_line, string1[:-1], (x, 60), cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(attribute_zone_line, string2[:-1], (x, 80), cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(attribute_zone_line, string3[:-1], (x, 100), cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)
            x += 133
        
        if type_ == 1:
            t = "Full-"
        elif type_ == 2:
            t = "Semi-"
        else:
            t = "Non-"
        cv2.putText(image, t, (x, 40), cv2.FONT_HERSHEY_DUPLEX,
                    1.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, "  Auto", (x, 90), cv2.FONT_HERSHEY_DUPLEX,
                    1.5, (0, 0, 0), 1, cv2.LINE_AA)
        if "~" in damage:
            temp = damage[:-1].split("~")
            
            cv2.putText(attribute_zone_line, temp[0] + "~", (x, 40), cv2.FONT_HERSHEY_DUPLEX,
                        1.5, (0, 0, 0), 1, cv2.LINE_AA)  
            cv2.putText(attribute_zone_line, temp[1], (x, 80), cv2.FONT_HERSHEY_DUPLEX,
                        1.5, (0, 0, 0), 1, cv2.LINE_AA)
        elif "-" in damage:
            temp = damage[:-1].split("-")
            
            cv2.putText(attribute_zone_line, temp[0] + "-", (x, 40), cv2.FONT_HERSHEY_DUPLEX,
                        1.5, (0, 0, 0), 1, cv2.LINE_AA)  
            cv2.putText(attribute_zone_line, temp[1], (x, 80), cv2.FONT_HERSHEY_DUPLEX,
                        1.5, (0, 0, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(attribute_zone_line, damage[:-1], (x, 80), cv2.FONT_HERSHEY_DUPLEX,
                        2, (0, 0, 0), 1, cv2.LINE_AA)
         
        if self.image is None:
            self.image = self.image = np.concatenate([image, attribute_zone_line], axis=0)
        else:
            self.image = np.concatenate([image, attribute_zone_line, self.image], axis=0)
    
    def save(self, path):
        if self.image is None:
            return
        cv2.imwrite(path, self.image)
        