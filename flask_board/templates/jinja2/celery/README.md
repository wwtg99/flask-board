Flask Project
=============

# Description

Develop Flask application with [Celery](https://docs.celeryproject.org/en/stable/).

# Install requirements

```
pip install -r requirements.txt
```

# Run dev server

```
flask run
```

# Run celery worker

Config your celery broker first in the .env file with `CELERY_BROKER_URL`.

```
celery worker -A worker:celery -l info
```

# Deploy with docker

Build docker image

```
docker build -t <your-image>:<your-tag> .
```

Run docker image web server

```
docker run -d -p 80:80 --env-file=.env <your-image>:<your-tag>
```

Run docker image celery worker

```
docker run -d --env-file=.env <your-image>:<your-tag> celery worker -A worker:celery
```

# Run unit tests

Define your tests in tests package.

```
pytest
```
