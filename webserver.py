from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import requests

app = FastAPI()

url = "http://127.0.0.1:8000/predict"
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/consultar", response_class=HTMLResponse)
def consultar(
              nombre: str=Form(...),
              sexo: str=Form(...),
              edad: int=Form(...),
              monto: int=Form(...),
              tipo_vivienda: str=Form(...)):

    response = requests.post(url,
                             data={"sexo": sexo,
                                   "edad": edad,
                                   "monto": monto,
                                   "tipo_vivienda": tipo_vivienda})

    respuesta = response.json()
    if respuesta["proba_bad_client"] > 0.5:
        mensaje = f"<h3>Apreciado {nombre}, no le podemos prestar dinero.</h3>"
    else:
        mensaje = f"<h3>Apreciado {nombre}, su crédito fue aprobado</h3>"

    return mensaje
