from fastapi import FastAPI,HTTPException
from service.process import ProcessService
import uvicorn

app = FastAPI()
process_service = ProcessService()

@app.get("/getUrl/despacho={office_Name}")
def get_office(office_Name: str):
    url = process_service.get_office_url(office_Name)
    if url:
        return {"url_despacho":url}
    else:
        raise HTTPException(status_code=404, detail="Despacho no encontrado")


@app.get("/getProcess/fileNumber={file_number}")
def get_process(file_number):
    return process_service.get_process_info(file_number)

#ONLY DEBUG
"""if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)"""
