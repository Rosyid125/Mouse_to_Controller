## To Use

venv\Scripts\activate
python mouseToJoy.py

## To make

1. Install vJoy and SDK
   Download vJoy:

Go to the vJoy website and download the latest version of vJoy.
Install vJoy:

Follow the installation instructions to install vJoy on your system.
Download vJoy SDK:

Download the vJoy SDK from the vJoy website. This contains the necessary libraries for development.

2. Set Up Your Python Environment
   Install Python:

Ensure you have Python installed. You can download it from python.org.
Create a Virtual Environment:

Open a terminal or Command Prompt and navigate to your project directory.
Create a virtual environment:
bash

python -m venv venv
Activate the Virtual Environment:

Command Prompt (Windows):
bash

venv\Scripts\activate
PowerShell (Windows):
bash

.\venv\Scripts\Activate.ps1
Unix-like Systems (Linux/macOS):
bash

source venv/bin/activate
Install Required Libraries:

Install pyvjoy and pyautogui using pip:
bash

pip install pyvjoy pyautogui

3. Create the Python Script
   Create a New Python File:

In your project directory, create a new Python file, for example, mouse_to_vjoy.py.
Write the Script:

Copy and paste the following script into your Python file:
python

import pyvjoy
import pyautogui
import time

# Initialize vJoy device

j = pyvjoy.VJoyDevice(1) # Assuming device ID 1

# Get screen size to normalize mouse position

screen_width, screen_height = pyautogui.size()

# Function to normalize mouse position to vJoy axis range

def normalize(value, max_value):
return int((value / max_value) \* 0x8000) # Normalized to 0-32767

try:
while True: # Get current mouse position
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

4. Run the Script
   Navigate to Your Project Directory (if not already there):

Ensure you are in the directory where mouse_to_vjoy.py is located.
Run the Script:

Execute the script using Python:
bash

python mouse_to_vjoy.py
Test the Output:

Move your mouse to see how the joystick's X and Y axes respond. You can use the vJoy Monitoring tool to see the joystick's input values in real-time.

5. Deactivating the Virtual Environment
   When you're done, you can deactivate the virtual environment by running:
   bash

venv/Scripts/deactivate

**//Berikut adalah penjelasan mengenai kegunaan masing-masing library yang digunakan dalam script tersebut:**

1. pyvjoy

Kegunaan:

pyvjoy adalah library Python yang menyediakan antarmuka untuk berinteraksi dengan vJoy, yaitu driver virtual joystick. Library ini memungkinkan Anda untuk mengontrol perangkat joystick virtual, termasuk mengatur posisi sumbu dan status tombol.
Fungsi Utama dalam Script:

pyvjoy.VJoyDevice(1): Membuat instance perangkat vJoy dengan ID 1 (ID perangkat vJoy bisa diubah sesuai kebutuhan).
j.set_axis(pyvjoy.HID_USAGE_X, joy_x): Mengatur posisi sumbu X pada joystick virtual sesuai dengan nilai joy_x.
j.set_axis(pyvjoy.HID_USAGE_Y, joy_y): Mengatur posisi sumbu Y pada joystick virtual sesuai dengan nilai joy_y.

2. pyautogui

Kegunaan:

pyautogui adalah library Python yang memungkinkan Anda untuk mengontrol dan memanipulasi mouse dan keyboard secara otomatis. Library ini sering digunakan untuk automasi GUI dan pengujian perangkat lunak.
Fungsi Utama dalam Script:

pyautogui.position(): Mengambil posisi mouse saat ini. Ini digunakan untuk mendapatkan koordinat X dan Y dari posisi mouse yang kemudian dipetakan ke sumbu joystick.

3. time

Kegunaan:

time adalah library standar Python yang menyediakan berbagai fungsi terkait waktu. Dalam konteks ini, time.sleep() digunakan untuk menambahkan jeda antara pembacaan posisi mouse dan pembaruan sumbu joystick.
Fungsi Utama dalam Script:

time.sleep(0.01): Menambahkan delay singkat (0.01 detik) di antara pembaruan posisi joystick untuk mengurangi penggunaan CPU dan memastikan bahwa skrip tidak berjalan terlalu cepat.

4. Ringkasan Kegunaan Library dalam Script

pyvjoy: Untuk berinteraksi dengan perangkat joystick virtual dan mengatur sumbu joystick.

pyautogui: Untuk mendapatkan posisi mouse saat ini.

time: Untuk menambahkan delay antara pembacaan mouse dan pembaruan joystick agar prosesnya lebih efisien.

Dengan memanfaatkan library-library ini, Anda dapat membuat skrip yang secara otomatis mengubah gerakan mouse menjadi input joystick untuk digunakan dalam aplikasi yang mendukung joystick virtual.

**//kenyataan bahwa venv itu direktorinya tidak boleh dipindah secara langsung dengan cara manual karena di dalam konfigurasinya itu dia merujuk ke direktori dimana venv dibuat.**

cara terbaik misal ada keperluan untuk memindah venv, lebih baik untuk memmbuat venv baru.

**//kenyataan bahwa untuk menjalankan suatu program pada venv tertentu pastikan di terminalnya ada tulisan (venv) kalau tidak, program akan dijalankan di env defaultnya**

intinya untuk menjalankan program harus di terminal dengan awalan (venv) /<PATH>
