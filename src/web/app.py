import streamlit as st
import pandas as pd
import whisper

MODEL_SIZE_LIST = ["tiny", "base", "small", "medium", "large"]

@st.cache_resource
def load_model(size):
    return whisper.load_model(size)

@st.cache_data
def convert_to_dataframe(result):
    col_name = ["start", "end", "text"]
    new_data = []
    for item in result['segments']:
        new_data.append([item["start"], item["end"], item["text"]])
    return pd.DataFrame(new_data, columns=col_name).to_csv().encode("utf-8")

st.title("AI 語音轉逐字稿")

model_size = st.selectbox("選擇模型大小", MODEL_SIZE_LIST)
model = load_model(model_size)

audio_file = st.file_uploader("上傳音訊檔案", type=["mp3", "wav", "ogg"])

if audio_file:
    file_name = audio_file.name
    # save to local
    with open(file_name, "wb") as f:
        f.write(audio_file.read())
    result = model.transcribe(file_name)
    st.write(result)
    if result:
        st.download_button(
            label="下載逐字稿",
            data=convert_to_dataframe(result),
            file_name="transcript.csv",
            mime="text/csv",
        )