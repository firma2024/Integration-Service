from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


@dataclass
class Actuacion:
    nombreActuacion: str
    anotacion: Optional[str]
    fechaActuacion: datetime
    fechaRegistro: datetime
    fechaInicia: str
    fechaFinaliza: str
    proceso: int
    existDocument: bool = field(default=False)


@dataclass
class PreProceso:
    idProceso: int
    numeroRadicado: str
    despacho: str
    departamento: str
    sujetos: str
    fechaRadicacion: datetime
    tipoProceso: str
    ubicacionExpediente: str

@dataclass
class ProcesoBuscar(BaseModel):
    number_process: int
    date: str
    file_number: str


@dataclass
class Proceso:
    idProceso: int
    numeroRadicado: str
    despacho: str
    departamento: str
    sujetos: str
    fechaRadicacion: datetime
    actuaciones: List[Actuacion]
    tipoProceso: str
    ubicacionExpediente: str


@dataclass
class ActuacionEmail:
    id: int
    actuacion: str
    radicado: str
    anotacion: str
    fechaActuacion: str
    emailAbogado: str
    nameAbogado: str
    link: str
