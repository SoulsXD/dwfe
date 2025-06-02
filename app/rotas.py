from flask import Blueprint, render_template, redirect, request, url_for
from app import banco, login
from app.modelos.usuario import Usuario
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.modelos.lista import Lista
from app.modelos.tarefa import Tarefa

rotas = Blueprint('rotas', __name__)

@login.user_loader
def carregar_usuario(usuario_id):
    return Usuario.query.get(int(usuario_id))

# CRUD de Listas
@rotas.route('/listas')
@login_required
def ver_listas():
    listas = Lista.query.filter_by(usuario_id=current_user.id).all()
    return render_template('listas/listas.html', listas=listas)

@rotas.route('/listas/nova', methods=['GET', 'POST'])
@login_required
def nova_lista():
    if request.method == 'POST':
        titulo = request.form['titulo']
        nova = Lista(titulo=titulo, usuario_id=current_user.id)
        banco.session.add(nova)
        banco.session.commit()
        return redirect(url_for('rotas.ver_listas'))
    return render_template('listas/nova_lista.html')

@rotas.route('/listas/<int:lista_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_lista(lista_id):
    lista = Lista.query.get_or_404(lista_id)
    if lista.usuario_id != current_user.id:
        return "Acesso negado"
    
    if request.method == 'POST':
        lista.titulo = request.form['titulo']
        banco.session.commit()
        return redirect(url_for('rotas.ver_listas'))
    
    return render_template('listas/editar_lista.html', lista=lista)

@rotas.route('/listas/<int:lista_id>/excluir')
@login_required
def excluir_lista(lista_id):
    lista = Lista.query.get_or_404(lista_id)
    if lista.usuario_id != current_user.id:
        return "Acesso negado"

    for tarefa in lista.tarefas:
        banco.session.delete(tarefa)

    banco.session.delete(lista)
    banco.session.commit()
    return redirect(url_for('rotas.ver_listas'))


# CRUD de Tarefas
@rotas.route('/listas/<int:lista_id>/tarefas')
@login_required
def ver_tarefas(lista_id):
    lista = Lista.query.get_or_404(lista_id)
    if lista.usuario_id != current_user.id:
        return "Acesso negado"
    return render_template('tarefas/tarefas.html', lista=lista)

@rotas.route('/listas/<int:lista_id>/tarefas/nova', methods=['POST'])
@login_required
def nova_tarefa(lista_id):
    descricao = request.form['descricao']
    nova = Tarefa(descricao=descricao, lista_id=lista_id)
    banco.session.add(nova)
    banco.session.commit()
    return redirect(url_for('rotas.ver_tarefas', lista_id=lista_id))

@rotas.route('/tarefas/<int:id>/concluir')
@login_required
def concluir_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    tarefa.feita = not tarefa.feita
    banco.session.commit()
    return redirect(url_for('rotas.ver_tarefas', lista_id=tarefa.lista_id))

@rotas.route('/tarefas/<int:id>/excluir')
@login_required
def excluir_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    lista_id = tarefa.lista_id
    banco.session.delete(tarefa)
    banco.session.commit()
    return redirect(url_for('rotas.ver_tarefas', lista_id=lista_id))

@rotas.route('/tarefas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    if tarefa.lista.usuario_id != current_user.id:
        return "Acesso negado"

    if request.method == 'POST':
        tarefa.descricao = request.form['descricao']
        tarefa.feita = 'feita' in request.form
        banco.session.commit()
        return redirect(url_for('rotas.ver_tarefas', lista_id=tarefa.lista_id))

    return render_template('tarefas/editar_tarefa.html', tarefa=tarefa)

# CRUD USUARIO

@rotas.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar_usuarios.html', usuarios=usuarios)

from flask import flash

@rotas.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
def novo_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = generate_password_hash(request.form['senha'], method='pbkdf2:sha256')

        if Usuario.query.filter_by(nome=nome).first():
            flash('Nome de usuário já existe. Escolha outro.', 'erro')
            return redirect(url_for('rotas.novo_usuario'))

        novo = Usuario(nome=nome, senha=senha)
        banco.session.add(novo)
        banco.session.commit()
        flash('Usuário criado com sucesso!', 'sucesso')
        return redirect(url_for('rotas.listar_usuarios'))
    return render_template('usuarios/novo_usuario.html')

@rotas.route('/usuarios/<int:id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        senha = request.form['senha']

        if not check_password_hash(usuario.senha, senha):
            flash('Senha incorreta. Exclusão cancelada.', 'erro')
            return redirect(url_for('rotas.excluir_usuario', id=id))

        banco.session.delete(usuario)
        banco.session.commit()
        flash('Usuário excluído com sucesso.', 'sucesso')

        if usuario.id == current_user.id:
            logout_user()
            return redirect(url_for('rotas.inicio'))

        return redirect(url_for('rotas.listar_usuarios'))

    return render_template('usuarios/excluir_usuario.html', usuario=usuario)


# INICIO

@rotas.route('/')
def inicio():
    return render_template('inicio.html')

@rotas.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = generate_password_hash(request.form['senha'], method='pbkdf2:sha256')
        novo_usuario = Usuario(nome=nome, senha=senha)
        banco.session.add(novo_usuario)
        banco.session.commit()
        return redirect(url_for('rotas.login'))
    return render_template('cadastro.html')

@rotas.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(nome=nome).first()
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('rotas.painel'))
    return render_template('login.html')

@rotas.route('/sair')
@login_required
def sair():
    logout_user()
    return redirect(url_for('rotas.inicio'))

@rotas.route('/painel')
@login_required
def painel():
    return redirect(url_for('rotas.ver_listas'))