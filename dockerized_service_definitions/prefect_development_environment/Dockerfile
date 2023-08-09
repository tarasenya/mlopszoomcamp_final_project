FROM prefecthq/prefect:2.11.3-python3.9

RUN apt-get update && apt-get install -y libgomp1
RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app
COPY [ "Pipfile", "Pipfile.lock", "./" ]
RUN pipenv install --system --deploy
COPY ["prefect.yaml", "./aws_scripts/flows_orchestration_scripts.sh","./"]
ENV PYTHONPATH /app
#CMD "cd src/models && python model_training_flows.py"
#CMD "prefect deploy -n train_initial_model_deployment && prefect deployment run 'TrainInitialModel/train_initial_model_deployment'"
