FROM prefecthq/prefect:2-python3.9
RUN apt-get update && apt-get install -y libgomp1
RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]
RUN pipenv install --system --deploy

COPY ["/src/models/model_training_flows.py", "/opt/prefect/flows/"]