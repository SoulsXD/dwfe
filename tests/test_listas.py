def test_lista_index(auth_client):
    # Verifica se a lista existente aparece na página
    response = auth_client.get('/listas/', follow_redirects=True)
    assert b'Lista Teste' in response.data

def test_create_lista(auth_client):
    # Cria nova lista e verifica se aparece na página
    response = auth_client.post('/listas/criar', data={
        'titulo': 'Nova Lista'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Nova Lista' in response.data

def test_create_lista_sem_titulo(auth_client):
    # Tenta criar lista sem título e verifica mensagem de erro
    response = auth_client.post('/listas/criar', data={'titulo': ''}, follow_redirects=True)
    assert "Título é obrigatório.".encode('utf-8') in response.data

def test_update_lista(auth_client, app):
    # Atualiza lista existente
    with app.app_context():
        client = auth_client
        response = client.post('/listas/1/atualizar', data={'titulo': 'Lista Atualizada'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Lista Atualizada' in response.data

def test_delete_lista(auth_client, app):
    # Deleta lista existente
    with app.app_context():
        client = auth_client
        response = client.post('/listas/1/excluir', follow_redirects=True)
        assert response.status_code == 200
        assert b'Lista Teste' not in response.data
