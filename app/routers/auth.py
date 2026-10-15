import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import app.models as models
from app.schemas import UsuarioLogin
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Autenticação"])

# Funções e objetos auxiliares
SECRET_KEY = "secret_key_muito_forte"
bearer = HTTPBearer()

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
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # Essa secret key é tão fraca que vai vir até warning

    # em aplicações mais bem-feitas, não é necessário inserir isso manualmente
    return token

def verificar_token_jwt(auth_headers: HTTPAuthorizationCredentials = Depends(bearer)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(auth_headers.credentials, SECRET_KEY, algorithms="HS256")
        
        email: str = payload.get("sub")
        cargo: str = payload.get("cargo")
        
        if email is None:
            raise credentials_exception
            
        return {"email": email, "cargo": cargo}
        
    except jwt.PyJWTError:
        raise credentials_exception

# Requisito Funcional: É preciso haver autenticação
@router.post('')
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