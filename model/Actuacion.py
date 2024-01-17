from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Actuacion:
    nombreActuacion: str
    anotacion: Optional[str]
    fechaActuacion: datetime
    fechaRegistro: datetime
    fechaInicia: datetime
    fechaFinaliza: datetime
    proceso: int
    existDocument: bool = field(default=False)