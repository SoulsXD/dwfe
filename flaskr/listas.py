from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('listas', __name__, url_prefix='/listas')

@bp.route('/')
def index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        'SELECT id, titulo FROM lista WHERE user_id = %s',
        (g.user['id'],)
    )
    listas = cursor.fetchall()
    return render_template('listas/index.html', listas=listas)

@bp.route('/criar', methods=('GET', 'POST'))
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
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO lista (titulo, user_id) VALUES (%s, %s)',
                (titulo, g.user['id'])
            )
            db.commit()
            return redirect(url_for('listas.index'))

    return render_template('listas/create.html')

def get_lista(id, verificar_usuario=True):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        'SELECT id, titulo, user_id FROM lista WHERE id = %s',
        (id,)
    )
    lista = cursor.fetchone()

    if lista is None:
        abort(404, f"Lista id {id} não existe.")
    if verificar_usuario and lista['user_id'] != g.user['id']:
        abort(403)

    return lista

@bp.route('/<int:id>/atualizar', methods=('GET', 'POST'))
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
            cursor = db.cursor()
            cursor.execute(
                'UPDATE lista SET titulo = %s WHERE id = %s',
                (titulo, id)
            )
            db.commit()
            return redirect(url_for('listas.index'))

    return render_template('listas/create.html', lista=lista)

@bp.route('/<int:id>/excluir', methods=('POST',))
def excluir(id):
    get_lista(id)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM lista WHERE id = %s', (id,))
    db.commit()
    return redirect(url_for('listas.index'))
