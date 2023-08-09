#!/bin/bash
prefect deploy --all && prefect deployment run 'TrainInitialModel/train-initial-model-deployment'