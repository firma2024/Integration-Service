
from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class ActuacionEmail(BaseModel):
    id: int
    demandante: str
    demandado: str
    actuacion: str
    radicado: str
    anotacion: str
    fechaActuacion: str
    emailAbogado: str
    nameAbogado: str
    link: str

