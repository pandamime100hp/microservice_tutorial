FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests build-essential default-libmysqlclient-dev \
    && apt-get install pkg-config -y --no-install-recommends --no-install-suggests default-libmysqlclient-dev build-essential \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 5000

CMD ["python", "server.py"]