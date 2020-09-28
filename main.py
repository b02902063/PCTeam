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
    
        self.first_id = 0
        self.damages = []
        self.automaticity = []
        
        self.team_existence = []
        self.image_on_click_list = []
        
        self.added = False
        self.root = tk.Tk()
        
        self.all_images = []
        self.all_damages_label = []
        self.all_automaticity_label = []
        self.star_var = []
        self.rank_var = []
        
        self.current_images = []
        self.current_images_index = []
        self.current_star = []
        self.current_rank = []
        self.all_label_imgs = []         
        
        self.root.title("PCTeam")
        container = tk.Frame(self.root)        
 
        canvas= tk.Canvas(container, width=850)
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
        delete_button = tk.Button(buttom_frame, text="Delete Selected Team", command=self.remove_team).pack(side=tk.LEFT, padx=(30, 0))
        
        self.radio_value = tk.IntVar()
        self.radio_value.set(1)
        
        def generate_radio_command(value):
            if value == 1:
                def on_select():
                    team_index = self.selected_image//5
                    self.automaticity[team_index] = value
                    self.all_automaticity_label[team_index].set("Full-Auto")
            elif value == 2:
                def on_select():
                    team_index = self.selected_image//5
                    self.automaticity[team_index] = value
                    self.all_automaticity_label[team_index].set("Semi-Auto")
            else:
                def on_select():
                    team_index = self.selected_image//5
                    self.automaticity[team_index] = value
                    self.all_automaticity_label[team_index].set("Non-Auto")
            return on_select
     
        tk.Radiobutton(buttom_frame, text="全自動", variable=self.radio_value, value=1, command=generate_radio_command(1)).pack(side=tk.LEFT, padx=(30, 0))
        tk.Radiobutton(buttom_frame, text="半自動", variable=self.radio_value, value=2, command=generate_radio_command(2)).pack(side=tk.LEFT)
        tk.Radiobutton(buttom_frame, text="手動", variable=self.radio_value, value=3, command=generate_radio_command(3)).pack(side=tk.LEFT)
        var = tk.StringVar()
        var.set("傷害：")
        tk.Label(buttom_frame, textvariable=var).pack(side=tk.LEFT, padx=(30, 0))
        self.damage = tk.StringVar()
        
        def on_trace(name, index, mode, sv=self.damage):
            team_index = self.selected_image//5
            self.damages[team_index] = sv.get()
            self.all_damages_label[team_index].set(sv.get())
            
        self.damage.trace("w", on_trace)
        tk.Entry(buttom_frame, textvariable=self.damage).pack(side=tk.LEFT)  
        
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
        
    def remove_team(self):
        if sum(self.team_existence) == 1:
            return
        team = self.selected_image//5
        start = 5 * team
        end = 5 * team + 5
        self.damages[team] = -1
        self.automaticity[team] = -1
        self.all_automaticity_label[team] = -1
        self.all_damages_label[team] = -1
        self.current_images[start:end] = [-1, -1, -1, -1, -1]
        self.current_images_index[start:end] = [-1, -1, -1, -1, -1]
        self.current_star[start:end] = [-1, -1, -1, -1, -1]
        self.current_rank[start:end] = [-1, -1, -1, -1, -1]
        self.rank_var[start:end] = [-1, -1, -1, -1, -1]
        self.star_var[start:end] = [-1, -1, -1, -1, -1]
        self.image_on_click_list[start:end] = [-1, -1, -1, -1, -1]
        self.team_existence[team] = False
        
        def find_last_true(in_):
            for i, x in enumerate(reversed(in_)):
                if x:
                    break
            return len(in_) - i - 1
            
        last_true = find_last_true(self.team_existence)
        self.image_on_click_list[5*last_true]()
        
        temp = self.all_teams[team]
        self.all_teams[team] = -1
        temp.destroy()
        
        
    def add_new_team(self):
        self.saved = False
        if self.added:
            for n, i in zip(self.current_images, self.all_images):
                if n == -1:
                    continue
                i.image = self.all_unselected_icons[n]
                i.configure(image=self.all_unselected_icons[n])
        else:
            self.added = True
        self.selected_image = self.first_id
        
        self.damages.append("")
        self.automaticity.append(1)
        self.team_existence.append(True)
        holder = tk.Frame(self.team_frame)
        holder.pack(side=tk.BOTTOM, pady=(5, 0))
        character_frame = tk.Frame(holder, width=800)
        self.all_teams.append(holder)
        character_frame.pack(side=tk.LEFT)
        
        ad_frame = tk.Frame(holder)
        ad_frame.pack(side=tk.LEFT, padx=(0, 0), anchor=tk.NW)
        
        var = tk.StringVar()
        var.set("Full-Auto")
        self.all_automaticity_label.append(var)
        tk.Label(ad_frame, textvariable=var, font=("Arial", 20), width=10, height=1).grid(row=0, column=0)

        tk.Label(ad_frame, text="Damage:", font=("Arial", 20), width=10, height=1).grid(row=1, column=0) 
        
        var = tk.StringVar()
        var.set("")
        self.all_damages_label.append(var)
        tk.Label(ad_frame, textvariable=var, font=("Arial", 20), width=10, height=1).grid(row=2, column=0)  
        
        for i in range(self.first_id, self.first_id+5):
            self.current_images.append("empty")
            self.current_images_index.append(-1)
            self.current_star.append([])
            self.current_rank.append([])
            self.rank_var.append([])
            if i == 0:
                label_img = tk.Label(character_frame, image=self.all_selected_icons["empty"])
            else:
                label_img = tk.Label(character_frame, image=self.all_unselected_icons["empty"])
            self.all_label_imgs.append(label_img)
            label_img.grid(row=0, column=i-self.first_id)
            on_click = self._image_on_click_event_generator(i)
            self.image_on_click_list.append(on_click)
            label_img.bind("<Button-1>", on_click)
            self.all_images.append(label_img)
            
            var = tk.StringVar()
            var.set("星數：")
            self.star_var.append(var)
            label = tk.Label(character_frame, textvariable=var, wraplength=128)
            label.grid(row=1, column=i-self.first_id, sticky=tk.W)
            
            var = tk.StringVar()
            var.set("Rank：")
            self.rank_var[i].append(var)
            label = tk.Label(character_frame, textvariable=var, wraplength=125)
            label.grid(row=2, column=i-self.first_id, sticky=tk.W)
            
            var = tk.StringVar()
            var.set(" ")
            self.rank_var[i].append(var)
            label = tk.Label(character_frame, textvariable=var, wraplength=125)
            label.grid(row=3, column=i-self.first_id, sticky=tk.W)
            
            var = tk.StringVar()
            var.set(" ")
            self.rank_var[i].append(var)
            label = tk.Label(character_frame, textvariable=var, wraplength=125)
            label.grid(row=4, column=i-self.first_id, sticky=tk.W)
            if i == self.first_id:
                temp_o = on_click
        self.first_id += 5
        temp_o()
        
    def run(self):
        self.root.mainloop()
        
    def _save(self):
        f = filedialog.asksaveasfilename (defaultextension=".jpg", initialdir = "./",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if not f.endswith("jpg") and not f.endswith("jpeg"):
            return

        self.image.generate(self.current_images, self.current_star, self.current_rank, self.automaticity, self.damages, self.team_existence)
        self.image.save(f)
        
    def _image_on_click_event_generator(self, num):
        def on_click(event=None):
            self.selected_image = num
            self.all_images[num].image = self.all_selected_icons["empty"]
            self.all_images[num].configure(image=self.all_selected_icons["empty"])
            for i in range(len(self.current_images)):
                if self.current_images[i] == -1:
                    continue
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
            self.radio_value.set(self.automaticity[num//5])
            self.damage.set(self.damages[num//5])
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

