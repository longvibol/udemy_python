import glob
import streamlit as st
import plotly.express as px

from nltk.sentiment import SentimentIntensityAnalyzer
from numpy.ma.core import negative

# Create filepath from the folder and sort the file
filepaths = sorted(glob.glob('diary/*.txt'))

analyzer = SentimentIntensityAnalyzer()

st.title("Sentiment Intensity Analyzer")

negative = []
positive = []

for filepath in filepaths:
    with open(filepath) as file:
        content = file.read()
    scores = analyzer.polarity_scores(content)
    positive.append(scores['pos'])
    negative.append(scores['neg'])


# extrac the data from the file name : 'diary\\2023-10-22.txt'
dates = [name.strip(".txt").strip("diary\\") for name in filepaths]

st.title("Diary Tone")
st.subheader("Positive")

pos_fig = px.line(x=dates, y=positive, labels={"x": "Date", "y": "Positive"})
st.plotly_chart(pos_fig)

st.subheader("Negative")
neg_fig = px.line(x=dates, y=negative, labels={"x": "Date", "y": "Negative"})
st.plotly_chart(neg_fig)


