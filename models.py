from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    ativo = Column(String, index=True) # Ex: WINV26
    estrategia = Column(String)        # Ex: Rompimento, Pullback
    resultado_financeiro = Column(Float) # Ex: 50.0 (Gain) ou -30.0 (Loss)
    data = Column(DateTime, default=datetime.datetime.utcnow)