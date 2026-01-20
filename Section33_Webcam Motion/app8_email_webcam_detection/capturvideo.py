import cv2
import streamlit as st
from datetime import datetime

st.title("Motion Detector")
start = st.button("Start")


if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        check, frame = camera.read()

        if not check:
            break

        # covert fto RGB color
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        now = datetime.now()
        current_day = now.strftime("%A")
        current_time = now.strftime("%H:%M:%S")

        cv2.putText(img=frame, text=current_day, org=(10, 50),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 255, 255),
                    thickness=1, lineType=cv2.LINE_AA)

        cv2.putText(img=frame, text=current_time, org=(10, 100),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(250, 0, 0),
                    thickness=1, lineType=cv2.LINE_AA)

        streamlit_image.image(frame)