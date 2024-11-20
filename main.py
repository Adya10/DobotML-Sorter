from serial.tools import list_ports
import pydobotplus
import time
import cv2
import numpy as np
import pywhatkit

port = list_ports.comports()[3].device # list port and connect
device = pydobotplus.Dobot(port=port) # define port

# start position
# device.clear_alarms()
# device.home()
# device.move_to(x=229.7577362060547, y=-8.920731544494629, z=76.87593078613281, r=-28.777681350708008) # home position
# device._set_end_effector_gripper(enable=True) # close gripper
pose = device.get_pose() # get position
print(pose)

def color_recognition():
    COLOR_RANGES = {
        "blue": ((100, 150, 0), (140, 255, 255)),
        "yellow": ((20, 150, 100), (30, 255, 255)),
        "red_low": ((0, 150, 100), (10, 255, 255)),
        "red_high": ((170, 150, 100), (180, 255, 255)),
    }

    MIN_AREA = 1500  # Adjust for an ~80% confidence level

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

    def process_contours(contours, color_name):
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= MIN_AREA:
                return True  # Detected color with sufficient area
        return False

    
    cap = cv2.VideoCapture(0)
    detected_color = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detected_color = detect_color_objects(frame)
        if detected_color:
            print(f"Detected Color: {detected_color}")
            break

        cv2.imshow("Color Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return detected_color

def coveyor():
    device.conveyor_belt(speed=0.5, direction=1)
    device.conveyor_belt_distance(speed_mm_per_sec=100, distance_mm=200, direction=1)
    print(device.get_ir(port=1))

def red():
    # move to conve
    device.move_to(x=-21.18318748474121, y=-286.0504455566406, z=63.0224723815918, r=-120.78944396972656)
    device._set_end_effector_gripper(enable=False) # open gripper
    time.sleep(0.5)
    device.move_to(x=-21.18318748474121, y=-286.0504455566406, z=33.0224723815918, r=-120.78944396972656)
    device._set_end_effector_gripper(enable=True) # close gripper
    time.sleep(0.5)
    device.move_to(x=-21.18318748474121, y=-286.0504455566406, z=63.0224723815918, r=-120.78944396972656)

    # move red obj
    device.move_to(x=-94.33621215820312, y=246.54771423339844, z=-18.039230346679688, r=84.38408660888672)
    device._set_end_effector_gripper(enable=False) # open gripper
    time.sleep(0.5)
    device.move_to(x=-94.33621215820312, y=246.54771423339844, z=18.039230346679688, r=84.38408660888672)
    time.sleep(0.5)
    device._set_end_effector_gripper(enable=True) # close gripper
    device.move_to(x=229.7577362060547, y=-8.920731544494629, z=76.87593078613281, r=-28.777681350708008)

def yellow():
    # move to conve
    device.move_to(x=-21.18318748474121, y=-286.0504455566406, z=63.0224723815918, r=-120.78944396972656)
    device._set_end_effector_gripper(enable=False) # open gripper
    time.sleep(0.5)
    device.move_to(x=-21.18318748474121, y=-286.0504455566406, z=33.0224723815918, r=-120.78944396972656)
    device._set_end_effector_gripper(enable=True) # close gripper
    time.sleep(0.5)
    device.move_to(x=-21.18318748474121, y=-286.0504455566406, z=63.0224723815918, r=-120.78944396972656)

    # move yellow obj
    device.move_to(x=154.1808624267578, y=201.44615173339844, z=-16.757827758789062, r=26.016435623168945)
    device._set_end_effector_gripper(enable=False) # open gripper
    time.sleep(0.5)
    device.move_to(x=154.1808624267578, y=201.44615173339844, z=16.757827758789062, r=26.016435623168945)
    time.sleep(0.5)
    device._set_end_effector_gripper(enable=True) # close gripper
    device.move_to(x=229.7577362060547, y=-8.920731544494629, z=76.87593078613281, r=-28.777681350708008)

def blue():
 # move to conve
    device.move_to(x=-21.18318748474121, y=-286.0504455566406, z=63.0224723815918, r=-120.78944396972656)
    device._set_end_effector_gripper(enable=False) # open gripper
    time.sleep(0.5)
    device.move_to(x=-21.18318748474121, y=-286.0504455566406, z=33.0224723815918, r=-120.78944396972656)
    device._set_end_effector_gripper(enable=True) # close gripper
    time.sleep(0.5)
    device.move_to(x=-21.18318748474121, y=-286.0504455566406, z=63.0224723815918, r=-120.78944396972656)

    # move blue obj
    device.move_to(x=23.042776107788086, y=255.08580017089844, z=-19.236053466796875, r=58.284088134765625)
    device._set_end_effector_gripper(enable=False) # open gripper
    time.sleep(0.5)
    device.move_to(x=23.042776107788086, y=255.08580017089844, z=19.236053466796875, r=58.284088134765625)
    time.sleep(0.5)
    device._set_end_effector_gripper(enable=True) # close gripper
    device.move_to(x=229.7577362060547, y=-8.920731544494629, z=76.87593078613281, r=-28.777681350708008)


def API():
    # mobile_num = '+4915734553894' # contact number
    # imgPath = 'jq2kktmfx9ra1.jpg' # save imag path
    # caption = 'John Pork 2' # message
    # pywhatkit.sendwhats_image(mobile_num, imgPath, caption, 7) # send image and message
    print('Code not ready yet')


detected_color = color_recognition()
if detected_color == 'red':
    red()

elif detected_color == 'yellow':
    yellow()

elif detected_color == 'blue':
    blue()

else: 
    API()
    
