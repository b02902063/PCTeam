import tkinter as tk
from tkinter import filedialog
import cv2
import os
import numpy as np
from util.data import allIcons
from util.image import Image


chinese_number = ["一", "二", "三", "四", "五", "六"]

def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img

class PCTeam:

    def __init__(self):
        
        self.added = False
        self.saved = False
        self.root = tk.Tk()
        self.root.title("PCTeam")
        container = tk.Frame(self.root)        
 
        canvas= tk.Canvas(container, width=700)
        self.canvas = canvas
        vbar = tk.Scrollbar(canvas, orient=tk.VERTICAL, command=canvas.yview) 
        self.team_frame = tk.Frame(canvas)
        self.all_teams = []
        vbar.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        self.team_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.team_frame, anchor="nw")
        canvas.configure(yscrollcommand=vbar.set)
        
        container.grid(row=0, column=0, pady=(20, 0)) 
        canvas.pack(side="left", fill="both", expand=True)
        vbar.pack(side="right", fill="y")
        
        buttom_frame = tk.Frame(self.root)
        buttom_frame.grid(row=1, column=0)
        new_team_button = tk.Button(buttom_frame, text="Add New Team", command=self.add_new_team).pack(side=tk.LEFT)
        save_button = tk.Button(buttom_frame, text="Save", command=self._save).pack(side=tk.LEFT, padx=(30, 0))
        
        self.radio_value = tk.IntVar()
        self.radio_value.set(1)
        tk.Radiobutton(buttom_frame, text="全自動", variable=self.radio_value, value=1).pack(side=tk.LEFT, padx=(30, 0))
        tk.Radiobutton(buttom_frame, text="半自動", variable=self.radio_value, value=2).pack(side=tk.LEFT)
        tk.Radiobutton(buttom_frame, text="手動", variable=self.radio_value, value=3).pack(side=tk.LEFT)
        var = tk.StringVar()
        var.set("傷害：")
        tk.Label(buttom_frame, textvariable=var).pack(side=tk.LEFT, padx=(30, 0))
        self.damage = tk.Text(buttom_frame, height=1, width=20)
        self.damage.pack(side=tk.LEFT)  
        
        
        data = allIcons()
        self.all_listboxes = []
        self.all_selected_icons = data.all_selected_icons
        self.all_unselected_icons = data.all_unselected_icons
        self.all_names = data.all_names
        self.all_images_array = data.all_images_array
        self.image = Image()
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=2, column=0, pady=(20, 20))
        
        def character_on_select(event=None):
            if not self.added:
                return
            w = event.widget
            index = int(w.curselection()[0])
            name = w.get(index)
            img = self.all_selected_icons[name]
            self.all_images[self.selected_image].image = img
            self.all_images[self.selected_image].configure(image=img)
            self.current_images[self.selected_image] = name
            self.current_images_index[self.selected_image] = index
            
        def star_on_select(event=None):
            if not self.added:
                return
            w = event.widget
            index = [int(x) for x in w.curselection()]
            self.current_star[self.selected_image] = index
            
            var = self.star_var[self.selected_image]
            string = "星數："
            for i in sorted(index):
                string += chinese_number[i] + ","
            var.set(string[:-1])
         
        def rank_on_select(event=None):
            if not self.added:
                return
            w = event.widget
            index = [int(x) for x in w.curselection()]
            self.current_rank[self.selected_image] = index
            vars_ = self.rank_var[self.selected_image]
            vars_[0].set("Rank：")
            vars_[1].set(" ")
            vars_[2].set(" ")
            string = "Rank："
            for i, n in enumerate(sorted(index)):
                string += str(n+1) + ","
                vars_[i // 6].set(string[:-1])
                if (i + 1) % 6 == 0:
                    string = "          "
        self._generate_listbox_with_scrollbar(control_frame, self.all_names, anchor="w", on_select=character_on_select)
        self._generate_listbox_with_scrollbar(control_frame, ["一星", "二星", "三星", "四星", "五星", "六星"], selectmode=tk.MULTIPLE, on_select=star_on_select)
        self._generate_listbox_with_scrollbar(control_frame, \
                                              ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15", "R16", "R17"], \
                                              selectmode=tk.MULTIPLE, anchor="e", on_select=rank_on_select)
       
        self.add_new_team()
        
    def add_new_team(self):
        self.saved = False
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
        temp_o()
        
    def run(self):
        self.root.mainloop()
        
    def _save(self):
        f = filedialog.asksaveasfilename (defaultextension=".jpg", initialdir = "./",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if not f.endswith("jpg") and not f.endswith("jpeg"):
            return

        if not self.saved:
            self.image.add_new_team(self.current_images, self.current_star, self.current_rank, self.radio_value.get(), self.damage.get(1.0, tk.END))
        self.image.save(f)
        self.saved = True
        
    def _image_on_click_event_generator(self, num):
        def on_click(event=None):
            self.selected_image = num
            self.all_images[num].image = self.all_selected_icons["empty"]
            self.all_images[num].configure(image=self.all_selected_icons["empty"])
            for i in range(5):
                if i == num:
                    self.all_images[i].image = self.all_selected_icons[self.current_images[i]]
                    self.all_images[i].configure(image=self.all_selected_icons[self.current_images[i]])
                else:
                    self.all_images[i].image = self.all_unselected_icons[self.current_images[i]]
                    self.all_images[i].configure(image=self.all_unselected_icons[self.current_images[i]])
            for lb in self.all_listboxes:
                lb.selection_clear(0, tk.END)
            self.all_listboxes[0].select_set(self.current_images_index[num])
            for i in self.current_star[num]:
                self.all_listboxes[1].select_set(i)
            for i in self.current_rank[num]:
                self.all_listboxes[2].select_set(i)
        return on_click
        
    def _generate_listbox_with_scrollbar(self, root, item_list, selectmode=tk.SINGLE, anchor=None, on_select=None):
        listbox_frame = tk.Frame(root)
        listbox_frame.pack(side=tk.LEFT, padx=(20, 0), anchor=anchor)

        listbox = tk.Listbox(listbox_frame, selectmode=selectmode, height=25, activestyle="none")
        listbox.pack(side=tk.LEFT)
        scroll_bar = tk.Scrollbar(listbox_frame)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.BOTH)
        listbox.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=listbox.yview)
        for n in item_list:
            listbox.insert(tk.END, n)
        listbox.configure(exportselection=False)
        if on_select is not None:
            listbox.bind("<<ListboxSelect>>", on_select)
        self.all_listboxes.append(listbox)

if __name__ == "__main__":
    _main = PCTeam()
    _main.run()

