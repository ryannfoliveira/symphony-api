
# Symphony API

Symphony API é uma API REST desenvolvida com FastAPI para o gerenciamento de uma loja fictícia de instrumentos e produtos musicais (a mesma do repositório symphony-sql).

O projeto implementa autenticação JWT, controle de acesso por cargos e operações relacionadas a categorias, produtos, usuários e pedidos. Basicamente, é só um repositório simples para que eu tenha um capítulo do meu github narrando isso, para não passar em branco.

## Funcionalidades

- Consulta da situação da API
- Cadastro e autenticação de usuários
- Autenticação via token JWT
- Controle de acesso para clientes, funcionários e administradores
- CRUD de categorias
- CRUD de produtos
- Criação e consulta de pedidos
- Atualização do status dos pedidos
- Atualização automática do estoque
- Proteção de rotas administrativas
- Banco de dados SQLite local
- Dados iniciais por meio de scripts SQL e dados em JSON
- Documentação interativa gerada pelo FastAPI

## 🛠️ Tecnologias utilizadas

- **Python 3.14**
- **FastAPI 0.141.1**
- **SQLAlchemy 2.0.52**
- **SQLite**
- **Pydantic 2.13.5**
- **PyJWT 2.15.1**
- **bcrypt 5.0.0**
- **Uvicorn (via fastapi[standard])**

## 📦 Estrutura do projeto

```text
symphony-api/
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── categorias.py
│   │   ├── pedidos.py
│   │   └── produtos.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── data/
├── sql/
│   ├── schema.sql
│   └── seed.sql
├── init_db.py
├── requirements.txt
├── users.json
└── README.md
```

## Instalação

### 1. Criar um ambiente virtual

```bash
python -m venv .venv
```

### 2. Ativar o ambiente virtual

**Linux/macOS:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicializar o banco de dados

```bash
python3 init_db.py
```
(ou só python, se o seu retornar comando não existente)

Esse comando executa o arquivo schema.sql, insere os dados de exemplo de seed.sql e cria os usuários definidos em users.json.

O banco SQLite é criado em data/database.db.

> O script de inicialização não foi projetado para ser executado várias vezes sobre o mesmo banco, pois tentará recriar dados e produzirá todo tipo de erro indesejado.

## Executar a API

```bash
fastapi dev app/main.py
```
### Verificação de funcionamento

Endpoint público:

```http
GET /
```

Exemplo de resposta:

```json
{
  "running": "True"
}
```

## Autenticação

A autenticação utiliza tokens JWT com o esquema Bearer.

### Login

```http
POST /auth
Content-Type: application/json
```

Corpo da requisição:

```json
{
  "email": "eduardo.lima@symphony.com",
  "senha": "senha_impossivel_de_adivinhar"
}
```

Exemplo de resposta:

```json
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

Use a ferramenta Authorize do Swagger do FastAPI (o cadeadozinho verde à direita do cabeçalho), ou então envie o token nas rotas protegidas:

```http
Authorization: Bearer SEU_TOKEN
```

Os tokens expiram após duas horas, mas ninguém vai demorar tanto tem.

## Dados de demonstração

O arquivo users.json contém usuários para teste:

| Cargo | E-mail | Senha |
|---|---|---|
| Cliente | laerte.oxiartes@example.com | senha123 |
| Cliente | maria.oliveira@example.com | senha456 |
| Cliente | carlos.santos@example.com | senha789 |
| Funcionário | doralice.costa@symphony.com | senha_extremamente_forte |
| Administrador | eduardo.lima@symphony.com | senha_impossivel_de_adivinhar |

A senha armazenada no banco é protegida por um hash bcrypt.

## Permissões

| Cargo | Permissões |
|---|---|
| Cliente | Consultar produtos e categorias, criar pedidos e consultar seus próprios pedidos |
| Funcionário | Gerenciar categorias e produtos; consultar e alterar pedidos |
| Administrador | Igual, talvez futuramente tenha mais permissões |

Funcionários e administradores podem alterar pedidos para `concluido`. Clientes não possuem essa permissão.

## Endpoints

### Produtos

| Método | Rota | Acesso |
|---|---|---|
| `GET` | `/produtos` | Público |
| `GET` | `/produtos/{product_id}` | Público |
| `POST` | `/produtos` | Funcionário ou administrador |
| `PUT` | `/produtos/{product_id}` | Funcionário ou administrador |
| `DELETE` | `/produtos/{product_id}` | Funcionário ou administrador |

Exemplo de criação de produto:

```json
{
  "nome": "Violão Folk",
  "preco": 1200,
  "estoque": 8,
  "categoria_id": 1
}
```

### Categorias

| Método | Rota | Acesso |
|---|---|---|
| `GET` | `/categorias` | Público |
| `GET` | `/categorias/{categoria_id}` | Público |
| `POST` | `/categorias` | Funcionário ou administrador |
| `PUT` | `/categorias/{categoria_id}` | Funcionário ou administrador |
| `DELETE` | `/categorias/{categoria_id}` | Funcionário ou administrador |

Exemplo de criação de categoria:

```json
{
  "nome": "Cordas"
}
```

### Pedidos

| Método | Rota | Acesso |
|---|---|---|
| `POST` | `/pedidos` | Autenticado |
| `GET` | `/pedidos/{pedido_id}` | Proprietário, funcionário ou administrador |
| `PUT` | `/pedidos/{pedido_id}` | Proprietário, funcionário ou administrador |

Exemplo de criação de pedido:

```json
{
  "produtos": [
    {
      "produto_id": 1,
      "quantidade": 2
    },
    {
      "produto_id": 3,
      "quantidade": 1
    }
  ]
}
```

Na criação:

- O usuário é identificado pelo token JWT.
- Cada produto precisa existir.
- A quantidade precisa ser maior que zero.
- É preciso haver pelo menos um produto.
- A quantidade solicitada não pode exceder o estoque.
- Os produtos em estoque são atualizados automaticamente.
- O preço unitário é salvo no momento da compra.

Exemplo de atualização do status (rota aceita substituição ou patch):

```json
{
  "status": "concluido"
}
```

Os status disponíveis são:

- `pendente`
- `concluido`
- `cancelado`

## Banco de dados

As principais entidades são:

- `categorias`
- `produtos`
- `usuarios`
- `pedidos`
- `itens_pedidos`

A tabela `itens_pedidos` salva o preço unitário do produto no momento da compra. Dessa forma, alterações futuras no preço não modificam o histórico do pedido.

## Estrutura das respostas

Os erros seguem o formato padrão de detalhes do FastAPI:

```json
{
  "detail": "Descrição do erro"
}
```

Implementa os status codes de acordo com a convenção:

- `400` — Dados inválidos ou estoque insuficiente
- `401` — Credenciais inválidas ou token ausente
- `403` — Usuário sem permissão
- `404` — Recurso não encontrado
- `500` — Erro interno durante uma operação

Bem que eu queria um lugar para pôr um 418...

## Observações

Este projeto foi criado com fins educacionais e possui simplificações que não devem ser usadas diretamente em produção:

- A chave secreta do JWT está diretamente no código.
- Os usuários de demonstração possuem senhas conhecidas.
- O banco SQLite foi escolhido pela praticidade.
- Não há migrações;
- Não há testes automatizados incluídos;

Só para constar que não sou tapado de achar que isso aqui é sério.