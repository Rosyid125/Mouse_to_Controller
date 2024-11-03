import pyvjoy
import pyautogui
import time
import sys
from pynput import mouse
import tkinter as tk
import ttkbootstrap as ttk

# Checking the env that is now used
print(sys.executable)

# Initialize vJoy device
j = pyvjoy.VJoyDevice(1)  # Assuming device ID 1

def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        if pressed:
            j.set_button(4, 1)
        else:
            j.set_button(4, 0)

    if button == mouse.Button.right:
        if pressed:
            j.set_button(1, 1)
        else:
            j.set_button(1, 0)

def on_scroll(x, y, dx, dy):
    if dy < 0:
        j.set_button(2, 1)
        time.sleep(0.01)
        j.set_button(2, 0)
    elif dy > 0:
        j.set_button(3, 1)
        time.sleep(0.01)
        j.set_button(3, 0)

# Mouse listener
listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
listener.start()

# Get screen size to normalize mouse position
screen_width, screen_height = pyautogui.size()

# Function to normalize mouse position to vJoy axis range
def normalize(value, max_value):
    return int((value / max_value) * 0x8000)  # Normalized to 0-32767

# Fungsi untuk mengupdate panjang balok pada Canvas sesuai dengan nilai slider
def update_y_up(*args):
    value = y_up.get()
    height = int((value / 16383) * 200)
    canvas_y_up.delete("bar")
    canvas_y_up.create_rectangle(20, 200 - height, 80, 200, fill="green", tags="bar")

def update_y_down(*args):
    value = y_down.get()
    height = int((value / 16383) * 200)
    canvas_y_down.delete("bar")
    canvas_y_down.create_rectangle(20, 0, 80, height, fill="red", tags="bar")

def update_x_left(*args):
    value = x_left.get()
    width = int((value / 16383) * 50)
    canvas_x_left.delete("bar")
    canvas_x_left.create_rectangle(50 - width, 20, 50, 80, fill="blue", tags="bar")

def update_x_right(*args):
    value = x_right.get()
    width = int((value / 16383) * 50)
    canvas_x_right.delete("bar")
    canvas_x_right.create_rectangle(0, 20, width, 80, fill="orange", tags="bar")

# Membuat window dengan ttkbootstrap
root = ttk.Window(themename="darkly")
root.title("Mouse to vJoy")
root.attributes("-topmost", True)  # Membuat jendela tetap di atas
root.attributes("-alpha", 0.7)     # Menyesuaikan transparansi window
root.overrideredirect(True)        # Menghilangkan border dan title bar

# Variables for the sliders
x_left = tk.IntVar()
x_right = tk.IntVar()
y_up = tk.IntVar()
y_down = tk.IntVar()

# Menghubungkan update fungsi dengan perubahan nilai slider
y_up.trace_add("write", update_y_up)
y_down.trace_add("write", update_y_down)
x_left.trace_add("write", update_x_left)
x_right.trace_add("write", update_x_right)

# Create a frame for the "+" layout
frame = tk.Frame(root)
frame.pack()

# Create a subframe for Y axis (vertical layout)
frame_y = tk.Frame(frame)
frame_y.grid(row=1, column=2)

# Canvas untuk Y-Up slider (balok hijau)
canvas_y_up = tk.Canvas(frame_y, width=100, height=200, bg="white")
canvas_y_up.pack()
update_y_up()  # Inisialisasi tampilan awal

# Create a subframe for X axis (horizontal layout)
frame_x = tk.Frame(frame)
frame_x.grid(row=2, column=1)

# Canvas untuk X-Left slider (balok biru)
canvas_x_left = tk.Canvas(frame_x, width=50, height=100, bg="white")
canvas_x_left.pack()
update_x_left()  # Inisialisasi tampilan awal

# Create a subframe for X axis again (horizontal layout)
frame_x2 = tk.Frame(frame)
frame_x2.grid(row=2, column=3)

# Canvas untuk X-Right slider (balok oranye)
canvas_x_right = tk.Canvas(frame_x2, width=50, height=100, bg="white")
canvas_x_right.pack()
update_x_right()  # Inisialisasi tampilan awal

# Create a subframe for Y axis again (horizontal layout)
frame_y2 = tk.Frame(frame)
frame_y2.grid(row=3, column=2)

# Canvas untuk Y-Down slider (balok merah)
canvas_y_down = tk.Canvas(frame_y2, width=100, height=200, bg="white")
canvas_y_down.pack()
update_y_down()  # Inisialisasi tampilan awal

# Function to update joystick and sliders
def update_joystick():
    # Get current mouse position
    mouse_x, mouse_y = pyautogui.position()

    # Normalize to vJoy range (0 - 32767)
    joy_x = normalize(mouse_x, screen_width)
    joy_y = normalize(mouse_y, screen_height)

    # Set the value of the sliders (center at 0, max 16383)
    if joy_x > 16383:  # Value above half
        x_right.set(joy_x - 16383)  # Move right slider
        x_left.set(0)  # Reset the left slider
    else:
        x_right.set(0)  # Reset the right slider
        x_left.set(16383 - joy_x)  # Move left slider

    if joy_y > 16383:  # Value above half
        y_down.set(joy_y - 16383)  # Move down slider
        y_up.set(0)  # Reset the up slider
    else:
        y_down.set(0)  # Reset the down slider
        y_up.set(16383 - joy_y)  # Move up slider

    # Set vJoy axis
    j.set_axis(pyvjoy.HID_USAGE_X, joy_x)
    j.set_axis(pyvjoy.HID_USAGE_Y, joy_y)

    # Schedule the function to be called again after 10ms
    root.after(50, update_joystick) # Lower makes mouse move detection smoother but requires huge cpu usage, normal is 50 ms (same like discord cpu usage when on background)

# Start updating the joystick
update_joystick()

# Start the Tkinter main loop
root.mainloop()
