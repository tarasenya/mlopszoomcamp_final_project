Assumptions:
It is assumed that one works on a linux system with installed docker/docker-compose and makefile.
In order to deploy all the services one should do the following:

1. Go to root folder of the project. Set environmental variables defined in .env file of the project by
```bash
set -a
set -o allexport
. .env
set +a
```
or by setting them manually vie export command.
2. Execute then the following commands
```bash
make build_all_services
docker-compose up
```

Explanations: the first command builds images of all dockerized services, the second sets them (and
some others) up and running, orchestrates them.
3. Predict endpoint is available on the 9696/predict and can be tested by executing from the root folder of the project:
```bash
pipenv run python tests/integration_tests/test_bucket.py
```
