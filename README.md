# 5003 Project

- [5003 Project](#5003-project)
  - [Getting Started](#getting-started)
    - [Env Info](#env-info)
    - [Prerequisite](#prerequisite)
    - [Steps](#steps)
  - [Managing Conda Environment](#managing-conda-environment)
  - [Start Dev Servers](#start-dev-servers)
  - [Docker Compose](#docker-compose)
  - [Example Files](#example-files)
  - [Additional Setup](#additional-setup)
    - [Pytest](#pytest)
  - [Credentials](#credentials)
    - [Notebook](#notebook)
    - [TimescaleDB](#timescaledb)
  - [Additional Docs](#additional-docs)
  - [Troubleshoot](#troubleshoot)

## Getting Started

### Env Info

- Python version: 3.9.7  
- Code formatter: autopep8
- Spark: 3.1.2
  - Hadoop: 3.2.0
  - Scala: 2.12
  - py4j: 0.10.9

### Prerequisite

- Docker Desktop: [link](https://docs.docker.com/get-docker/)
  - You may have to go to Preferences > Resources to increase memory.  
  Recommend > 6GB.
- Conda: [link](https://docs.anaconda.com/anaconda/install/index.html)

### Steps

1. Git clone and `cd 5003-project`.
2. Duplicate `.env.example` and rename it to `.env`, update the credentials inside if needed  
(Tip: if you can't find the file, try opening the folder with an IDE)
3. Update `KAFKA_CONNECTION_STRING`, `KAFKA_TOPIC_NAME` and `ENV` in `.env` accordingly.
   1. If `ENV` is not set or is `dev`, the ingestor will send messages to the local dockerized kafka broker.
   2. [Optional] To send messages to cloud endpoint (Azure Event Hubs), simply update `KAFKA_CONNECTION_STRING`, and set `ENV` to `prod`
4. Run `docker compose pull`
5. Run `docker compose up` to start services.
6. Run `docker compose down` to stop the services.

## Managing Conda Environment

- Create conda environment with packages: `conda env create -f environment.yml`  
- Activate conda environment: `conda activate 5003-project`  
- Export conda package list: `conda env export --no-builds --from-history > environment.yml`  

## Start Dev Servers  

1. cd to project root
2. API
   1. Call `uvicorn src.backend_api.app.main:app --reload --env-file=".env" --app-dir="src/backend_api/app"`
   2. Access docs at `http://127.0.0.1:8000/latest/docs`
3. Notebook
   1. Call `jupyter-lab --config=/jupyter_lab_config.py`
   2. Access at `http://127.0.0.1:9999/`

## Docker Compose

- Running in local: `docker compose up`  
  - API Docs: [http://localhost:80/latest/docs](http://localhost:80/latest/docs)  
  - Notebook: [http://localhost:8888/lab?token=5003-project](http://localhost:8888/lab?token=5003-project)  
  - TimescaleDB: `localhost:5432`  
  - Spark master node (Pyspark endpoint): `localhost:7077`  
  - Spark master node (WebUI): [http://localhost:8080/](http://localhost:8080/)  
  - Grafana: [http://localhost:3000/](http://localhost:3000/)  

- Running in local with rebuild: `docker compose up --build`  
- Interactive shell for debugging: `docker compose up && docker-compose run backend-api sh`

## Example Files

Example notebooks can be found in the `notebook` directory

## Additional Setup

### Pytest

- Config at `setup.cfg`

## Credentials

### Notebook

- Token: 5003-project

### TimescaleDB

- DB Name: 5003-project-dev  
- Username: postgres  
- Password: 5003-project  

## Additional Docs

- Grafana provisioning: <https://grafana.com/tutorials/provision-dashboards-and-data-sources/>

## Troubleshoot

- Question: TimescaleDB keeps complaining about `WARNING:  could not open statistics file "pg_stat_tmp/global.stat": Operation not permitted`
  - Answer: This is a known problem documented in Postgres' official docker hub page. In short, it does not affect operation, and can be safely ignored.
