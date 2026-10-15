from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from app.database import get_db
from app.routers.auth import verificar_token_jwt

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# Requisito Funcional 1: Cadastrar produtos em estoque
@router.post('/')
def produto_create(produto: schemas.ProdutoCreate,
                   db: Session = Depends(get_db),
                   usuario_atual: dict = Depends(verificar_token_jwt)):

    if usuario_atual['cargo'] not in ['admin', 'funcionario']:
        raise HTTPException(status_code=403, detail="Você não possui permissão para criar produtos.")
    
    db_produto = models.Produto(
        nome = produto.nome,
        preco = produto.preco,
        estoque = produto.estoque,
        categoria_id = produto.categoria_id
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    
    return db_produto

# Requisito Funcional 2: Listar os instrumentos musicais
@router.get('/{product_id}')
def produto_read(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Produto).filter(models.Produto.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    return product

@router.get('/')
def produto_list(db: Session = Depends(get_db)):
    products = db.query(models.Produto).all()

    if not products:
        return {"detail": "Não há produtos"}

    return products

# Requisito Funcional 3: Atualizar dados do produto
@router.put('/{product_id}')
def produto_update(product_id: int, new_info: schemas.ProdutoUpdate,
                   db: Session = Depends(get_db),
                   usuario_atual: dict = Depends(verificar_token_jwt)):

    if usuario_atual['cargo'] not in ['admin', 'funcionario']:
        raise HTTPException(status_code=403, detail="Você não possui permissão para resetar os produtos.")

    product = db.query(models.Produto).filter(models.Produto.id == product_id).first()

    update = new_info.model_dump(exclude_unset=True)

    for key, value in update.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    
    return product

# Requisito Funcional 4: Deletar produtos cuja venda será descontinuada
@router.delete('/{product_id}')
def produto_delete(product_id: int, db: Session = Depends(get_db),
                   usuario_atual: dict = Depends(verificar_token_jwt) ):

    if usuario_atual['cargo'] not in ['admin', 'funcionario']:
        raise HTTPException(status_code=403, detail="Você não possui permissão para resetar os produtos.")

    # Encontra o produto
    product = db.query(models.Produto).filter(models.Produto.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="O produto especificado não existe.")
    
    db.delete(product)
    db.commit()
        
    return {'message': f'Produto {product_id} removido com sucesso'}

@router.delete('/reset')
def reset_products(db: Session = Depends(get_db),
                   usuario_atual: dict = Depends(verificar_token_jwt)):
    
    if usuario_atual['cargo'] not in ['admin', 'funcionario']:
        raise HTTPException(status_code=403, detail="Você não possui permissão para resetar os produtos.")
    
    # O equivalente ao TRUNCATE ou DELETE FROM products;
    db.query(models.Produto).delete()
    db.commit()
    return {"detail": "Toda a tabela foi limpa!"}