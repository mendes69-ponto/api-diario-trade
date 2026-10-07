from pydantic import BaseModel
from datetime import datetime

# Isso define o que o usuário PRECISA enviar para registrar um trade
class TradeCreate(BaseModel):
    ativo: str
    estrategia: str
    resultado_financeiro: float

# Isso define o formato que a API vai DEVOLVER para o usuário
class TradeResponse(BaseModel):
    id: int
    ativo: str
    estrategia: str
    resultado_financeiro: float
    data: datetime

    class Config:
        from_attributes = True