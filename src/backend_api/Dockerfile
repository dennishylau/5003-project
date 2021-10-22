
# FROM python:3.9
FROM continuumio/miniconda3:4.10.3p0

ENV BASH_ENV ~/.bashrc
ENV PYTHONPATH=/app

SHELL ["/bin/bash", "-c"]

# install java
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
# install scala
RUN wget https://downloads.lightbend.com/scala/2.12.3/scala-2.12.3.deb
RUN dpkg -i scala-2.12.3.deb
# install via conda
COPY environment.yml environment.yml
RUN conda init
RUN conda env create -f environment.yml
RUN echo "conda activate 5003-project" >> ~/.bashrc
RUN conda activate 5003-project
# copy local files
COPY src/backend_api/gunicorn.conf.py gunicorn.conf.py
COPY src/backend_api/start.sh start.sh
RUN chmod +x /start.sh
COPY src/backend_api/start-reload.sh start-reload.sh
RUN chmod +x /start-reload.sh

WORKDIR /app/

COPY src/backend_api/app /app

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]