import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px

connection = sqlite3.connect("temdatabase.db")
cursor = connection.cursor()

cursor.execute("SELECT date FROM temperature")
date = cursor.fetchall()
date = [item[0] for item in date]

cursor.execute("SELECT tem FROM temperature")
tem = cursor.fetchall()
tem = [item[0] for item in tem]


st.title("Temperature")

# Plot line chart
fig = px.line(x="date", y="temperature")

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Temperature (°C)",
)

fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig)
