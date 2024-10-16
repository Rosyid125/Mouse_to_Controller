import pyvjoy
import pyautogui
import time
import sys
from pynput import mouse
import tkinter as tk
import ttkbootstrap as ttk
import ctypes

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

# Membuat window dengan ttkbootstrap
root = ttk.Window(themename="darkly")
root.title("Mouse to vJoy")
root.attributes("-topmost", True)  # Membuat jendela tetap di atas

# Mengatur window transparan
root.attributes("-alpha", 0.7)  # Menyesuaikan nilai alpha untuk tingkat transparansi (0.0 - 1.0)
root.overrideredirect(True)  # Menghilangkan border dan title bar, soalnya kalau ditampilkan jg gabisa ditekan hehe

# Mendapatkan handle jendela Tkinter
root.update_idletasks()
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())

# Atur jendela untuk tembus klik menggunakan Windows API
# WS_EX_LAYERED = 0x00080000, WS_EX_TRANSPARENT = 0x00000020
ctypes.windll.user32.SetWindowLongW(hwnd, -20, 
    ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x00080000 | 0x00000020)

# Variables for the sliders
x_left = tk.IntVar()
x_right = tk.IntVar()
y_up = tk.IntVar()
y_down = tk.IntVar()

# Create a frame for the "+" layout
frame = tk.Frame(root)
frame.pack()

# Create a subframe for Y axis (vertical layout)
frame_y = tk.Frame(frame)
frame_y.grid(row=1, column=1)

# Create Y-Up slider (top of the layout) with green style
slider_y_up = ttk.Scale(frame_y, from_=16383, to=0, variable=y_up, bootstyle="success", orient=tk.VERTICAL, length=200)
slider_y_up.pack()

# Create a subframe for X axis (horizontal layout)
frame_x = tk.Frame(frame)
frame_x.grid(row=2, column=1)

# Create X-Left slider (left of the layout) - using default style
slider_x_left = ttk.Scale(frame_x, from_=16383, to=0, variable=x_left, bootstyle="info", orient=tk.HORIZONTAL, length=100)
slider_x_left.pack(side=tk.LEFT)

# Create X-Right slider (right of the layout) - using default style
slider_x_right = ttk.Scale(frame_x, from_=0, to=16383, variable=x_right, bootstyle="warning", orient=tk.HORIZONTAL, length=100)
slider_x_right.pack(side=tk.RIGHT)

# Create a subframe for Y axis again (horizontal layout)
frame_y2 = tk.Frame(frame)
frame_y2.grid(row=3, column=1)

# Create Y-Down slider (bottom of the layout) with red style
slider_y_down = ttk.Scale(frame_y2, from_=0, to=16383, variable=y_down, bootstyle="danger", orient=tk.VERTICAL, length=200)
slider_y_down.pack()


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
    root.after(10, update_joystick)

# Start updating the joystick
update_joystick()

# Start the Tkinter main loop
root.mainloop()
