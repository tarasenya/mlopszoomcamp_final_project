Assumptions:
It is assumed that one works on a linux system with installed docker/docker-compose and makefile.
In order to deploy all the services one should do the following:

1. Go to root folder of the project.

```bash
make build_all_services
docker-compose up
```

Explanations: the first command builds images of all dockerized services, the second sets them (and
some others) up and running, orchestrates them.
2.
