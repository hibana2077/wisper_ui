FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    ffmpeg \
    curl

WORKDIR /app

# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install setuptools-rust

COPY . .

EXPOSE 8501

# python -m streamlit run Home.py --server.enableCORS=false --server.enableXsrfProtection=false
CMD ["streamlit", "run", "app.py", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]