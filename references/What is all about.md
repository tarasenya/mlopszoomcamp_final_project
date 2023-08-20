Detailed description of business logics
------
Assume that a hospital needs a method to predict whether a patient will get a stroke or not. It has a historical data collected before. Based on it, we build a ml model and observe it s performance. Once pro month we get a report with new data (in some sense it will be biased, since if it is assumed that a patient will get a stroke he/hse will get a treatment). After new reports we retrain the model and so on.

Description of flows
------
There are 3 deployments:
1. TrainInitialModel
2. RetrainModel
3. GenerateReport

**TrainInitialModel** is run on the execution prefect environment at the start. This flow generates an initial model which is served by the prediction web service.
The model is trained using initial_heart_stroke_data.csv from data dir, which is transferred to S3 bucket at the beginning.
Moreover, we assume that in the future some csv dumps (one can think of them as of a database dumps) with old and new data are also transferred to the corresponding bucket.  This corresponds to our business case, every month we get the results whether patients we attested with our model indeed got a heart stroke or not.
To mimic this behaviour, we use copy_files_to_bucket.sh from aws_scripts folder.
This script takes a heart_stroke_.csv data, which is a concatenation of initial csv and some other test data, appends the current date to the name and uploads it to the heart-stroke-bucket.

**GenerateReport flow** generates an EvidentlyAI Report. It is scheduled for every Monday. If one runs it manually, one should run copy_files_to_bucket.sh before.

**RetrainModel** flow retrains a model that is used by a web service, if such retraining is needed (it is decided by the correspondent evidently AI test). To run this flow manually, one should proceed as above for GenerateReport flow.


In order to access prefect flows, go to 4200/api and proceed with it as in the course.


In order to access mlflow server, got to 5000.
