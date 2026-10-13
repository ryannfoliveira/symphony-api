from sqlalchemy import text
from app.database import engine
import os
import json
import bcrypt

base_dir = os.path.dirname(os.path.abspath(__file__))

def init_db(path: str):
    '''
    Função responsável por inicializar o banco de dados
    com o schema e os dados iniciais fictícios.
    '''
    with open(path, 'r') as f:
        statements = f.read().strip()

    raw = engine.raw_connection()

    try:
        raw.executescript(statements)
        raw.commit()
    finally:
        raw.close()


def insert_users(path: str):
    '''
    Função responsável por inserir usuários fictícios no banco de dados.
    '''

    with open(path, 'r') as f:
        usuarios = json.load(f)

    with engine.begin() as conn:
        # Usando as vantangens do ORM para deixar o projeto mais tolerante a mudança de SGBD
        # pois aquela sintaxe de "VALUES (?, ?, [...])" não é entendida por todos eles
        query = text("INSERT INTO usuarios (nome, email, senha, cargo) VALUES (:nome, :email, :senha, :cargo)")

        for i, usuario in enumerate(usuarios):
            print(f"Inserindo usuário {i + 1}/{len(usuarios)}")
            usuario['senha'] = bcrypt.hashpw(usuario['senha'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            conn.execute(query, usuario)


def main():
    schema_path = os.path.join(base_dir, 'sql', 'schema.sql')
    seed_path = os.path.join(base_dir, 'sql', 'seed.sql')
    users_path = os.path.join(base_dir,  'users.json')
    
    print("Criando tabelas...")
    init_db(schema_path)

    print("Populando tabelas...")
    init_db(seed_path)

    print("Inserindo usuários fictícios...")
    insert_users(users_path)

    print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    main()