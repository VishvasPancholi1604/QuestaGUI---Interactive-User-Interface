from root import *
from methods import *
from globals import *

# 1800x900
# Create an instance of the Configure class
root = ConfigGUI()
root.set_geomatry(scale='600x500')

# Add a button to the main window
root.add_button("Settings", "Settings", setting, root)
root.set_button_location("Settings", horizontal_mult=1, vertical_mult=0, x_offset=-20, y_offset=15, anchor='ne')

pixels_from_right = 80
buttons_vertical_offset = 50
buttons_starting_position = 75

button_count = 0
root.add_button("compile button", "Compile", compile)
root.set_button_location("compile button", horizontal_mult=1, vertical_mult=0, x_offset=-pixels_from_right, y_offset=(buttons_starting_position+button_count*(buttons_vertical_offset)), anchor='n')

button_count += 1
root.add_button("testcases button", "testcases", testcase, root)
root.set_button_location("testcases button", horizontal_mult=1, vertical_mult=0, x_offset=-pixels_from_right, y_offset=(buttons_starting_position+button_count*(buttons_vertical_offset)), anchor='n')

button_count += 1
root.add_button("simulation button", "simulate", simulate, root)
root.set_button_location("simulation button", horizontal_mult=1, vertical_mult=0, x_offset=-pixels_from_right, y_offset=(buttons_starting_position+button_count*(buttons_vertical_offset)), anchor='n')

'''
button_count += 1
root.add_button("Run ls", "Run ls", lambda: root.run_command("dir"))
root.set_button_location("Run ls", horizontal_mult=1, vertical_mult=0, x_offset=-pixels_from_right, y_offset=(buttons_starting_position+button_count*(buttons_vertical_offset)), anchor='n')

button_count += 1
root.add_button("Run pwd", "Run pwd", lambda: root.run_command("pwd"))
root.set_button_location("Run pwd", horizontal_mult=1, vertical_mult=0, x_offset=-pixels_from_right, y_offset=(buttons_starting_position+button_count*(buttons_vertical_offset)), anchor='n')
'''

# Start the Tkinter main event loop
root.main_window.mainloop()