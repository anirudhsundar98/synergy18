# Synergy Website


## Prerequisites
- [Python3](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)
- [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
- phpMyAdmin
- nginx (for use with docker and for deployment)
- Virtualenv (can be used for local development without docker)

## Setting up the project
- Clone the repository locally and cd into it
- Create a virtual environment
```
virtualenv venv -p python3
source venv/bin/activate
```
- Install dependencies
```
pip install -r requirements.txt
```
- Configure database credentials in `db.cnf`
```
cp db.cnf.example db.cnf
```
- NOTE: Remove the line `host = db` in `db.cnf` for local development. Add it when using docker for development and/or deployment.


- Create and run migrations
```
python manage.py makemigrations
python manage.py migrate
```
- Run a dev server using python
```
python manage.py runserver
```
- Run with docker
```
docker-compose up
```
