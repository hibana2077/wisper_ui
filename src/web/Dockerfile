FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    ffmpeg \
    curl

WORKDIR /app

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
RUN echo 'source $HOME/.cargo/env' >> $HOME/.bashrc

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install setuptools-rust

COPY . .

EXPOSE 8501

# python -m streamlit run Home.py --server.enableCORS=false --server.enableXsrfProtection=false
CMD ["streamlit", "run", "app.py", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]