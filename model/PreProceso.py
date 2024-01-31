from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from model.Actuacion import Actuacion

@dataclass
class PreProceso:
    idProceso: int
    numeroRadicado: str
    despacho: str
    departamento: str
    demandante: str
    demandado: str
    fechaRadicacion: datetime
    tipoProceso: str
    ubicacionExpediente: str