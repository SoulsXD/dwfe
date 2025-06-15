import mysql.connector
from flask import current_app, g
import click

def get_db():
    if 'db' not in g:
        config = current_app.config['DB_CONFIG']
        g.db = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()
    with current_app.open_resource('schema.sql') as f:
        statements = f.read().decode('utf8').split(';')
        for stmt in statements:
            stmt = stmt.strip()
            if stmt:
                cursor.execute(stmt)
    db.commit()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Banco de dados MySQL inicializado.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)    