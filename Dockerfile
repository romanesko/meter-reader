FROM python:3.12-slim


COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY src .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENV PROFILE=docker

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]