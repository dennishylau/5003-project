FROM python:3.9

WORKDIR /app

COPY src/data_ingestor/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/data_ingestor/ ./
RUN wget https://5003project.blob.core.windows.net/data/archive%20%282%29.zip -P /app/data/
RUN unzip /app/data/archive*.zip -d /app/data/

CMD ["python3", "ingestor.py"]