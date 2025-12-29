import streamlit as st
from PIL import Image


with st.expander("Camera App"):
    # start the camera
    camera_img=st.camera_input("Camera")

if camera_img:
    # Create a pillow image instance
    img = Image.open(camera_img)

    # Convert img to grayscale
    gray_img = img.convert("L")

    #Render the image to the webpage
    st.image(gray_img)

