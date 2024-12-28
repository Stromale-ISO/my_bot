FROM python:3.11.11

WORKDIR /usr/src/app

COPY . .

RUN apt update && apt install -y --no-install-recommends python3-pip && \
    pip install --no-cache-dir -r requirements.txt



CMD ["python", "main.py"]