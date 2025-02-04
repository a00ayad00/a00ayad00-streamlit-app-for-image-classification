FROM python:3.11.10-slim

RUN apt update -y && apt install awscli -y && pip install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app.py"]