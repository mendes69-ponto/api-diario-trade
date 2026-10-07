from typing import Optional
from fastapi import FastAPI, Depends,  HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine

# Essa linha cria o arquivo trades.db e as tabelas automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Diário de Trade API",
    description="API para gerenciar operações na bolsa de valores.",
    version="1.0"
)

# Função para abrir e fechar a conexão com o banco a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para CADASTRAR um novo trade no banco
@app.post("/trades/", response_model=schemas.TradeResponse)
def registrar_trade(trade: schemas.TradeCreate, db: Session = Depends(get_db)):
    novo_trade = models.Trade(
        ativo=trade.ativo,
        estrategia=trade.estrategia,
        resultado_financeiro=trade.resultado_financeiro
    )
    db.add(novo_trade)
    db.commit()            # Confirma a gravação
    db.refresh(novo_trade) # Atualiza com o ID gerado e a data
    return novo_trade

# Rota para LER todos os trades salvos
@app.get("/trades/", response_model=list[schemas.TradeResponse])
def listar_trades(db: Session = Depends(get_db)):
    trades = db.query(models.Trade).all()
    return trades

  # NOVA ROTA: Estatísticas com Filtro de Estratégia
@app.get("/estatisticas/")
def obter_estatisticas(estrategia: Optional[str] = None, db: Session = Depends(get_db)):
    # Inicia a busca no banco de dados
    query = db.query(models.Trade)
    
    # Se o usuário digitar uma estratégia, aplica o filtro
    if estrategia:
        query = query.filter(models.Trade.estrategia == estrategia)
        
    trades = query.all()
    
    total_trades = len(trades)
    if total_trades == 0:
        texto_erro = f"Nenhum trade encontrado para a estratégia '{estrategia}'." if estrategia else "Nenhum trade registrado."
        return {"mensagem": texto_erro}
        
    trades_vencedores = [t for t in trades if t.resultado_financeiro > 0]
    taxa_acerto = (len(trades_vencedores) / total_trades) * 100
    saldo_total = sum(t.resultado_financeiro for t in trades)
    
    return {
        "estrategia_analisada": estrategia or "Todas as estratégias",
        "total_operacoes": total_trades,
        "taxa_de_acerto": f"{taxa_acerto:.2f}%",
        "saldo_financeiro_total": f"R$ {saldo_total:.2f}"
    }

 # NOVA ROTA: Deletar um trade registrado por engano
@app.delete("/trades/{trade_id}")
def deletar_trade(trade_id: int, db: Session = Depends(get_db)):
    # Busca o trade específico pelo ID
    trade = db.query(models.Trade).filter(models.Trade.id == trade_id).first()
    
    # Se o ID não existir, retorna o clássico erro 404
    if not trade:
        raise HTTPException(status_code=404, detail="Trade não encontrado.")
        
    db.delete(trade)
    db.commit()
    return {"mensagem": f"Trade {trade_id} deletado com sucesso!"}