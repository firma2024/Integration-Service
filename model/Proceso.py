from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from model.Actuacion import Actuacion

@dataclass
class Proceso:
    idProceso: int
    numeroRadicado: str
    fechaUltimaActuacion: datetime
    despacho: str
    departamento: str
    demandante: str
    demandado: str
    fechaRadicacion: datetime
    actuaciones: List[Actuacion]
    tipoProceso: str
    ubicacionExpediente: str