import glob
import os
import time
from threading import Thread

import cv2

from cleanfuntion import clean_folder
from emailing import send_email

# --- Helpers ---
def send_email_safe(image_path: str):
    """Send email and print the real result (success/fail)."""
    try:
        send_email(image_path)
        print(f"✅ Email actually sent with image: {image_path}")
    except Exception as e:
        print("❌ Email failed:", repr(e))


# --- Camera ---
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)

first_frame = None
status_list = [0, 0]   # keep only last 2 statuses safely
count = 1

# ensure folder exists
os.makedirs("images", exist_ok=True)

# cooldown: minimum seconds between emails (avoid spamming)
COOLDOWN_SECONDS = 10
last_email_time = 0

while True:
    status = 0

    check, frame = video.read()
    if not check:
        time.sleep(0.1)
        continue

    # 1) Gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2) Blur
    gray_frame_gau = cv2.GaussianBlur(gray, (21, 21), 0)

    # Store first frame once (background reference)
    if first_frame is None:
        first_frame = gray_frame_gau
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) == ord("q"):
            break
        continue

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # 3) Threshold
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # 4) Dilate
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Contours
    contours, _ = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue

        status = 1  # motion/object detected

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Save frames while motion is happening
        cv2.imwrite(f"images/{count}.png", frame)
        count += 1

    # Keep only last 2 statuses
    status_list.append(status)
    status_list = status_list[-2:]

    # Motion ended (1 -> 0)
    if status_list[0] == 1 and status_list[1] == 0:
        now = time.time()

        # Cooldown check
        if now - last_email_time >= COOLDOWN_SECONDS:
            all_images = sorted(glob.glob("images/*.png"))
            if all_images:
                middle_index = len(all_images) // 2
                image_with_object = all_images[middle_index]

                email_thread = Thread(target=send_email_safe, args=(image_with_object,), daemon=True)
                clean_thread = Thread(target=clean_folder, daemon=True)

                email_thread.start()
                clean_thread.start()

                last_email_time = now
            else:
                print("⚠️ No images found to send.")
        else:
            print("⏳ Cooldown active - skipping email to avoid spam.")

        # Reset counter for next event
        count = 1

        # Reset background so motion can end cleanly next time
        first_frame = None

    print("status_list:", status_list)

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
