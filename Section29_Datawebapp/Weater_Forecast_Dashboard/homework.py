import streamlit as st
import plotly.express as px
import pandas as pd

df=pd.read_csv("happy.csv")

st.title('In Search for Happiness')

column_map = {
    "GDP": "gdp",
    "Happiness": "happiness",
    "Generosity": "generosity"
}

x_label = st.selectbox(
    "Select the data for the X-axis",
    list(column_map.keys()),
    key="x"
)

y_label = st.selectbox(
    "Select the data for the Y-axis",
    list(column_map.keys()),
    key="y"
)

x_column = column_map[x_label]
y_column = column_map[y_label]

st.subheader(f"{x_label} and {y_label}")

x=df[x_column]
y=df[y_column]

figure = px.scatter(x=x, y=y, labels={"x": x_label, "y": y_label})
st.plotly_chart(figure)