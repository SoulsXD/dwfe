def test_tarefa_index(auth_client):
    response = auth_client.get('/tarefas/1', follow_redirects=True)
    assert b'Tarefa Teste' in response.data

def test_create_tarefa(auth_client):
    response = auth_client.post('/tarefas/1/criar', data={
        'descricao': 'Nova tarefa de teste'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Nova tarefa de teste' in response.data