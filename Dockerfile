FROM ubuntu:22.04
RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

WORKDIR /data
COPY . .
COPY keveraertml6-0a444efd8235.json .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]