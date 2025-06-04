from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('todo', __name__)

@bp.route('/')
def index():
    db = get_db()
    listas = db.execute(
        'SELECT l.id, l.titulo, l.criado_em, l.author_id, u.username '
        'FROM lista l JOIN user u ON l.author_id = u.id '
        'ORDER BY l.criado_em DESC'
    ).fetchall()
    return render_template('listas/index.html', listas=listas)

@bp.route('/criar', methods=('GET', 'POST'))
@login_required
def criar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        erro = None

        if not titulo:
            erro = 'O título é obrigatório.'

        if erro:
            flash(erro)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO lista (titulo, author_id) VALUES (?, ?)',
                (titulo, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('listas/criar.html')

def get_lista(id, check_author=True):
    lista = get_db().execute(
        'SELECT l.id, l.titulo, l.criado_em, l.author_id, u.username '
        'FROM lista l JOIN user u ON l.author_id = u.id '
        'WHERE l.id = ?',
        (id,)
    ).fetchone()

    if lista is None:
        abort(404, f"A lista com id {id} não existe.")

    if check_author and lista['author_id'] != g.user['id']:
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
            erro = 'O título é obrigatório.'

        if erro:
            flash(erro)
        else:
            db = get_db()
            db.execute(
                'UPDATE lista SET titulo = ? WHERE id = ?',
                (titulo, id)
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('listas/atualizar.html', lista=lista)

@bp.route('/<int:id>/deletar', methods=('POST',))
@login_required
def deletar(id):
    get_lista(id)
    db = get_db()
    db.execute('DELETE FROM lista WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('todo.index'))

# --- Tarefas ---

def get_tarefa(id, check_author=True):
    tarefa = get_db().execute(
        'SELECT t.id, t.titulo, t.descricao, t.lista_id, l.author_id '
        'FROM tarefa t JOIN lista l ON t.lista_id = l.id '
        'WHERE t.id = ?',
        (id,)
    ).fetchone()

    if tarefa is None:
        abort(404, f"Tarefa id {id} não encontrada.")

    if check_author and tarefa['author_id'] != g.user['id']:
        abort(403)

    return tarefa

@bp.route('/listas/<int:lista_id>/tarefas/criar', methods=('GET', 'POST'))
@login_required
def criar_tarefa(lista_id):
    get_lista(lista_id)  # valida se lista existe e pertence ao user
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        erro = None

        if not titulo:
            erro = 'O título é obrigatório.'

        if erro:
            flash(erro)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tarefa (titulo, descricao, lista_id) VALUES (?, ?, ?)',
                (titulo, descricao, lista_id)
            )
            db.commit()
            return redirect(url_for('todo.ver_lista', id=lista_id))

    return render_template('tarefas/criar.html')

@bp.route('/tarefas/<int:id>/atualizar', methods=('GET', 'POST'))
@login_required
def atualizar_tarefa(id):
    tarefa = get_tarefa(id)

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        erro = None

        if not titulo:
            erro = 'O título é obrigatório.'

        if erro:
            flash(erro)
        else:
            db = get_db()
            db.execute(
                'UPDATE tarefa SET titulo = ?, descricao = ? WHERE id = ?',
                (titulo, descricao, id)
            )
            db.commit()
            return redirect(url_for('todo.ver_lista', id=tarefa['lista_id']))

    return render_template('tarefas/atualizar.html', tarefa=tarefa)

@bp.route('/tarefas/<int:id>/deletar', methods=('POST',))
@login_required
def deletar_tarefa(id):
    tarefa = get_tarefa(id)
    db = get_db()
    db.execute('DELETE FROM tarefa WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('todo.ver_lista', id=tarefa['lista_id']))

@bp.route('/listas/<int:id>')
@login_required
def ver_lista(id):
    lista = get_lista(id)

    tarefas = get_db().execute(
        'SELECT id, titulo, descricao FROM tarefa WHERE lista_id = ? ORDER BY id DESC',
        (id,)
    ).fetchall()

    return render_template('listas/ver.html', lista=lista, tarefas=tarefas)