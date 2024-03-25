from model.model import Actuacion, ActuacionEmail, PreProceso, Proceso, ProcesoBuscar
from service.WebScraperService import BeatifulSoupService
from service.WebScraperService import SeleniumService
from service.RestService import RestService
from service.EmailService import EmailService
import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import List, Dict
import asyncio

web_scraper_service = BeatifulSoupService()
selenium_service = SeleniumService()
rest_service = RestService()
email_service = EmailService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before the service start
    asyncio.create_task(selenium_service.get_offices())
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/api/integration/getUrl/despacho={office_name}/year={year}")
def get_office(office_name: str, year:str) -> Dict[str, str]:
    """Obtain url office given an office name

    Args:
        office_name (str): Office to be searched
        year (str): Year of the last action.

    Returns:
        Dict[str,str]: Dictionary with the office url.
    """
    url_court = selenium_service.get_office_url_df(office_name)
    url_estados = web_scraper_service.get_url_estados(url_court, year)
    return {"url_despacho": url_estados}


@app.get("/api/integration/getProcess/fileNumber={file_number}")
def get_process(file_number: str) -> PreProceso:
    """Get process information by CPNU.

    Args:
        file_number (str): Process file number to be searched in CPNU.

    Returns:
        PreProceso: Dataclass with the information process.
    """
    return rest_service.get_process_info(file_number)


@app.get("/api/integration/getAllProcess/fileNumber={file_number}")
def get_all_process_info(file_number: str) -> Proceso:
    """Get process and actions information by CPNU. 

    Args:
        file_number (str): Process file number to be searched in CPNU.

    Returns:
        Proceso: Dataclass with the information process and actions.
    """
    return rest_service.get_all_process_info(file_number)


@app.post("/api/integration/find/actuaciones")
def find_new_actuacion(request_body: List[ProcesoBuscar]) -> List[Actuacion]:
    """Check if actions exists.

    Args:
        request_body (List[ProcesoBuscar]): List of process to search.

    Returns:
        List[Actuacion]: List of actions with updates.
    """
    list_actuaciones = []
    for item in request_body:
        print(item.file_number, item.date, item.number_process)
        exist = rest_service.new_actuacion_process(
            item.file_number, item.date)
        if exist:
            new_actuaciones = rest_service.get_last_actuacion(item.number_process, item.date)
            for act in new_actuaciones:
                list_actuaciones.append(act)
    return list_actuaciones


@app.post("/api/integration/send_email")
def send_email(request_body: List[ActuacionEmail]) :
    """Send email when an logic detect an update action.

    Args:
        request_body (List[ActuacionEmail]): List of the 

    Returns:
        List[ActuacionEmail]: Actions submitted.
    """
    list_actuaciones_send = []
    for item in request_body:
        print("Enviando email...", "actuacion", item.id)
        send = email_service.send_email(item.emailAbogado, item)
        if send:
            list_actuaciones_send.append(item.id)

    return list_actuaciones_send


# ONLY DEBUG
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
