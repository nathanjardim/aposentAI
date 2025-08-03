from pydantic import BaseModel

class SimulacaoRequest(BaseModel):
    idade: int
    aporte: float
    resultado: float
