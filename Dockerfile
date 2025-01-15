FROM python:3.11.11

#for start system technics
RUN apt update && apt install -y --no-install-recommends \
    python3-pip python3-setuptools python3-wheel && \
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

#copy file with biblios for use docker cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["python", "main.py"]