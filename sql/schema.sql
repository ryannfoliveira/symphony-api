-- Minha gente, sei que não é uma prática muito boa deixar o id como integer autoincrementável (além de outras maluquices)
-- Num cenário real, numa loja real com vários acessos, isso iria causar problemas de concorrência,
-- além de ser fácil de adivinhar. Mas o foco aqui é a API.
-- Noutro projeto futuro eu exponho um SQL mais robusto, que seja realmente utilizável em produção

-- No mais, o schema abaixo é fruto de refatoração e expansão do meu outro repositório, mais antigo, symphony-sql

CREATE TABLE categorias (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255) UNIQUE
);

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY,
    categoria_id INTEGER NOT NULL REFERENCES categorias(id) ON DELETE SET NULL,
    nome VARCHAR(255),
    preco DECIMAL(10,2) NOT NULL CHECK (preco >= 0),
    estoque INTEGER NOT NULL CHECK (estoque >= 0)
);

-- Tabela única de pessoas
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    senha VARCHAR(255),
    cargo VARCHAR(255) CHECK (cargo IN ('admin', 'funcionario', 'cliente'))
);

CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES usuarios(id),
    data DATE DEFAULT CURRENT_DATE
);

CREATE TABLE itens_pedidos (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    produto_id INTEGER NOT NULL REFERENCES produtos(id),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10,2) NOT NULL CHECK (preco_unitario >= 0)
    -- Essa é uma técnica de desnormalização proposital. Aprendi esse termo faz um tempinho
    -- Nessa coluna se salva o preço no momento da compra, já que produtos(preco) é mutável,
    --o que garante reconstrução fidedigna do histórico
);