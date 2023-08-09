FROM python:3.9.7-slim
RUN apt-get update && apt-get install -y libgomp1
RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "/src/web_service/prediction_web_service.py", "./" ]

EXPOSE 9696
ENV PYTHONPATH /app

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "prediction_web_service:app" ]