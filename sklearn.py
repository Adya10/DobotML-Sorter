import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from serial.tools import list_ports
import pydobot

# ------------- Machine Learning Setup -------------
# Dataset with only red, blue, and yellow
data = [
    [255, 0, 0, 'red'], [200, 0, 0, 'red'], [150, 0, 0, 'red'], [128, 0, 0, 'red'], [220, 20, 60, 'red'],
    [0, 0, 255, 'blue'], [0, 0, 200, 'blue'], [0, 0, 150, 'blue'], [0, 128, 255, 'blue'], [0, 0, 139, 'blue'],
    [255, 255, 0, 'yellow'], [200, 200, 0, 'yellow'], [150, 150, 0, 'yellow'], [255, 255, 102, 'yellow'], [255, 223, 0, 'yellow']
]
data = np.array(data)
X = data[:, :3].astype(int)  # RGB values
y = data[:, 3]  # Labels

# Train-test split and k-NN classifier training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
accuracy = accuracy_score(y_test, knn.predict(X_test))
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# ------------- Dobot Setup -------------
available_ports = list_ports.comports()
port = available_ports[0].device
device = pydobot.Dobot(port=port, verbose=True)

# Move Dobot to initial position
device.move_to(199, 0, -9, 0, wait=False)
device.wait(100)

# ------------- Color Detection Function -------------
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

# ------------- Dobot Movement Based on Color Detection -------------
def move_dobot_based_on_color(color):
    if color == 'red':
        device.move_to(255.4482, 144.9243, 4.2280, 29.5677, wait=True)
        device.grip(False)
        device.move_to(63.5066, 200.4843, 8.7176, 83.5596, wait=True)
    elif color == 'yellow':
        device.move_to(27.4136, -284.3935, 49.2138, -64.6022, wait=True)
        device.grip(False)
        device.move_to(63.5066, 200.4843, 8.7176, 83.5596, wait=True)
    elif color == 'blue':
        device.move_to(27.4136, -284.3935, 49.2138, -64.6022, wait=True)
        device.grip(False)
        device.move_to(63.5066, 200.4843, 8.7176, 83.5596, wait=True)
    elif color == 'undefined':
        # Move to a separate position for undefined colors
        device.move_to(50, 50, 50, 0, wait=True)
        device.grip(False)
        device.move_to(63.5066, 200.4843, 8.7176, 83.5596, wait=True)

# ------------- Main Loop -------------
cap = cv2.VideoCapture(0)  # Adjust index if needed
roi_size = 100
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break
    
    # Draw ROI
    height, width, _ = frame.shape
    x1 = width // 2 - roi_size // 2
    y1 = height // 2 - roi_size // 2
    x2 = x1 + roi_size
    y2 = y1 + roi_size
    roi = frame[y1:y2, x1:x2]

    # Color detection in ROI
    avg_color = roi.mean(axis=0).mean(axis=0)
    avg_color_rgb = avg_color[:3][::-1]  # Convert BGR to RGB order
    predicted_color = knn.predict([avg_color_rgb])[0]
    
    # Display detected color
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
    cv2.putText(frame, f"Detected Color: {predicted_color}", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.imshow("Webcam Feed", frame)

    # Move Dobot based on detected color
    move_dobot_based_on_color(predicted_color)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
device.close()