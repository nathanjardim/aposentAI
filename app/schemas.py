from pydantic import BaseModel

class SimulacaoRequest(BaseModel):
    idade: int
    idade_aposentadoria: int
    aporte: float
    resultado: float
