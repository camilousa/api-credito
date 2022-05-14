from fastapi import FastAPI, Form
import joblib
import boto3
import os

app = FastAPI()

s3 = boto3.resource('s3', 'us-east-1')
s3.meta.client.download_file('modelo-credito-255423', 'modelos/pipeline1.joblib', 'pipeline.joblib')
s3.meta.client.download_file('modelo-credito-255423', 'modelos/model01.joblib', 'model.joblib')

pipeline = joblib.load('pipeline.joblib')
modelo = joblib.load('model.joblib')

os.remove('pipeline.joblib')
os.remove('model.joblib')



@app.post("/predict")
def predict(sexo: str=Form(...),
            edad: int=Form(...),
            monto: int=Form(...),
            tipo_vivienda: str=Form(...)):

    X = pipeline.transform([[sexo, edad, monto, tipo_vivienda]])

    proba_bad_client = modelo.predict_proba(X)[0][1]
 
    return {"proba_bad_client": proba_bad_client}



