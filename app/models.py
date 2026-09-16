from sqlalchemy import Column, String, Integer, Float, ForeignKey
from app.database import Base

class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True)

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    preco = Column(Float)
    estoque = Column(Integer)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    cargo = Column(String)  # São eles: cliente, funcionário e administrador ( escrito "admin")

class Pedidos(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    data = Column(String)

class ItensPedidos(Base):
    __tablename__ = 'itens_pedidos'
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    quantidade = Column(Integer)