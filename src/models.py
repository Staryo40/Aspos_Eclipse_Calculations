from dataclasses import dataclass

@dataclass
class EclipseRecord:
    jde: float
    datetime: str
    k: float
    eclipse_type: str