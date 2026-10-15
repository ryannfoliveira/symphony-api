from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from app.database import get_db
from app.routers.auth import verificar_token_jwt

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.post('/')
def add_categoria(
    categoria: schemas.CategoriaCreate,
    db: Session = Depends(get_db),
    usuario_atual: dict = Depends(verificar_token_jwt)):

    if usuario_atual['cargo'] not in ['admin', 'funcionario']:
        raise HTTPException(status_code=403, detail="Você não possui permissão para criar categorias.")
    # Como está com um Depends, não é necessário verificar se o usuário fez login.
    # Se já não tivesse feito, o próprio FastAPI apitaria um 401
    db_categoria = models.Categoria(nome=categoria.nome)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
        
    return db_categoria

@router.get('/{categoria_id}')
def categoria_read(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

    if not categoria:
        raise HTTPException(status_code=404, detail="Não há nenhuma categoria com o id especificado.")

    return categoria

@router.get('/')
def categoria_list(db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).all()

    if not categorias:
        return {"detail": "Não há categorias"}

    return categorias

@router.put('/{categoria_id}')
def categoria_update(categoria_id: int,
                     new_info: schemas.CategoriaUpdate,
                     db: Session = Depends(get_db),
                     usuario_atual: dict = Depends(verificar_token_jwt)):

    if usuario_atual['cargo'] not in ['admin', 'funcionario']:
        raise HTTPException(status_code=403, detail="Você não possui permissão para atualizar categorias.")

    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    update = new_info.model_dump(exclude_unset=True)

    for key, value in update.items():
        setattr(categoria, key, value)

    db.commit()
    db.refresh(categoria)
        
    return categoria

@router.delete('/{categoria_id}')
def categoria_delete(categoria_id: int,
                     db: Session = Depends(get_db),
                     usuario_atual: dict = Depends(verificar_token_jwt)):
    
    if usuario_atual['cargo'] not in ['admin', 'funcionario']:
        raise HTTPException(status_code=403, detail="Você não possui permissão para apagar categorias.")

    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    
    if not categoria:
        raise HTTPException(status_code=404, detail="A categoria especificada não existe.")
        
    db.delete(categoria)
    db.commit()
        
    return {"detail": "Categoria deletada com sucesso."}

@router.delete('/reset')
def reset_products(db: Session = Depends(get_db),
                   usuario_atual: dict = Depends(verificar_token_jwt)):
    
    if usuario_atual['cargo'] not in ['admin', 'funcionario']:
        raise HTTPException(status_code=403, detail="Você não possui permissão para resetar as categorias.")
    
    db.query(models.Categoria).delete()
    db.commit()
    return {"detail": "Toda a tabela foi limpa!"}