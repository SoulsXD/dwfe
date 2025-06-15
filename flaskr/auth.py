import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from mysql.connector.errors import IntegrityError

from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        g.user = cursor.fetchone()
        cursor.close()

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "O nome é obrigatório."
        elif not password:
            error = "A senha é obrigatória."

        if error is None:
            try:
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO user (username, password) VALUES (%s, %s)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                cursor.close()
            except IntegrityError:
                error = f"O usuário {username} já está registrado."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user is None:
            error = "Usuário errado."
        elif not check_password_hash(user["password"], password):
            error = "Senha errada."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("listas.index"))

        flash(error)

    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("listas.index"))
