import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px

connection = sqlite3.connect("temdatabase.db")
cursor = connection.cursor()

cursor.execute("SELECT date, tem FROM temperature")
rows = cursor.fetchall()

# Create DataFrame from SQL result
df = pd.DataFrame(rows, columns=["date", "temperature"])

# | date                | temperature |
# | ------------------- | ----------- |
# | 2026-01-19-15-07-14 | 18          |
# | 2026-01-19-15-07-16 | 18          |
# | 2026-01-19-15-07-18 | 18          |
#

st.title("Temperature")

# Plot line chart
fig = px.line(df, x="date", y="temperature")

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Temperature (°C)",
)

fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig)
