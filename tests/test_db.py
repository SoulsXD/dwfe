from flaskr.db import get_db
#testa o banco de dados
def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db.is_connected()  # garante que conexão foi aberta
        db.close()
