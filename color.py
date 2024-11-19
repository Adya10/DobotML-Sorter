import cv2
import numpy as np

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

def main():
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

if __name__ == "__main__":
    color = main()
    print(f"Final Detected Color: {color}")