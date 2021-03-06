Flask Project
=============

# Description

Develop Flask application.

# Install requirements

```
pip install -r requirements.txt
```

# Run dev server

```
flask run
```

# Deploy with docker

Build docker image

```
docker build -t <your-image>:<your-tag> .
```

Run docker image

```
docker run -d -p 80:80 --env-file=.env <your-image>:<your-tag>
```

# Run unit tests

Define your tests in tests package.

```
pytest
```
