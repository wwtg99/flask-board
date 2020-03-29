FROM python:3.8

COPY . /opt
WORKDIR /opt
RUN pip install --no-cache-dir -r requirements.txt -i {{ pip_index }}
CMD ["gunicorn", "-b", "0.0.0.0:80", "server:app"]
