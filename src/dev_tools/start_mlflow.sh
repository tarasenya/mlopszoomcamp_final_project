#!/bin/bash
mlflow server --host 0.0.0.0 -p 5000 --backend-store-uri sqlite:///mlflow.db --artifacts-destination ./artifacts
