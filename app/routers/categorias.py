from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.post('/')
def add_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = models.Categoria(nome=categoria.nome)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    
    return db_categoria

@router.get('/{categoria_id}')
def categoria_read(categoria_id: int, db: Session = Depends(get_db)):
    categorias = [db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()]

    if not categorias:
        return {"detail": "Não há nenhuma categoria com o id especificado."}

    return categorias

@router.get('/')
def categoria_list(db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).all()

    if not categorias:
        return {"detail": "Não há categorias"}

    return categorias

@router.put('/{categoria_id}')
def categoria_update(categoria_id: int, new_info: schemas.CategoriaUpdate, db: Session = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Atualização de categorias ainda não implementada")

@router.delete('/{categoria_id}')
def categoria_delete(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

    if not categoria:
        raise HTTPException(status_code=404, detail="A categoria especificada não existe.")
    
    db.delete(categoria)
    db.commit()
    
    return {"detail": "Categoria deletada com sucesso."}