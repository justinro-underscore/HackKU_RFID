import RPi.GPIO as GPIO
import time
from evdev import InputDevice, ecodes

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)

def get_input():
    try:
        dev = InputDevice('/dev/input/event0')

        input_str = ""
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:
                if event.code == 28:
                    return input_str
                code = event.code - 1
                if code == 10:
                    code = 0
                input_str += str(code)
    except Exception as e:
        f = open("test_error.txt", "w")
        f.write(str(e) + "\n")
        f.close()

rfid = get_input()
for i in range(len(rfid)):
    num = int(rfid[i])
    for _ in range(num):
        GPIO.output(23, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(23, GPIO.LOW)
        time.sleep(0.1)
    time.sleep(0.3)

GPIO.cleanup()
