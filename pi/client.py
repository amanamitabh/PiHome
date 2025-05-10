import os
import time
import requests
import devices
from dotenv import load_dotenv

# Automatically load .env file in the current directory
load_dotenv()

# Get the server name from environment variables
server_name = os.getenv("SERVER_NAME")

# URL to send the image for processing
url = f"http://{server_name}:6500/process"

# Initialize devices
devices.setup()

try:
    while True:
        #os.system("libcamera-still -t 1000 -n -o image.jpg")
        # FOR NON-LEGACY CAMERAS, USE THE ABOVE LINE AND COMMENT THE LINE BELOW
        os.system("raspistill -t 1000 -n -o image.jpg")

         # Read the captured image in binary mode for sending it to the server for processing via POST request
        with open("image.jpg", 'rb') as img_file:
            files = {'img': img_file}
            response = requests.post(url, files=files)

        # Check if the server processed the image successfully and extract result
        if response.ok:
            result = response.json()['result']
            print("Server says:", result)
            
            # Assign hand gestures to devices on GPIO pins
            if result == 'Open':
                devices.toggleLED(17)
            
            elif result == 'OK':
                devices.toggleLED(18) 
                
            elif result == 'Pointer':
                devices.toggleFan(27)
                
            elif result == 'Close':
                devices.toggleLED(22)
            
        else:
            print("Failed to send image")
        
        # Delay between image captures
        time.sleep(3)
    
except KeyboardInterrupt:
    print("Exiting gracefully")
        
finally:
    # Cleanup GPIO pins before exiting program
    devices.cleanup()