from app import banco

class Lista(banco.Model):
    id = banco.Column(banco.Integer, primary_key=True)
    titulo = banco.Column(banco.String(100))
    usuario_id = banco.Column(banco.Integer, banco.ForeignKey('usuario.id'))
    tarefas = banco.relationship('Tarefa', backref='lista', lazy=True)
