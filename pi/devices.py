import RPi.GPIO as GPIO

print("Devices Loaded")

def setup():        
    # Use BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Define the 4 LED pins
    led_pins = {
        'LED1': 17,
        'LED2': 18,
        'LED3': 22
    }
    
    # Setup all LED pins as output
    for pin in led_pins.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)  # Start with all LEDs OFF
        
    # Initialize FAN pin as output
    fan_pin = 27
    GPIO.setup(fan_pin, GPIO.OUT)
    GPIO.output(fan_pin, GPIO.HIGH) # Relay module is active LOW
    

def toggleLED(pin):
    # Toggle LED state based on previous input
    if(GPIO.input(pin)):
        GPIO.output(pin, GPIO.LOW)
        print(f"Turning LED: {pin} OFF")
    else:
        GPIO.output(pin, GPIO.HIGH)
        print(f"Turning LED: {pin} ON")
        

def toggleFan(pin):
    # Toggle Fan state based on previous input
    if(GPIO.input(pin)):
        GPIO.output(pin, GPIO.LOW)
        print(f"Turning Fan: {pin} ON")
    else:
        GPIO.output(pin, GPIO.HIGH)
        print(f"Turning Fan: {pin} OFF")


def cleanup():
    # Reset GPIO pins to default states
    GPIO.cleanup()
