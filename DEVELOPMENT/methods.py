import tkinter as tk
import subprocess
import os
from tkinter import ttk, Toplevel, font
from supporting_functions import *
from globals import *

def setting(root):
    window_width  = 515
    window_height = 130

    settings_window = Toplevel(root.main_window)
    settings_window.title("Settings")

    screenwidth = settings_window.winfo_screenwidth()
    screenheight = settings_window.winfo_screenheight()
    geometry_alignment = '%dx%d+%d+%d' % (
    window_width, window_height, (screenwidth - window_width) / 2, (screenheight - window_height) / 2)
    settings_window.geometry(geometry_alignment)
    settings_window.configure(bg='light gray')  # 0d0d0d

    root.create_textbox(settings_window, 'Top module name', row=0)
    root.create_textbox(settings_window, 'SIM directory path', row=1)
    root.create_textbox(settings_window, 'Compilation command', row=2)
    root.create_textbox(settings_window, 'Testcase directory path', row=3)

    print(top_module_name)
    root.textbox_database["Top module name"].insert(tk.END, root.top_module_name)
    root.textbox_database["SIM directory path"].insert(tk.END, root.sim_directory_path)
    root.textbox_database["Testcase directory path"].insert(tk.END, root.testcase_directory)
    root.textbox_database["Compilation command"].insert(tk.END, root.compilation_command)

    add_button(root, settings_window, "Save & Exit", "Save & Exit", save_settings, root, settings_window)
    save_exit = root.button_database["Save & Exit"]
    save_exit.grid(row=4, column=0, columnspan=2)
    save_exit.place(relx=1, rely=1, x=-int(window_width/2)-60, y=-10, anchor="sw")

    add_button(root, settings_window, "Exit", "Exit", quit_settings, settings_window)
    exit = root.button_database["Exit"]
    exit.grid(row=4, column=0, columnspan=2)
    exit.place(relx=1, rely=1, x=-int(window_width/2)+20, y=-10, anchor="sw")

def save_settings(root, window):
    file_path = os.path.join(config_database_path + 'config.txt')

    top_module_name = root.textbox_database["Top module name"].get()
    sim_directory_path = root.textbox_database["SIM directory path"].get()
    compilation_command = root.textbox_database["Compilation command"].get()
    testcase_directory = root.textbox_database["Testcase directory path"].get()

    configs = f'''top module name :- {top_module_name}
sim directory path :- {sim_directory_path}
testcase directory path :- {testcase_directory}
compilation_command :- {compilation_command}
'''
    with open(file_path, 'w') as file:
        file.write(configs)
    quit_settings(window)
    terminal = root.textbox_database["terminal"]
    terminal.insert(tk.END, '')

def quit_settings(window):
    window.destroy()

def testcase(root):
    root.testcase_list = extract_testcases(root.testcase_directory)
    testfile = os.path.join(test_database_path, 'testcases.txt')
    with open(testfile, 'w') as file:
        for name in root.testcase_list:
            file.write(f'{name}\n')

def compile():
    print(compilation_command)

def simulate(root):
    cmd = f'vsim {root.top_module_name} -c -do \"run -all; exit\" +UVM_TESTNAME='
    testfile = os.path.join(test_database_path, 'testcases.txt')
    if os.path.exists(testfile):
        with open(testfile, 'r') as file:
            testcases = file.readlines()
        for name in testcases:
            print(f'{cmd}{name[:-1]}')
    else:
        root.display_output('Register testcases first by pressing the \'testcase\' button..')