from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('tarefas', __name__, url_prefix='/tarefas')

def get_lista(id, verificar_usuario=True):
    lista = get_db().execute(
        'SELECT id, titulo, usuario_id FROM lista WHERE id = ?', (id,)
    ).fetchone()

    if lista is None:
        abort(404, f"Lista id {id} não existe.")
    if verificar_usuario and lista['usuario_id'] != g.user['id']:
        abort(403)

    return lista

@bp.route('/<int:lista_id>/')
@login_required
def index(lista_id):
    lista = get_lista(lista_id)
    tarefas = get_db().execute(
        'SELECT id, descricao, completa FROM tarefa WHERE lista_id = ?',
        (lista_id,)
    ).fetchall()
    return render_template('tarefas/index.html', lista=lista, tarefas=tarefas)

@bp.route('/<int:lista_id>/criar', methods=('GET', 'POST'))
@login_required
def criar(lista_id):
    get_lista(lista_id)

    if request.method == 'POST':
        descricao = request.form['descricao']
        erro = None

        if not descricao:
            erro = 'Descrição é obrigatória.'

        if erro:
            flash(erro)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tarefa (descricao, lista_id) VALUES (?, ?)',
                (descricao, lista_id)
            )
            db.commit()
            return redirect(url_for('tarefas.index', lista_id=lista_id))

    return render_template('tarefas/create.html', lista_id=lista_id)

@bp.route('/<int:lista_id>/<int:tarefa_id>/completar', methods=('POST',))
@login_required
def completar(lista_id, tarefa_id):
    db = get_db()
    db.execute(
        'UPDATE tarefa SET completa = NOT completa WHERE id = ? AND lista_id = ?',
        (tarefa_id, lista_id)
    )
    db.commit()
    return redirect(url_for('tarefas.index', lista_id=lista_id))

@bp.route('/<int:lista_id>/<int:tarefa_id>/excluir', methods=('POST',))
@login_required
def excluir(lista_id, tarefa_id):
    db = get_db()
    db.execute('DELETE FROM tarefa WHERE id = ? AND lista_id = ?', (tarefa_id, lista_id))
    db.commit()
    return redirect(url_for('tarefas.index', lista_id=lista_id))
