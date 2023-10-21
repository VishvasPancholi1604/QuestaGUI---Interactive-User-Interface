from functools import partial
import tkinter as tk
from tkinter import ttk, Toplevel, font
import os

def extract_testcases(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_name_without_extension = file_name.split(".")[0]
            if "base_test" not in file_name_without_extension and "testbench" not in file_name_without_extension and "configurable_testcase" not in file_name_without_extension:
                files.append(file_name_without_extension + '_c')
    if len(files) == 0:
        files.append(f'ei_{project_name}_base_test_c')
    return files

def get_textbox_value():
    pass

def add_button(root, window, button_id, button_label, button_function, *args):
    button_function = partial(button_function, *args)
    button = tk.Button(window, text=button_label, command=button_function)
    root.button_database.update({button_id: button})