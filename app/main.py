import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

import app.models as models
from app.schemas import UsuarioLogin
from app.database import engine, get_db
from app.routers import produtos, categorias, pedidos

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Funções avulsas
def criar_access_token(email: str, cargo: str):
    '''
    Função responsável por criar um token de acesso JWT.
    '''
    expiracao = datetime.now(timezone.utc) + timedelta(hours=2)

    payload = {
        "sub": email,
        "cargo": cargo,
        "exp": expiracao
    }
    token = jwt.encode(payload, "secret_key_muito_forte", algorithm="HS256")

    # Devolver no formato esperado
    return {"access_token": token, "token_type": "bearer"}

# Endpoint para checar se a API está rodando
@app.get('/')
def alive():
    return {'running': 'True'}


# Requisito Funcional: É preciso haver autenticação
@app.post('/login')
def login(payload: UsuarioLogin, db: Session = Depends(get_db)):
    # Descobrir de que usuário estamos falando (ou se nem existe)
    usuario = db.query(models.Usuario).filter(models.Usuario.email == payload.email).first()

    # Se não existe um tal usuário no banco, despachamos o erro de volta para quem fez a requisição
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Em seguida, testamos se o hash da senha enviada é o mesmo que o hash armazenado no banco de dados
    senha_valida = bcrypt.checkpw(
            payload.senha.encode('utf-8'), 
            usuario.senha.encode('utf-8')
        )

    if not senha_valida:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = criar_access_token(email=usuario.email, cargo=usuario.cargo)

    return token_data

### ROTEADROES ###
app.include_router(produtos.router)
app.include_router(categorias.router)
app.include_router(pedidos.router)