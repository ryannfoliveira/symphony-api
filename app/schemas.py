from pydantic import BaseModel, Field
from typing import Optional

class Produto(BaseModel):
    nome: str
    preco: float = Field(gt=0)
    estoque: int = Field(gt=0)

# Está igual à base, mas é uma classe separada por
# propósitos de manutenibilidade e escalabilidade
class ProdutoCreate(Produto):
    pass

class ProdutoRead(Produto):
    id: int

    class Config:
        from_attributes = True

class ProdutoUpdate(BaseModel):
    nome: Optional[str]
    preco: Optional[float] = Field(None, gt=0)
    estoque: Optional[int] = Field(None, gt=0)

### CATEGORIAS ###
class Categoria(BaseModel):
    nome: str

class CategoriaCreate(Categoria):
    pass

class CategoriaRead(Categoria):
    id: int

    class Config:
        from_attributes = True

class CategoriaUpdate(BaseModel):
    nome: Optional[str]

### USUÁRIOS ###
class Usuario(BaseModel):
    nome: str
    email: str
    senha: str
    cargo: str

class UsuarioCreate(Usuario):
    pass

class UsuarioRead(Usuario):
    id: int

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nome: Optional[str]
    email: Optional[str]
    senha: Optional[str]
    cargo: Optional[str]

### PEDIDOS ###
class Pedido(BaseModel):
    usuario_id: int
    data: str