import streamlit as st
import pandas as pd
import torch
import whisper

# check gpu memory size
GPU_MEMORY_SIZE = torch.cuda.get_device_properties(0).total_memory / 1024 ** 3
MODEL_MEM_REQ_DICT = {
    "tiny": 0.5,
    "base": 1.5,
    "small": 2.5,
    "medium": 8,
    "large": 12,
}
MODEL_SIZE_LIST = [key for key, value in MODEL_MEM_REQ_DICT.items() if value < GPU_MEMORY_SIZE]

@st.cache_resource
def load_model(size):
    return whisper.load_model(size)

@st.cache_data
def convert_to_dataframe(result):
    col_name = ["start", "end", "text"]
    new_data = []
    for item in result['segments']:
        new_data.append([item["start"], item["end"], item["text"]])
    return pd.DataFrame(new_data, columns=col_name)

st.title("AI 語音轉逐字稿")

st.markdown("""![OpenAI](https://img.shields.io/badge/OpenAI-Wisper-412991?style=plastic-square&logo=OpenAI) ![OpenAI](https://img.shields.io/badge/OpenAI-Wisper-412991?style=plastic-square&logo=OpenAI) ![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-FF4B4B?style=plastic-square&logo=Streamlit)""")
st.write("""這是一個使用 OpenAI 的 Whisper 模型來進行語音轉逐字稿的網頁應用程式。""")
st.write("""Whisper 是一個基於 Transformer 的端對端語音轉文字模型，可以將語音檔案轉換成逐字稿。""")


st.write(f"GPU 記憶體大小: {GPU_MEMORY_SIZE:.2f} GB")
with st.expander("為什麼有些模型無法選擇?"):
    st.write('''
    由於 Whisper 模型需要大量的 GPU 記憶體，因此本應用程式會根據您的 GPU 記憶體大小來過濾掉無法運行的模型。
    ''')
    st.image("https://www.groovypost.com/wp-content/uploads/2022/12/gpu-graphics-card-featured.jpg", use_column_width=True)

st.divider()

model_size = st.selectbox("選擇模型大小", MODEL_SIZE_LIST)
model = load_model(model_size)

audio_file = st.file_uploader("上傳音訊檔案", type=["mp3", "wav", "ogg"])

if audio_file:
    file_name = audio_file.name
    # save to local
    with open(file_name, "wb") as f:
        f.write(audio_file.read())
    result = model.transcribe(file_name)
    st.write(result['text'])
    if result:
        st.dataframe(convert_to_dataframe(result).iloc[:15])
        st.download_button(
            label="下載逐字稿",
            data=convert_to_dataframe(result).to_csv().encode("utf-8"),
            file_name="transcript.csv",
            mime="text/csv",
        )