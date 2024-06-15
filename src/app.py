import streamlit as st
import pandas as pd
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.mp3")
st.write(result)