import os
import tkinter as tk
import subprocess
from tkinter import ttk, Toplevel, font
from functools import partial
from globals import *

class ConfigGUI:
    def __init__(self):
        self.top_module_name = top_module_name
        self.sim_directory_path = sim_directory_path
        self.testcase_directory = testcase_directory
        self.compilation_command = compilation_command
        self.testcase_list = testcase_list
        buttons_database = {}
        textbox_database = {}
        self.textbox_database = textbox_database
        self.button_database = buttons_database
        self.width = 600
        self.height = 500
        # main window configurations
        self.main_window = tk.Tk()
        self.main_window.title("Command Execution GUI")
        self.screenwidth = self.main_window.winfo_screenwidth()
        self.screenheight = self.main_window.winfo_screenheight()
        geometry_alignment = '%dx%d+%d+%d' % (self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2)
        self.main_window.geometry(geometry_alignment)
        self.main_window.configure(bg='light gray') #0d0d0d

        self.button_panel = tk.Frame(self.main_window, width=150, bg='light gray')
        self.button_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar = tk.Scrollbar(self.main_window)

        custom_font = font.nametofont("TkFixedFont")
        custom_font.configure(family="Consolas", size=12)

        self.terminal_output = tk.Text(self.main_window, wrap=tk.WORD, bg="black", fg="white", font=custom_font,
                                       yscrollcommand=self.scrollbar.set)
        self.terminal_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.textbox_database.update({"terminal" : self.terminal_output})

        self.scrollbar.config(command=self.terminal_output.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.read_config()

    def read_config(self):
        global top_module_name, sim_directory_path, testcase_directory, compilation_command
        file = os.path.join(config_database_path, 'config.txt')
        if os.path.exists(file):
            data = []
            with open(file, 'r') as file:
                data = file.readlines()
            for name in data:
                out = name.split(':-')
                if 'top module name' in out[0]:
                    self.top_module_name = out[1].replace(' ', '')[:-1]
                elif 'sim directory path' in out[0]:
                    self.sim_directory_path = out[1].replace(' ', '')[:-1]
                elif 'testcase directory path' in out[0]:
                    self.testcase_directory = out[1].replace(' ', '')[:-1]
                elif 'compilation_command' in out[0]:
                    self.compilation_command = out[1].replace(' ', '')[:-1]
        else:
            self.display_output('Complete the configuration process first!!')
        if self.top_module_name == '' or self.sim_directory_path == '' or self.testcase_directory == '' or self.compilation_command == '':
            self.display_output('Complete the configuration process first!!')

    def set_geomatry(self, scale = '600x500'):
        coordinates = scale.split('x')
        self.width, self.height = int(coordinates[0]), int(coordinates[1])
        geometry_alignment = '%dx%d+%d+%d' % (self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2)
        self.main_window.geometry(geometry_alignment)

    def add_button(self, button_id, button_label, button_function, *args):
        container = self.button_panel
        button_function = partial(button_function, *args)
        button = tk.Button(container, text=button_label, command=button_function)
        button.pack()
        self.button_database.update({button_id: button})

    def set_button_location(self, button_id, horizontal_mult=1, vertical_mult=1, x_offset = 0, y_offset = 0, anchor = 'none'):
        if button_id in self.button_database:
            button = self.button_database[button_id]
            button.place(relx=horizontal_mult, rely=vertical_mult, x=x_offset, y=y_offset, anchor=anchor)

    def button_paddings(self, button_id, x_padding, y_padding):
        if button_id in self.button_database:
            button = self.button_database[button_id]
            button.config(padx=x_padding, pady=y_padding)

    def move_button(self, button_id, cordinates='50,10'):
        x, y = cordinates.replace(' ', '').split(',')
        button = self.button_database[button_id]
        button.place(x=x, y=y)

    def list_all_button_ids(self):
        for idx, key in enumerate(self.button_database):
            print(f'{idx+1}. {key}')

    def root_window_range(self):
        return self.main_window.winfo_width(), self.main_window.winfo_height()

    def add_textbox(self, textbox_id):
        textbox = tk.Text(self.main_window, wrap=tk.WORD)
        textbox.pack()
        self.textbox_database.update({textbox_id : textbox})

    def run_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            self.display_output(f"gui-consol >>> {command}\n\n{output}\n")
        except subprocess.CalledProcessError as e:
            self.display_output(f"gui-consol >>> {command}\n\n{e.output}\n")

    def display_output(self, text):
        self.terminal_output.insert(tk.END, text)

    def create_textbox(self, window, lable_str, row):
        label = tk.Label(window, text=f'{lable_str} : ', bg="light gray")
        #label.pack(side=tk.LEFT)
        label.grid(row=row, column=0, sticky="w")
        textbox = tk.Entry(window, width=int(self.width/10))
        textbox.grid(row=row, column=1)
        self.textbox_database.update({lable_str : textbox})