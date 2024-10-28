FROM python:3.11-slim-buster

# # Necessary 
# RUN apk add gcc g++ libffi-dev musl-dev \
#     && python -m pip install --no-cache-dir brotlipy \
#     && apk del gcc g++ libffi-dev musl-dev

WORKDIR /app

COPY requirements.txt .

RUN ls -al 
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

COPY app .

# EXPOSE 8501

CMD [ "streamlit", "run" , "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
