from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post('/')
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Criação de pedidos ainda não implementada")