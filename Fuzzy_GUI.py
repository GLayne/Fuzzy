# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 15:32:44 2019

@author: Gabriel Lainesse (GLayne)
"""
import Fuzzy
import tkinter as tk
import tkinter.filedialog as filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=100, pady=100)
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self)
        self.title_label["text"] = "Fuzzy Matching"
        self.title_label.pack(side="top")
        
        self.btn_select_first_file = tk.Button(self)
        self.btn_select_first_file["text"] = "Select First File"
        self.btn_select_first_file["command"] = self.select_first_file
        self.btn_select_first_file.pack(side="top")
        
        self.btn_select_second_file = tk.Button(self)
        self.btn_select_second_file["text"] = "Select Second File"
        self.btn_select_second_file["command"] = self.select_second_file
        self.btn_select_second_file.pack(side="top")
        
        
        
        self.quit = tk.Button(self, text="Quit",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def select_first_file(self):
        first_file_path = filedialog.askopenfilename()
        
    def select_second_file(self):
        second_file_path = filedialog.askopenfilename()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
