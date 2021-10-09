
# FROM python:3.9
FROM continuumio/miniconda3:4.10.3p0

ENV BASH_ENV ~/.bashrc
ENV PYTHONPATH=/app

SHELL ["/bin/bash", "-c"]

COPY environment.yml environment.yml
COPY requirements.txt requirements.txt
COPY gunicorn.conf.py gunicorn.conf.py
COPY start.sh start.sh
COPY start-reload.sh start-reload.sh

RUN conda init
RUN conda env create -f environment.yml
RUN echo "conda activate 5003-project" >> ~/.bashrc
RUN conda activate 5003-project
RUN pip install --no-cache -r requirements.txt

WORKDIR /app/

COPY ./app /app

RUN chmod +x /start.sh
RUN chmod +x /start-reload.sh

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]