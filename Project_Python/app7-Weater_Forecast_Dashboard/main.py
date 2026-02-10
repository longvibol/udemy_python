import streamlit as st
import plotly.express as px
from backend import get_data

st.title('Weather Forecast for the Next Days')
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecast days")

option = st.selectbox("Select date to view", ("Temperature","Sky"))

st.subheader(f"{option} for the next {days} days in {place}")

if place:
    # Get the temperature/sky data
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperature = [dict['main']['temp'] for dict in filtered_data]
            temperature = [round(temp - 273.15) for temp in temperature]

            dates = [dict["dt_txt"] for dict in filtered_data]
            # create temperature plot
            figure = px.line(x = dates, y = temperature, labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            images = {"Clear":"images/clear.png","Clouds":"images/cloud.png",
                      "Rain":"images/rain.png","Snow":"images/snow.png"}
            sky_conditions = [dict['weather'][0]['main'] for dict in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            # print(image_paths)
            st.image(image_paths,width=115)
    except KeyError:
        st.text("Place doesn't exist")