from flask import (
    Blueprint, render_template, g
)
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('todo', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    listas = db.execute(
        'SELECT l.id, l.titulo, l.criado_em '
        'FROM lista_tarefas l '
        'WHERE l.usuario_id = ? '
        'ORDER BY l.criado_em DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('todo/index.html', listas=listas)
