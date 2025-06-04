from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db
from flaskr.auth import login_required

bp = Blueprint('listas', __name__, url_prefix='/listas')


@bp.route('/')
@login_required
def index():
    db = get_db()
    listas = db.execute(
        'SELECT id, titulo, criado_em FROM lista ORDER BY criado_em DESC'
    ).fetchall()
    return render_template('listas/index.html', listas=listas)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        titulo = request.form['titulo']
        error = None

        if not titulo:
            error = 'O título da lista é obrigatório.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO lista (titulo) VALUES (?)',
                (titulo,)
            )
            db.commit()
            return redirect(url_for('listas.index'))

    return render_template('listas/create.html')


def get_lista(id, check_author=True):
    lista = get_db().execute(
        'SELECT id, titulo FROM lista WHERE id = ?',
        (id,)
    ).fetchone()

    if lista is None:
        abort(404, f"Lista id {id} não existe.")

    return lista


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    lista = get_lista(id)

    if request.method == 'POST':
        titulo = request.form['titulo']
        error = None

        if not titulo:
            error = 'O título da lista é obrigatório.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE lista SET titulo = ? WHERE id = ?',
                (titulo, id)
            )
            db.commit()
            return redirect(url_for('listas.index'))

    return render_template('listas/edit.html', lista=lista)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM lista WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('listas.index'))
