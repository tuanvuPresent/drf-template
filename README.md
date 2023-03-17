# django-framework-python

- [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
- [https://docs.djangoproject.com/en/3.0/](https://docs.djangoproject.com/en/3.0/)

## Usage

### Dependencies

- Install docker and docker-compose

> [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

> [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)

### For development

step 1: install requirements

```
- python3 -m venv env
- source env/bin/activate 
- pip install -r requirements.txt 
```

step 2: Run

```
python manage.py runserver 0.0.0.0:8001
```

### For docker

step 1: Build code with docker compose

```
- docker-compose build
- docker-compose up -d
```

> Run: http://0.0.0.0:8010/

### For production

```
- docker-compose -f docker-compose.prod.yml build
- docker-compose -f docker-compose.prod.yml up -d
```

> Run: http://0.0.0.0:8123/

---

## setup celery

`1. celery.py`

```python
# django_celery/celery.py

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'scheduled_send_chatwork-every-day': {
        'task': 'apps.tasks.test',
        'schedule': crontab(),
    },
}

```

`2. setings.py`

```python
INSTALLED_APPS = [
    'django_celery_beat',
    'django_celery_results',
]
# django_celery/settings.py
# ...
# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
```

`3. __init__.py`

```python
# django_celery/__init__.py
from .celery import app as celery_app

__all__ = ("celery_app",)
```

`4. requrements.txt`

```text
celery==4.4.7
redis==3.5.3
django_celery_beat==2.0.0
django_celery_results==1.2.1
```
