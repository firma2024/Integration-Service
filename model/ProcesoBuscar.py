from pydantic import BaseModel


class ProcesoBuscar(BaseModel):
    number_process: int
    date: str
    file_number: int