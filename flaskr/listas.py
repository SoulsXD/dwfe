from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('listas', __name__, url_prefix='/listas')

@bp.route('/')
@login_required
def index():
    db = get_db()
    listas = db.execute(
        'SELECT id, titulo FROM lista WHERE usuario_id = ?',
        (g.user['id'],)
    ).fetchall()
    return render_template('listas/index.html', listas=listas)

@bp.route('/criar', methods=('GET', 'POST'))
@login_required
def criar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        erro = None

        if not titulo:
            erro = 'Título é obrigatório.'

        if erro is not None:
            flash(erro)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO lista (titulo, usuario_id) VALUES (?, ?)',
                (titulo, g.user['id'])
            )
            db.commit()
            return redirect(url_for('listas.index'))

    return render_template('listas/create.html')

def get_lista(id, verificar_usuario=True):
    lista = get_db().execute(
        'SELECT id, titulo, usuario_id FROM lista WHERE id = ?',
        (id,)
    ).fetchone()

    if lista is None:
        abort(404, f"Lista id {id} não existe.")
    if verificar_usuario and lista['usuario_id'] != g.user['id']:
        abort(403)

    return lista

@bp.route('/<int:id>/atualizar', methods=('GET', 'POST'))
@login_required
def atualizar(id):
    lista = get_lista(id)

    if request.method == 'POST':
        titulo = request.form['titulo']
        erro = None

        if not titulo:
            erro = 'Título é obrigatório.'

        if erro is not None:
            flash(erro)
        else:
            db = get_db()
            db.execute(
                'UPDATE lista SET titulo = ? WHERE id = ?',
                (titulo, id)
            )
            db.commit()
            return redirect(url_for('listas.index'))

    return render_template('listas/create.html', lista=lista)

@bp.route('/<int:id>/excluir', methods=('POST',))
@login_required
def excluir(id):
    get_lista(id)
    db = get_db()
    db.execute('DELETE FROM lista WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('listas.index'))
