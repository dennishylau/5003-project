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
    - [Git Hooks](#git-hooks)
    - [Pytest](#pytest)
  - [Credentials](#credentials)
    - [Notebook](#notebook)
    - [TimescaleDB](#timescaledb)

## Getting Started

### Env Info

- Python version: 3.9  
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

1. `cd 5003-project`
2. Duplicate `.env.example` and rename it to `.env`, update the credentials inside if needed  
(Tip: if you can't find the file, try opening the folder with an IDE)
3. Run `docker compose up`

## Managing Conda Environment

- Install: `conda env create -f environment.yml`  
- Activate: `conda activate 5003-project`  
- Export conda package list: `conda env export --no-builds --from-history > environment.yml`  
- Export pip package list: `pip list --format=freeze > requirements.txt`  

## Start Dev Servers  

1. cd to project root
2. API
   1. Call `uvicorn src.backend_api.app.main:app --reload --env-file=".env" --app-dir="src/backend_api/app"`
   2. Access docs at `http://127.0.0.1:8000/latest/docs`
3. Notebook
   1. Call `jupyter-lab --config=/jupyter_lab_config.py`
   2. Access at `http://127.0.0.1:8888/`

## Docker Compose

- Running in local: `docker compose up`  
  - API Docs: [http://localhost:80/latest/docs](http://localhost:80/latest/docs)  
  - Notebook: [http://localhost:8888/lab?token=5003-project](http://localhost:8888/lab?token=5003-project)  
  - TimescaleDB: `localhost:5432`  
  - Spark master node (Pyspark endpoint): `localhost:7077`  
  - Spark master node (WebUI): [http://localhost:8080/](http://localhost:8080/)  

- Running in local with rebuild: `docker compose up --build`  
- Interactive shell for debugging: `docker compose up && docker-compose run backend-api sh`

## Example Files

Example notebooks can be found in the `notebook` directory

## Additional Setup

### Git Hooks

- Set this up so no need to manually run `conda env export` and `pip freeze`
- Ensure `conda` is automatically sourced in `~/.bashrc`
- Run `git config core.hooksPath githooks` to modify the default hooks directory
- Run `chmod +x githooks/*` to make the scripts executable

### Pytest

- Config at `setup.cfg`

## Credentials

### Notebook

- Token: 5003-project

### TimescaleDB

- DB Name: 5003-project-dev  
- Username: 5003-project  
- Password: 5003-project  
