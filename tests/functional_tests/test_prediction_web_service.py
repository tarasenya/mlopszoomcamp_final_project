import requests

test_patient_info = {'gender': 'Male',
                     'age': 67,
                     'hypertension': 0,
                     'heart_disease': 1,
                     'ever_married': 'Yes',
                     'work_type': 'Private',
                     'Residence_type': 'Urban',
                     'avg_glucose_level': 228.69,
                     'bmi': 36.6,
                     'smoking_status': 'formerly smoked',}

url = 'http://0.0.0.0:9696/predict'

if __name__ == '__main__':
    response = requests.post(url, json=test_patient_info)
    print(response.json())
