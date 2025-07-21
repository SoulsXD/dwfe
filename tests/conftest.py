import os
import pytest
from flaskr import create_app
from flaskr.db import get_db

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'MYSQL_HOST': 'localhost',
        'MYSQL_USER': 'root',
        'MYSQL_PASSWORD': '1608',
        'MYSQL_DATABASE': 'flask_test',
    })

    # Define uma chave secreta para a sessão funcionar corretamente
    app.secret_key = 'test_secret_key'

    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Criar tabelas necessárias
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(150) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lista (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefa (
            id INT AUTO_INCREMENT PRIMARY KEY,
            descricao TEXT NOT NULL,
            completa BOOLEAN DEFAULT FALSE,
            lista_id INT NOT NULL,
            FOREIGN KEY (lista_id) REFERENCES lista(id) ON DELETE CASCADE
        );
        """)
        db.commit()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Limpa o banco e insere dados de teste antes de cada teste
@pytest.fixture(autouse=True)
def limpar_banco(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE tarefa;")
        cursor.execute("TRUNCATE TABLE lista;")
        cursor.execute("TRUNCATE TABLE user;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        db.commit()

        # Insere usuário e dados básicos
        cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", ('testuser', 'testpass'))
        user_id = cursor.lastrowid
        cursor.execute("INSERT INTO lista (titulo, user_id) VALUES (%s, %s)", ('Lista Teste', user_id))
        lista_id = cursor.lastrowid
        cursor.execute("INSERT INTO tarefa (descricao, completa, lista_id) VALUES (%s, %s, %s)",
                       ('Tarefa Teste', False, lista_id))
        db.commit()

# Cliente já autenticado manualmente pela sessão para burlar o login required (tava dando erro)
@pytest.fixture
def auth_client(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1 
        return client
