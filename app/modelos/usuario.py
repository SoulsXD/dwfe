from app import banco
from flask_login import UserMixin

class Usuario(UserMixin, banco.Model):
    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(100), unique=True)
    senha = banco.Column(banco.String(100))