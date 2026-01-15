import cv2
import time

import numpy as np

from emailing import send_email

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)

first_frame =  None
status_list = []

while True:
    status = 0
    # Read the frame
    check, frame = video.read()

    #1 Convert to Gray Color
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #2 Gaussian to make the effective
    gray_frame_gau = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    #3 Create threshold
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    #4 smoother the image
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Create contours about the object (around the white area)

    contours ,check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # if it is the face object we continue to the loop again
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email()

    print(status_list)

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()



