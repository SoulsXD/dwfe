from app import banco

class Tarefa(banco.Model):
    id = banco.Column(banco.Integer, primary_key=True)
    descricao = banco.Column(banco.String(200))
    feita = banco.Column(banco.Boolean, default=False)
    lista_id = banco.Column(banco.Integer, banco.ForeignKey('lista.id'))