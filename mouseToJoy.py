import pyvjoy
import pyautogui
import time
import sys
from pynput import mouse

# Checking the env that is now used
print(sys.executable)

# Initialize vJoy device
j = pyvjoy.VJoyDevice(1)  # Assuming device ID 1

def on_click(x, y, button, pressed):
    # print('{0} at {1}'.format(
    #     'Pressed' if pressed else 'Released',
    #     (x, y)))
    if button == mouse.Button.left:
        if pressed:
            j.set_button(4, 1)
        elif not pressed:
            j.set_button(4, 0)

    if button == mouse.Button.right:
        if pressed:
            j.set_button(1, 1)
        elif not pressed:
            j.set_button(1, 0)

def on_scroll(x, y, dx, dy):
    # print('Scrolled {0} at {1}'.format(
    #     'down' if dy < 0 else 'up',
    #     (x, y)))
    if dy < 0:
        j.set_button(2, 1)
        time.sleep(0.01)
        j.set_button(2, 0)
    elif dy > 0:
        j.set_button(3, 1)
        time.sleep(0.01)
        j.set_button(3, 0)

# Collect events until released (ini blocking ya jadi nanti ctrl c nya nggak bisa digunakan untuk terminate)
# with mouse.Listener(
#         on_click=on_click,
#         on_scroll=on_scroll) as listener:
#     listener.join()

# ini baru yang non blocking
listener = mouse.Listener(
    on_click=on_click,
    on_scroll=on_scroll)
listener.start()

# Get screen size to normalize mouse position
screen_width, screen_height = pyautogui.size()

# Function to normalize mouse position to vJoy axis range
def normalize(value, max_value):
    return int((value / max_value) * 0x8000)  # Normalized to 0-32767

try:
    while True:
        # Get current mouse position
        mouse_x, mouse_y = pyautogui.position()

        # Normalize to vJoy range
        joy_x = normalize(mouse_x, screen_width)
        joy_y = normalize(mouse_y, screen_height)

        # Set vJoy axis
        j.set_axis(pyvjoy.HID_USAGE_X, joy_x)
        j.set_axis(pyvjoy.HID_USAGE_Y, joy_y)

        # Small delay to prevent excessive CPU usage
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Script terminated by user.")
