from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.services.auth_service import autenticar_usuario, perfil_para_sessao

auth_bp = Blueprint("auth_bp", __name__)


def login_required(perfil=None):
    def decorator(view):
        from functools import wraps

        @wraps(view)
        def wrapper(*args, **kwargs):
            if not session.get("logado"):
                return redirect(url_for("auth_bp.login"))
            if perfil and session.get("perfil_usuario") != perfil:
                flash("Acesso não autorizado.", "danger")
                return redirect(url_for("auth_bp.login"))
            return view(*args, **kwargs)

        return wrapper

    return decorator


@auth_bp.route("/", endpoint="login")
def login():
    if session.get("logado"):
        if session.get("perfil_usuario") == "professor":
            return redirect(url_for("professor_bp.professor_inicio"))
        if session.get("perfil_usuario") == "aluno":
            return redirect(url_for("aluno_bp.aluno_inicio"))
        if session.get("perfil_usuario") == "admin":
            return redirect(url_for("admin_bp.admin_dashboard"))
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"], endpoint="autenticar")
def autenticar():
    usuario = autenticar_usuario(request.form.get("cpf"), request.form.get("senha"))

    if not usuario or not usuario.ativo:
        flash("Usuário ou senha inválidos, ou conta desativada.", "danger")
        return redirect(url_for("auth_bp.login"))

    session["usuario_id"] = usuario.id
    session["nome"] = usuario.nome
    session["logado"] = True
    session["perfil_usuario"] = perfil_para_sessao(usuario.perfil)

    if session["perfil_usuario"] == "professor":
        return redirect(url_for("professor_bp.professor_inicio"))
    if session["perfil_usuario"] == "admin":
        return redirect(url_for("admin_bp.admin_dashboard"))
    return redirect(url_for("aluno_bp.aluno_inicio"))


@auth_bp.route("/home", endpoint="home")
def home():
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/sair", endpoint="logout")
def logout():
    session.clear()
    return redirect(url_for("auth_bp.login"))
