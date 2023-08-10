FROM prefecthq/prefect:2.11.3-python3.9

RUN apt-get update && apt-get install -y libgomp1
RUN apt-get install curl -y
RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app
COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy
ENV PYTHONPATH /app


