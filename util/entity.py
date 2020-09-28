import tkinter as tk
from util.data import allIcons
from util.image import Image


data = allIcons()
image = Image

class Character:

    def __init__(self):
        self.name = "empty"
        self.star = []
        self.rank = []
        
    def init_widgets(self):
        
        
    def set_name(self, name):
        self.name = name
    
    def set_star(self, star):
        self.star = star
        
    def set_rank(self, rank):
        self.rank = rank

class Team:

    
    def __init__(self):
        self.characters = []

if self.added:
            for n, i in zip(self.current_images, self.all_images):
                i.image = self.all_unselected_icons[n]
                i.configure(image=self.all_unselected_icons[n])
            for l in self.all_label_imgs:
                l.unbind("<Button 1>")
            self.image.add_new_team(self.current_images, self.current_star, self.current_rank, self.radio_value.get(), self.damage.get(1.0, tk.END))
        else:
            self.added = True
        self.selected_image = 0
        self.all_images = []

        self.all_unselected_icons["empty"] = tk.PhotoImage(file='./Resources/Unselected.png')
        self.all_selected_icons["empty"] = tk.PhotoImage(file='./Resources/Selected.png')
        self.current_images = ["empty", "empty", "empty", "empty", "empty"]
        self.current_images_index = [-1, -1, -1, -1, -1]
        self.current_star = [[], [], [], [], []]
        self.current_rank = [[], [], [], [], []]
        self.all_label_imgs = []
        
        self.star_var = []
        self.rank_var = [[], [], [], [], []]
        
        character_frame = tk.Frame(self.team_frame)
        self.all_teams.append(character_frame)
        character_frame.pack(side=tk.BOTTOM, pady=(5, 0))
        for i in range(5):
            if i == 0:
                label_img = tk.Label(character_frame, image=self.all_selected_icons["empty"])
            else:
                label_img = tk.Label(character_frame, image=self.all_unselected_icons["empty"])
            self.all_label_imgs.append(label_img)
            label_img.grid(row=0, column=i)
            on_click = self._image_on_click_event_generator(i)
            label_img.bind("<Button-1>", on_click)
            self.all_images.append(label_img)
            
            var = tk.StringVar()
            var.set("星數：")
            self.star_var.append(var)
            label = tk.Label(character_frame, textvariable=var, wraplength=128)
            label.grid(row=1, column=i, sticky=tk.W)
            
            var = tk.StringVar()
            var.set("Rank：")
            self.rank_var[i].append(var)
            label = tk.Label(character_frame, textvariable=var, wraplength=125)
            label.grid(row=2, column=i, sticky=tk.W)
            
            var = tk.StringVar()
            var.set(" ")
            self.rank_var[i].append(var)
            label = tk.Label(character_frame, textvariable=var, wraplength=125)
            label.grid(row=3, column=i, sticky=tk.W)
            
            var = tk.StringVar()
            var.set(" ")
            self.rank_var[i].append(var)
            label = tk.Label(character_frame, textvariable=var, wraplength=125)
            label.grid(row=4, column=i, sticky=tk.W)
            if i == 0:
                temp_o = on_click