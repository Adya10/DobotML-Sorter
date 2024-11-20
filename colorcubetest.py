import cv2
import numpy as np

COLOR_RANGES = {
    "blue": ((100, 150, 0), (140, 255, 255)),
    "yellow": ((20, 150, 100), (30, 255, 255)),
    "red_low": ((0, 150, 100), (10, 255, 255)),
    "red_high": ((170, 150, 100), (180, 255, 255)),
}

MIN_AREA = 1500  #Adjust for an ~80% confidence level

def detect_color_objects(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    blue_mask = cv2.inRange(hsv, COLOR_RANGES["blue"][0], COLOR_RANGES["blue"][1])
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame = process_contours(frame, blue_contours, "blue")

    yellow_mask = cv2.inRange(hsv, COLOR_RANGES["yellow"][0], COLOR_RANGES["yellow"][1])
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame = process_contours(frame, yellow_contours, "yellow")
    
    red_mask_low = cv2.inRange(hsv, COLOR_RANGES["red_low"][0], COLOR_RANGES["red_low"][1])
    red_mask_high = cv2.inRange(hsv, COLOR_RANGES["red_high"][0], COLOR_RANGES["red_high"][1])
    red_mask = cv2.bitwise_or(red_mask_low, red_mask_high)
    
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame = process_contours(frame, red_contours, "red")
    
    return frame

def process_contours(frame, contours, color_name):
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < MIN_AREA:
            continue  
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4: 
            x, y, w, h = cv2.boundingRect(contour)
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 2)
            cv2.putText(frame, f"{color_name} ({int(area)})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    return frame

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = detect_color_objects(frame)
        
        cv2.imshow("Color Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()