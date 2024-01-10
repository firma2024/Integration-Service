from fastapi import FastAPI
from model.Actuacion import Actuacion
from model.ActuacionEmail import ActuacionEmail
from model.ProcesoBuscar import ProcesoBuscar
from service.WebScraperService import WebScraperService
from service.SeleniumService import SeleniumService
from service.RestService import RestService
from service.EmailService import EmailService
import uvicorn
from typing import List

# FIXME delete this
from datetime import datetime

app = FastAPI()
web_scraper_service = WebScraperService()
selenium_service = SeleniumService()
rest_service = RestService()
email_service = EmailService()


@app.get("/getUrl/despacho={office_Name}")
def get_office(office_Name: str):
    print(office_Name)
    url_juzgado = web_scraper_service.get_url_juzgado(office_Name)

    while True:
        url_despacho = selenium_service.get_office_url(
            office_Name, url_juzgado)
        if url_despacho is not None:
            break
        print("Error de conexion, reintentando...")

    url_estados = web_scraper_service.get_url_estados(url_despacho)
    return {"url_despacho": url_estados}


@app.get("/getProcess/fileNumber={file_number}")
def get_process(file_number):
    return rest_service.get_process_info(file_number)


@app.post("/find/actuaciones")
def find_new_actuacion(request_body: List[ProcesoBuscar]):
    list_actuaciones = []
    for item in request_body:
        print(item.file_number, item.date, item.number_process)
        exist_actuacion, last_date_actuacion = rest_service.new_actuacion_process(
            item.file_number, item.date)
        if exist_actuacion:
            list_actuaciones.append(
                rest_service.get_last_actuacion(
                    item.number_process, last_date_actuacion)
            )
    return list_actuaciones


@app.post("/send_email")
def send_email_test(request_body: List[ActuacionEmail]):
    list_actuaciones_send = []
    # FIXME delete this dummy instance
    for item in request_body:
        # FIXME change this functionality
        print("Enviando email...","actuacion", item.id)
        send = email_service.send_email(item.emailAbogado, item)
        if send:
            list_actuaciones_send.append(item.id)
    
    return list_actuaciones_send
            

# ONLY DEBUG
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
