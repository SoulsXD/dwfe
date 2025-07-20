def test_login_invalid(client):
    response = client.post('/auth/login', data={
        'username': 'usuario_invalido',
        'password': 'senhaqualquer'
    }, follow_redirects=True)
    page_text = response.get_data(as_text=True)
    assert "Usuário errado" in page_text or "Senha errada" in page_text

    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'senha_errada'
    }, follow_redirects=True)
    page_text = response.get_data(as_text=True)
    assert "Usuário errado" in page_text or "Senha errada" in page_text