import cv2
import os
import time
import requests
import devices

server_name = "AMANPAVILION.local"  # Server hostname or IP address
url = f"http://{server_name}:6500/process"
devices.setup()


try:
    while True:
        os.system("raspistill -t 1000 -n -o image.jpg")   # Capture image using and save it in 'image.jpg'
        with open("image.jpg", 'rb') as img_file:
            files = {'img': img_file}
            response = requests.post(url, files=files)

        if response.ok:
            result = response.json()['result']
            print("Server says:", result)
            
            if result == 'Open':
                devices.toggleLED(17) # Red LED
            
            elif result == 'OK':
                devices.toggleLED(18) # Green LED
                
            elif result == 'Pointer':
                devices.toggleFan(27) # Fan
                
            elif result == 'Close':
                devices.toggleLED(22) # Red LED
            
        else:
            print("Failed to send image")
        
            
        time.sleep(5)
    
except KeyboardInterrupt:
    print("Exiting gracefully")
        
finally:
    devices.cleanup()
        
        




