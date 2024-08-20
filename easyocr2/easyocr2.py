import easyocr  
import pyautogui  
import time  
from PIL import ImageGrab  
from screeninfo import get_monitors  

# Initialize the OCR reader (load the model into memory)  
reader = easyocr.Reader(['fa', 'en'])  

def show_monitors():  
    monitors = get_monitors()  
    for i, monitor in enumerate(monitors):  
        print(f"Monitor {i}: {monitor.width}x{monitor.height} at ({monitor.x}, {monitor.y})")  
    return monitors  

def read_text_under_mouse(selected_monitor):   
    while True:  
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

if __name__ == "__main__":  
    print("Available monitors:")  
    monitors = show_monitors()  
    
    # Allow the user to select a monitor  
    monitor_index = int(input("Select a monitor index (0 for first monitor, etc.): "))  
    
    if monitor_index < 0 or monitor_index >= len(monitors):  
        print("Invalid monitor index selected.")  
    else:  
        print(f"Starting OCR on Monitor {monitor_index}. Move your mouse to read text...")  
        try:  
            read_text_under_mouse(monitors[monitor_index])  
        except KeyboardInterrupt:  
            print("Stopping OCR.")