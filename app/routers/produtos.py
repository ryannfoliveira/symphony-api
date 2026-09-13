from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from app.database import get_db

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# Requisito Funcional 1: Cadastrar produtos em estoque
@router.post('/products')
def add_product(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = models.Produto(
        nome = produto.nome,
        preco = produto.preco,
        estoque = produto.estoque
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    
    return db_produto

# Requisito Funcional 2: Listar os instrumentos musicais
@router.get('/products')
def list_products(db: Session = Depends(get_db)):
    products = db.query(models.Produto).all()

    if not products:
        return {"detail": "Não há produtos"}

    return products

# Requisito Funcional 3: Atualizar quantidade em estoque
@router.put('/products/{product_id}')
def update_entry(product_id: int, new_info: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    product = db.query(models.Produto).filter(models.Produto.id == product_id).first()

    update = new_info.model_dump(exclude_unset=True)

    for key, value in update.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    
    return product

# Requisito Funcional 4: Deletar produtos cuja venda será descontinuada
@router.delete('/products/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Encontra o produto
    product = db.query(models.Produto).filter(models.Produto.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="O produto especificado não existe.")
    
    db.delete(product)
    db.commit()
        
    return {'message': f'Produto {product_id} removido com sucesso'}

@router.delete('/reset-products')
def reset_products(db: Session = Depends(get_db)):
    # O equivalente ao TRUNCATE ou DELETE FROM products;
    db.query(models.Produto).delete()
    db.commit()
    return {"detail": "Toda a tabela foi limpa!"}