#in this project a machine learning module was implemented ona dodbot arm 
#to detect the color of the boxes so that it can move the boxes based on that color
#to a fixed position and on a spicifed order 

#---------------------------------------------------------------------------------------
#first thing the dobot arm holdes the box and take it to a fixed place where the camera can see
#it so it can detect the color of it then after than the arm takes the box to a specifed position
#for that color.
#
#
#
#---------------------------------------------------------------------------------------
from serial.tools import list_ports
import pydobot      #for dobot
import cv2          #for color detecction
import speech_recognition as sr
import pyttsx3
#----------------------to turn the camera on-----------------------

cap = cv2.VideoCapture(2)
Whatcolor = 'white'
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#---------------------Voice Recognition Section---------------------
def Voice_recognition():
    r = sr.Recognizer()
    def SpeakText(command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()
    MyText = "NA"
    v_color = 'NA'
    print('say your color')
    with sr.Microphone() as source2:
        r = sr.Recognizer()

        r.adjust_for_ambient_noise(source2, duration=0.2)


        audio2 = r.listen(source2)

        MyText = r.recognize_google(audio2)

        MyText = MyText.lower()
        if 'red' in MyText:
            v_color = 'red'
        elif 'green' in MyText:
            v_color = 'green'
        elif 'blue' in MyText:
            v_color = 'blue'
        elif 'yellow' in MyText:
            v_color = 'yellow'
        elif 'orange' in MyText:
            v_color = 'orange'
        elif 'violet' in MyText:
            v_color = 'violet'
        elif 'stop' in MyText:
            v_color = 'stop'
            
        return v_color
#-------------------------------------------------------------------
#---------------------Color Detection section-----------------------
def color_detection(color):
    

    while True:
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape

        cx = int(width / 2)
        cy = int(height / 2)

        # Pick pixel value
        pixel_center = hsv_frame[cy, cx]
        hue_value = pixel_center[0]

        color = "Undefined"
        Whatcolor = color
        if hue_value < 5:
            color = "RED"
        
        elif hue_value < 22:
            color = "ORANGE"

        elif hue_value < 33:
            color = "YELLOW"
        
        elif hue_value < 78:
            color = "GREEN"
        
        elif hue_value < 131:
            color = "BLUE"
        
        elif hue_value < 170:
            color = "VIOLET"
        
        else:
            color = "Empty"
        
        break
    return color
#---------------------End of color section-------------------------
#---------------------Dobot Section -------------------------------
available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[3].device

device = pydobot.Dobot(port=port, verbose=True)
(x, y, z, r, j1, j2, j3, j4) = device.pose()
print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
#------------------------------------------------------------------
#homing place
device.move_to(199, 0, -9, 0, wait=False)
device.wait(100)

#--------------------------------
#To make the Hand grip the box
#this line is to make the hand take the box from the it fixed position
device.move_to(9.8151, 189.5203, 6, 87.6613, wait=True) # initial postion to just above the box
device.grip(False)
device.wait(1000)
device.move_to(4.6536, 179.8364, -26.2896, 88.5177, wait=True) # to hold the box
device.grip(True)
device.move_to(7.3677, 270.2359, 3.6315, 88.4383, wait=True) # camera position
#--------------------------------

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
    #elif value == 'stop':
    #    print("Bye")
    #    device.close()
    #    break



#-------------------------End of Dobot section---------------------