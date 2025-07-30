import pytest
from flaskr.db import get_db
from werkzeug.security import generate_password_hash

@pytest.fixture
def init_user(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        # Remove o usuário se já existir
        cursor.execute("DELETE FROM user WHERE username = %s", ('testuser',))
        # Insere o usuário
        cursor.execute(
            "INSERT INTO user (username, password) VALUES (%s, %s)",
            ('testuser', generate_password_hash('testpass'))
        )
        db.commit()
        cursor.close()


def test_register_success(client, app):
    response = client.post('/auth/register', data={
        'username': 'novo_usuario',
        'password': 'senha123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Logar" in response.get_data(as_text=True)  # página de login após registro

    # Verifica se o usuário foi inserido no banco
    with app.app_context():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE username = %s", ('novo_usuario',))
        user = cursor.fetchone()
        cursor.close()
        assert user is not None


def test_register_validate_input(client):
    # Nome vazio
    response = client.post('/auth/register', data={
        'username': '',
        'password': 'senha123'
    }, follow_redirects=True)
    assert "O nome é obrigatório." in response.get_data(as_text=True)

    # Senha vazia
    response = client.post('/auth/register', data={
        'username': 'usuario',
        'password': ''
    }, follow_redirects=True)
    assert "A senha é obrigatória." in response.get_data(as_text=True)


def test_register_duplicate(client):
    # Registra usuário inicialmente
    client.post('/auth/register', data={
        'username': 'duplicado',
        'password': 'senha123'
    })

    # Tenta registrar novamente
    response = client.post('/auth/register', data={
        'username': 'duplicado',
        'password': 'senha456'
    }, follow_redirects=True)

    assert "já está registrado" in response.get_data(as_text=True)


def test_login_success(client, init_user):
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Lista" in response.get_data(as_text=True)  # Página inicial após login


def test_login_invalid_user(client):
    response = client.post('/auth/login', data={
        'username': 'usuario_invalido',
        'password': 'qualquer'
    }, follow_redirects=True)
    assert "Usuário errado." in response.get_data(as_text=True)


def test_login_invalid_password(client, init_user):
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'senha_errada'
    }, follow_redirects=True)
    assert "Senha errada." in response.get_data(as_text=True)

def test_logout(client, init_user):
    # Faz login
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)

    # Faz logout
    response = client.get('/auth/logout', follow_redirects=True)
    
    # Verifica que foi redirecionado para a tela de login (título da página)
    assert "Logar" in response.get_data(as_text=True)

    # Tenta acessar rota protegida depois do logout
    response2 = client.get('/listas/', follow_redirects=True)
    assert "Logar" in response2.get_data(as_text=True)
