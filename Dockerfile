FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/My_Portfolio.py", "--server.port=8501", "--server.address=0.0.0.0"]
