# django-framework-python
- [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
- [https://docs.djangoproject.com/en/3.0/](https://docs.djangoproject.com/en/3.0/)
# start project 
step 1: install docker and docker-compose

- [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
- [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)

step 2: Build code with docker compose
```
- docker-compose build
- docker-compose up -d
```

step 3: Create folder logs tại root project

step 4: Run
```
- run server 0.0.0.0:8010
```

# for development 
step 1: install requirements
```
- python3 -m venv env
- source env/bin/activate 
- pip install -r requirements.txt 
```
step 2: Run
```
- python manage.py runserver 0.0.0.0:8001
- run server at 0.0.0.0:8001
```

# for production 
```
- docker-compose -f docker-compose.prod.yml build
- docker-compose -f docker-compose.prod.yml up -d
```
- run server 0.0.0.0:8123

