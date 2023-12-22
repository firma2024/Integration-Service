from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Actuacion:
    nombreActuacion: str
    anotacion: Optional[str]
    fechaActuacion: datetime
    fechaRegistro: datetime
    proceso: Optional[str]

@dataclass
class Proceso:
    idProceso: int
    numeroRadicado: str
    despacho: str
    departamento: str
    demandante: str
    demandado: str
    fechaRadicacion: datetime
    actuaciones: List[Actuacion]
    tipoProceso: str
    ubicacionExpediente: str
