from serial.tools import list_ports
import pydobot      #for dobot
import cv2          #for color detecction

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[3].device

device = pydobot.Dobot(port=port, verbose=True)

device.move_to(199, 0, -9, 0, wait=False)
device.wait(100)

cap = cv2.VideoCapture(1)
Whatcolor = 'white'
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def color_detection(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape
    cx, cy = width // 2, height // 2
    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]

    if hue_value < 5:
        return "red"
    elif hue_value < 22:
        return "yellow"
    elif hue_value < 131:
        return "blue"
    else:
        return "undefined"


color_value = "Undefined"
while True:
    device.wait(1000)
    device.grip(True)
    color = color_detection(color_value)
    #value = Voice_recognition()
    #print(value)
    if color == 'RED':
        device.move_to(255.4482, 144.9243, 4.2280, 29.5677, wait=True)    #take the box from here
        device.grip(False)                                                  #Hold the box
        device.wait(500)                                                    
        device.move_to(63.5066, 200.4843, 8.7176, 83.5596, wait=True)      #go to the home again        

    elif color == 'ORANGE':
        device.move_to(27.4136, -284.3935, 49.2138, -64.6022, wait=True)    
        device.grip(False)                                                  
        device.wait(500)
        device.move_to(63.5066, 200.4843, 8.7176, 83.5596, wait=True)  

    elif color == 'YELLOW':
        device.move_to(27.4136, -284.3935, 49.2138, -64.6022, wait=True)    
        device.grip(False)
        device.wait(500)
        device.move_to(63.5066, 200.4843, 8.7176, 83.5596, wait=True)  

    elif color == 'GREEN':
        device.move_to(27.4136, -284.3935, 49.2138, -64.6022, wait=True)    
        device.grip(False)
        device.wait(500)
        device.move_to(63.5066, 200.4843, 8.7176, 83.5596, wait=True)  

    elif color == 'BLUE':
        device.move_to(27.4136, -284.3935, 49.2138, -64.6022, wait=True)    
        device.grip(False)
        device.wait(500)
        device.move_to(63.5066, 200.4843, 8.7176, 83.5596, wait=True)  
        

    elif color == 'VIOLET':
        device.move_to(27.4136, -284.3935, 49.2138, -64.6022, wait=True)    
        device.grip(False)
        device.wait(500)
        device.move_to(63.5066, 200.4843, 8.7176, 83.5596, wait=True)  
        

    elif color == 'Empty':
        print("This color is not recognised")
        continue