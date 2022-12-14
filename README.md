# How to install

## With docker
```
docker-compose build
docker-compose up -d
docker-compose exec app ./manage.py migrate
```
## With Venv
```
python3 -m venv /path/to/new/virtual/environment
source <venv_path>/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
