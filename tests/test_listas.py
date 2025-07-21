def test_lista_index(auth_client): 
    response = auth_client.get('/listas/', follow_redirects=True)
    assert b'Lista Teste' in response.data

def test_create_lista(auth_client):
    response = auth_client.post('/listas/criar', data={
        'titulo': 'Nova Lista'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Nova Lista' in response.data
