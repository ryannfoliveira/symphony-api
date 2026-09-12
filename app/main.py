from fastapi import FastAPI, Depends, HTTPException
import app.models as models
from app.database import engine, SessionLocal
from app.routers import produtos, clientes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Endpoint para checar se a API está rodando
@app.get('/')
def alive():
    return {'running': 'True'}


# Requisito Funcional: É preciso haver autenticação
@app.get('/login')
def login():
    raise HTTPException(status_code=501, detail="Autenticação ainda não implementada")

### ROTEADROES ###
app.include_router(produtos.router)