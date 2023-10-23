from tkinter import Toplevel
from supporting_functions import *
from globals import *
import json

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

    configs = f'''top module name:-{top_module_name}
sim directory path:-{sim_directory_path}
testcase directory path:-{testcase_directory}
compilation_command:-{compilation_command}
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
    create_testcases_window(root)

def compile(root):
    root.run_command(root.compilation_command)

def simulate(root):
    cmd = f'vsim {root.top_module_name} -c -do \"run -all; exit\" +UVM_TESTNAME='
    selected_testcases = get_selected_testcases(root)
    for idx, name in enumerate(selected_testcases):
        root.display_output(f'Running Testcase : {name}...\n')
        root.run_command_background(f'{cmd}{name}')

def save_checkbox_states(checkbox_states):
    with open('checkbox_states.json', 'w') as file:
        json.dump(checkbox_states, file)

def load_checkbox_states():
    try:
        with open('checkbox_states.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def create_testcases_window(root):
    testcases_window = tk.Toplevel(root.main_window)
    testcases_window.title("Testcases")

    testcases = root.testcase_list

    checkbox_states = [tk.IntVar() for _ in testcases]

    saved_states = load_checkbox_states()
    for i, state in enumerate(saved_states):
        if i < len(checkbox_states):
            checkbox_states[i].set(state)

    def on_checkbox_change():
        save_checkbox_states([var.get() for var in checkbox_states])

    for i, testcase in enumerate(testcases):
        checkbox = tk.Checkbutton(testcases_window, text=testcase, variable=checkbox_states[i], command=on_checkbox_change)
        checkbox.grid(row=i, column=0, sticky="w")

    def select_all():
        for i in range(len(checkbox_states)):
            checkbox_states[i].set(1)
        save_checkbox_states([var.get() for var in checkbox_states])

    def deselect_all():
        for i in range(len(checkbox_states)):
            checkbox_states[i].set(0)
        save_checkbox_states([var.get() for var in checkbox_states])

    def save_and_exit():
        selected_testcases = [testcases[i] for i, var in enumerate(checkbox_states) if var.get() == 1]
        print("Selected Testcases:", selected_testcases)
        testcases_window.destroy()

    select_all_button = tk.Button(testcases_window, text="Select All", command=select_all)
    select_all_button.grid(row=len(testcases), column=0, columnspan=2)

    deselect_all_button = tk.Button(testcases_window, text="Deselect All", command=deselect_all)
    deselect_all_button.grid(row=len(testcases) + 1, column=0, columnspan=2)

    save_and_exit_button = tk.Button(testcases_window, text="Save & Exit", command=save_and_exit)
    save_and_exit_button.grid(row=len(testcases) + 2, column=0, columnspan=2)

    exit_button = tk.Button(testcases_window, text="Exit", command=testcases_window.destroy)
    exit_button.grid(row=len(testcases) + 3, column=0, columnspan=2)

def get_selected_testcases(root):
    try:
        with open('checkbox_states.json', 'r') as file:
            checkbox_states = json.load(file)
        testcases = extract_testcases(root.testcase_directory)
        selected_testcases = [testcase for i, testcase in enumerate(testcases) if checkbox_states[i] == 1]
        return selected_testcases
    except FileNotFoundError:
        print("Warning: No checkbox states file found. Returning an empty list.")
        return []