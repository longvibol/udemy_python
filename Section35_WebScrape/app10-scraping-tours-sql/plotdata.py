import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("home.txt")

st.title("Temperature")

dates = df["date"].tolist()
temperatures = df["temperature"].tolist()

print(temperatures)

fig = px.line(df, x="date", y="temperature",color_discrete_sequence=["red"])

# ✅ Change axis text + rotate + format
fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Temperature (°C)",
)

fig.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(fig)
