def test_tarefa_index(auth_client):
    # Verifica se a tarefa padrão aparece
    response = auth_client.get('/tarefas/1/', follow_redirects=True)
    assert "Tarefa Teste" in response.get_data(as_text=True)


def test_create_tarefa(auth_client):
    # Cria nova tarefa e verifica se aparece
    response = auth_client.post('/tarefas/1/criar', data={
        'descricao': 'Nova tarefa de teste'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Nova tarefa de teste" in response.get_data(as_text=True)


def test_create_tarefa_sem_descricao(auth_client):
    # Tenta criar tarefa sem descrição e valida mensagem de erro
    response = auth_client.post('/tarefas/1/criar', data={
        'descricao': ''
    }, follow_redirects=True)
    assert "Descrição é obrigatória." in response.get_data(as_text=True)


def test_completar_tarefa(auth_client):
    # Marca/desmarca tarefa como completa
    response = auth_client.post('/tarefas/1/1/completar', follow_redirects=True)
    assert response.status_code == 200
    # Verifica se continua exibindo a mesma descrição
    assert "Tarefa Teste" in response.get_data(as_text=True)


def test_excluir_tarefa(auth_client):
    # Exclui a tarefa e verifica se desaparece da lista
    response = auth_client.post('/tarefas/1/1/excluir', follow_redirects=True)
    assert response.status_code == 200
    assert "Tarefa Teste" not in response.get_data(as_text=True)
