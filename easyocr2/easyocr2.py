import easyocr
import pyautogui
import time
from PIL import ImageGrab
from screeninfo import get_monitors
import tkinter as tk
from tkinter import messagebox, Entry, Label, Button
import threading

# Initialize the OCR reader (load the model into memory)
reader = easyocr.Reader(['fa', 'en'])

# Global variable to control the OCR loop
running = False

def show_monitors():
    monitors = get_monitors()
    for i, monitor in enumerate(monitors):
        print(f"Monitor {i}: {monitor.width}x{monitor.height} at ({monitor.x}, {monitor.y})")
    return monitors

def read_text_under_mouse(selected_monitor):
    global running
    while running:
        # Get the current mouse position
        x, y = pyautogui.position()

        # Check if the mouse is within the selected monitor's boundaries
        monitor = selected_monitor
        if (monitor.x <= x < monitor.x + monitor.width) and (monitor.y <= y < monitor.y + monitor.height):
            # Take a screenshot of a small area around the mouse cursor (e.g., 100x50 pixels)
            bbox = (x - 50, y - 25, x + 50, y + 25)  # Define the region to capture
            screenshot = ImageGrab.grab(bbox)

            # Save the screenshot as a JPEG file
            screenshot_path = 'screenshot.jpg'
            screenshot.save(screenshot_path)

            # Use EasyOCR to read the text within the captured image
            result = reader.readtext(screenshot_path)

            # Print the results
            for (bbox, text, prob) in result:
                print(f"Detected text: {text} (Confidence: {prob:.2f})")

        time.sleep(0.01)  # Sleep for 0.01 seconds (10 ms)

def start_ocr():
    global running
    if running:
        messagebox.showwarning("Warning", "OCR is already running!")
        return

    try:
        monitor_index = int(monitor_input.get())
        monitors = show_monitors()
        
        if monitor_index < 0 or monitor_index >= len(monitors):
            messagebox.showerror("Error", "Invalid monitor index selected.")
            return

        selected_monitor = monitors[monitor_index]
        running = True
        threading.Thread(target=read_text_under_mouse, args=(selected_monitor,), daemon=True).start()
        messagebox.showinfo("Info", "OCR started. Move your mouse to read text.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid monitor index.")

def stop_ocr():
    global running
    running = False
    messagebox.showinfo("Info", "OCR stopped.")

# GUI Setup
root = tk.Tk()
root.title("OCR Application")

monitor_label = Label(root, text="Select Monitor Index:")
monitor_label.pack(pady=10)

monitor_input = Entry(root)
monitor_input.pack(pady=10)

start_button = Button(root, text="Start OCR", command=start_ocr)
start_button.pack(pady=10)

stop_button = Button(root, text="Stop OCR", command=stop_ocr)
stop_button.pack(pady=10)

root.mainloop()