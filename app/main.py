from fastapi import FastAPI

import app.models as models
from app.database import engine
from app.routers import auth, produtos, categorias, pedidos

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Endpoint para checar se a API está rodando
@app.get('/')
def alive():
    return {'running': 'True'}

### ROTEADROES ###
app.include_router(auth.router)
app.include_router(produtos.router)
app.include_router(categorias.router)
app.include_router(pedidos.router)