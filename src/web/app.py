import streamlit as st
import numpy as np
import pandas as pd
import whisper

MODEL_SIZE_LIST = ["tiny", "base", "small", "medium", "large"]

@st.cache_resource
def load_model(size):
    return whisper.load_model(size)

@st.cache_data
def convert_to_dataframe(result):
    df = pd.DataFrame(result["words"])
    df["start_time"] = df["start_time"].apply(lambda x: round(x, 2))
    df["end_time"] = df["end_time"].apply(lambda x: round(x, 2))
    return df.to_csv().encode("utf-8")

st.title("AI 語音轉逐字稿")

model_size = st.selectbox("選擇模型大小", MODEL_SIZE_LIST)
model = load_model(model_size)

audio_file = st.file_uploader("上傳音訊檔案", type=["mp3", "wav", "ogg"])

if audio_file:
    # convert to numpy array
    audio_bytes = audio_file.read()
    audio_array = np.frombuffer(audio_bytes, dtype=np.int16)

    # inference
    result = model.transcribe(audio_array)

st.write(result)

if result:
    st.download_button(
        label="下載逐字稿",
        data=convert_to_dataframe(result),
        file_name="transcript.csv",
        mime="text/csv",
    )