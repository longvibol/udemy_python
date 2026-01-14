import cv2
import time
import os

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Open webcam (WORKING setup for Windows 11)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)

# Create output folder
os.makedirs("faces", exist_ok=True)

print("Press S to save photo | Press Q to quit")

while True:
    ok, frame = cap.read()
    if not ok:
        print("Camera read failed")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:
        # Make square box
        size = max(w, h)
        cx, cy = x + w // 2, y + h // 2

        x1 = max(cx - size // 2, 0)
        y1 = max(cy - size // 2, 0)
        x2 = min(x1 + size, frame.shape[1])
        y2 = min(y1 + size, frame.shape[0])

        # Draw square
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Save face when pressing S
        if cv2.waitKey(1) & 0xFF == ord("s"):
            face_img = frame[y1:y2, x1:x2]
            filename = f"faces/face_{int(time.time())}.jpg"
            cv2.imwrite(filename, face_img)
            print(f"Saved: {filename}")

    cv2.imshow("Square Face Capture", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
