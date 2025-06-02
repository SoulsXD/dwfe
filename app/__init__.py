from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

banco = SQLAlchemy()
login = LoginManager()

def criar_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'f8b74f07296978329a9592a2ca03754fc593be341226e15f4980a7a5a8e79f1e'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'

    banco.init_app(app)
    login.init_app(app)

    from app.rotas import rotas
    app.register_blueprint(rotas)

    return app
