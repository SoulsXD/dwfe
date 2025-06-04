INSERT INTO user (username, password)
VALUES ('test', 'pbkdf2:sha256:600000$ZIXoD5JP0HuZZ0u2$73520603a2a42245cbf0e2de6fe0e2fffc3c5e5853ef582bafe884aeae7df52c');

INSERT INTO lista (nome, user_id)
VALUES ('Lista de Teste', 1);

INSERT INTO tarefa (descricao, concluida, lista_id)
VALUES ('Tarefa de Teste', 0, 1);
