FROM python:3.9.7-slim
RUN apt-get update && apt-get install -y libgomp1
RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy