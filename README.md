# 5003 Project

## Getting Started

### Env Info

Python version: 3.9.4  
Anaconda version: 2021.05  
Code formatter: autopep8

### Managing Conda Environment

Install: `conda env create -f src/backend-api/environment.yml`  
Activate: `conda activate 5003-project`  
Export conda package list: `conda env export --no-builds --from-history > src/backend-api/environment.yml`  
Export pip package list: `pip list --format=freeze > src/backend-api/requirements.txt`  

### Start API Dev Server  

1. cd to project root
2. Call `uvicorn src.backend-api.app.main:app --reload --env-file=".env" --app-dir="src/backend-api/app"`
3. Access docs at `http://127.0.0.1:8000/latest/docs`

## Docker Compose

Running in local: `docker compose up`

- Docs at [http://127.0.0.1:80/latest/docs](http://127.0.0.1:80/latest/docs)  
- Notebook at [http://localhost:8888/](http://localhost:8888/)  

Running in local with rebuild: `docker compose up --build`  
Interactive shell for debugging: `docker compose up && docker-compose run backend-api sh`

## Credentials

Notebook: 5003-project
