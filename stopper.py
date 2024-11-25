from serial.tools import list_ports
import pydobotplus
import time
import cv2
import numpy as np

port = list_ports.comports()[3].device 
device = pydobotplus.Dobot(port=port)  

def start_conveyor():
    print("Conveyor started")  

def stop_conveyor():
    print("Conveyor stopped")  

def color_recognition():
    COLOR_RANGES = {
        "blue": ((100, 150, 0), (140, 255, 255)),
        "yellow": ((20, 150, 100), (30, 255, 255)),
        "red_low": ((0, 150, 100), (10, 255, 255)),
        "red_high": ((170, 150, 100), (180, 255, 255)),
    }
    MIN_AREA = 1500  

    def process_contours(contours, color):
        for contour in contours:
            if cv2.contourArea(contour) > MIN_AREA:
                return True
        return False

    def detect_color_objects(frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Check for blue
        blue_mask = cv2.inRange(hsv, COLOR_RANGES["blue"][0], COLOR_RANGES["blue"][1])
        blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if process_contours(blue_contours, "blue"):
            return "blue"

        # Check for yellow
        yellow_mask = cv2.inRange(hsv, COLOR_RANGES["yellow"][0], COLOR_RANGES["yellow"][1])
        yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if process_contours(yellow_contours, "yellow"):
            return "yellow"
        
        # Check for red (both ranges)
        red_mask_low = cv2.inRange(hsv, COLOR_RANGES["red_low"][0], COLOR_RANGES["red_low"][1])
        red_mask_high = cv2.inRange(hsv, COLOR_RANGES["red_high"][0], COLOR_RANGES["red_high"][1])
        red_mask = cv2.bitwise_or(red_mask_low, red_mask_high)
        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if process_contours(red_contours, "red"):
            return "red"
        
        return None

    frame = cv2.imread('path_to_image')  
    detected_color = detect_color_objects(frame)
    return detected_color

def handle_color(color):
    if color == 'red':
        red()
    elif color == 'yellow':
        yellow()
    elif color == 'blue':
        blue()
    else:
        API()
def red():
    stop_conveyor()
    time.sleep(2)  
    start_conveyor()

def yellow():
    stop_conveyor()
    time.sleep(2)  
    start_conveyor()

def blue():
    stop_conveyor()
    time.sleep(2)  
    start_conveyor()

def API():
    print('Code not ready yet')

while True:
    detected_color = color_recognition()
    if detected_color:
        handle_color(detected_color)
    time.sleep(0.1)  
