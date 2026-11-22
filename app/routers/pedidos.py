from datetime import datetime
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from app.database import get_db
from app.routers.auth import verificar_token_jwt

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post('/', status_code=201)
def pedido_create(pedido: schemas.PedidoCreate, db: Session = Depends(get_db), usuario_atual: dict = Depends(verificar_token_jwt)):

    if not pedido.produtos:
        raise HTTPException(status_code=400, detail="O pedido deve conter ao menos um produto.")
    
    # A lista dos itens, como vieram na requisição, para poder fazer checagens
    itens: Dict[int, int] = {} # {id: quantidade}

    for item in pedido.produtos:
        itens[item.produto_id] = itens.get(item.produto_id, 0) + item.quantidade

    produtos_db = db.query(models.Produto).filter(models.Produto.id.in_(list(itens.keys()))).all()
    # Isso em cima só retorna os produtos que de fato existem
    # Vou criar um outro dicionário para esses produtos
    produtos = {produto.id: produto.estoque for produto in produtos_db}
    
    for id, quantidade in itens.items():
        produto = produtos.get(id)
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto com id {id} não encontrado.")
        if produto < quantidade:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para o produto {produto.nome}. Pedimos desculpas pelo transtorno.")

    id_atual = db.query(models.Usuario).filter(models.Usuario.email == usuario_atual['email']).first().id

    try:
        db_pedido = models.Pedido(cliente_id=id_atual, data=datetime.now().isoformat())
        db.add(db_pedido)
        db.flush()

        for item in pedido.produtos:
            db_item = models.ItensPedidos(
                pedido_id=db_pedido.id,
                produto_id=item.produto_id,
                quantidade=item.quantidade,
                preco_unitario=db.query(models.Produto).filter(models.Produto.id == item.produto_id).first().preco
            )
            db.add(db_item)
            # Atualizando o estoque do produto
            produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
            produto.estoque -= item.quantidade
            db.refresh(produto)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=e.args[0] if e.args else "Erro ao criar o pedido.")
    else:
        db.commit()
        db.refresh(db_pedido)
        db.refresh(db_item)

        return db_pedido

@router.get('/{pedido_id}')
def pedido_read(pedido_id: int, db: Session = Depends(get_db), usuario_atual: dict = Depends(verificar_token_jwt)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

    id_atual = db.query(models.Usuario).filter(models.Usuario.email == usuario_atual['email']).first().id

    if pedido.cliente_id != id_atual and usuario_atual['cargo'] not in ['admin', 'funcionario']:
        raise HTTPException(status_code=403, detail="O pedido não está associado à sua conta.")

    if not pedido:
        raise HTTPException(status_code=404, detail="Não existe nenhum pedido com o id informado.")

    itens = db.query(models.ItensPedidos).filter(models.ItensPedidos.pedido_id == pedido_id).all()
    produtos = []
    for item in itens:
        produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
        produtos.append({
            "produto_id": produto.id,
            "nome": produto.nome,
            "quantidade": item.quantidade,
            "preco_unitario": item.preco_unitario
        })

    return {
        "pedido_id": pedido.id,
        "cliente_id": pedido.cliente_id,
        "data": pedido.data,
        "status": pedido.status,
        "produtos": produtos
    }

# Uma rota produto_list seria sem sentido

@router.put('/{pedido_id}')
def pedido_update(pedido_id: int, new_info: schemas.PedidoUpdate, db: Session = Depends(get_db), usuario_atual: dict = Depends(verificar_token_jwt)):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Não existe nenhum pedido com o id informado.")
    
    id_atual = db.query(models.Usuario).filter(models.Usuario.email == usuario_atual['email']).first().id

    if pedido.cliente_id != id_atual and usuario_atual['cargo'] not in ['admin', 'funcionario']:
        raise HTTPException(status_code=403, detail="O pedido não está associado à sua conta.")

    if usuario_atual['cargo'] not in ['admin', 'funcionario'] and new_info.status == 'concluido':
        raise HTTPException(status_code=403, detail="Você não possui permissão para marcar pedidos como concluídos.")

    elif usuario_atual['cargo'] not in ['admin', 'funcionario'] and pedido.status == 'cancelado':
        raise HTTPException(status_code=403, detail="Uma vez cancelado, o pedido não pode ser mais alterado. Contate o suporte.")

    update = new_info.model_dump(exclude_unset=True)

    for key, value in update.items():
        setattr(pedido, key, value)

    db.commit()
    db.refresh(pedido)

    return pedido