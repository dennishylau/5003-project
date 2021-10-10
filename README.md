# 5003 Project

## Getting Started

### Env Info

Python version: 3.9.4  
Anaconda version: 2021.05  
Code formatter: autopep8

### Managing Conda Environment

Install: `conda env create -f environment.yml`  
Activate: `conda activate 5003-project`  
Export conda package list: `conda env export --no-builds --from-history > environment.yml`  
Export pip package list: `pip list --format=freeze > requirements.txt`  

### Start Dev Servers  

1. cd to project root
2. Duplicate `.env.example` and rename it to `.env`, update the credentials inside if needed
3. API
   1. Call `uvicorn src.backend_api.app.main:app --reload --env-file=".env" --app-dir="src/backend_api/app"`
   2. Access docs at `http://127.0.0.1:8000/latest/docs`
4. Notebook
   1. Call `jupyter-lab --config=/jupyter_lab_config.py`
   2. Access at `http://127.0.0.1:8888/`

## Docker Compose

Running in local: `docker compose -f docker-compose.local.yml up`

- Docs at [http://127.0.0.1:80/latest/docs](http://127.0.0.1:80/latest/docs)  
- Notebook at [http://localhost:8888/](http://localhost:8888/)  
- TimescaleDB at `localhost:5432`  

See list of credentials below.  

Running in local with rebuild: `docker compose -f docker-compose.local.yml up --build`  
Interactive shell for debugging: `docker compose -f docker-compose.local.yml up && docker-compose run backend-api sh`

## Additional Setup

### Git Hooks

- Set this up so no need to manually run `conda env export` and `pip freeze`
- Run `git config core.hooksPath githooks` to modify the default hooks directory
- Run `chmod +x githooks/*` to make the scripts executable

## Credentials

### Notebook

- Password: 5003-project

### TimescaleDB

- DB Name: 5003-project-dev  
- Username: 5003-project  
- Password: 5003-project  
