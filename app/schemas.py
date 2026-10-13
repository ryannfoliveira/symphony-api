from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Produto(BaseModel):
    nome: str
    preco: float = Field(gt=0)
    estoque: int = Field(gt=0)
    categoria_id: int

# Está igual à base, mas é uma classe separada por
# propósitos de manutenibilidade e escalabilidade
class ProdutoCreate(Produto):
    pass

class ProdutoRead(Produto):
    id: int

    class Config:
        from_attributes = True

class ProdutoUpdate(BaseModel):
    nome: str | None
    preco: Optional[float] = Field(None, gt=0)
    estoque: Optional[int] = Field(None, gt=0)
    categoria_id: int | None

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
    email: EmailStr
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

## AUTENTICAÇÃO
class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

### PEDIDOS ###
class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)

class PedidoCreate(BaseModel):
    usuario_id: int
    produtos: List[ItemPedidoCreate]