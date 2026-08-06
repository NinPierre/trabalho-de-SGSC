import os
from functools import wraps
from adm import *
from flask import Flask, flash, redirect, render_template, request, session, url_for



app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "EUSOUALUNOLICEU")



def limpar_cpf(cpf):
    return "".join(char for char in (cpf or "") if char.isdigit())



def autenticar_usuario(cpf, senha):
    cpf_limpo = limpar_cpf(cpf)

    try:
        usuario_banco = buscar_usuario(cpf_limpo, senha)
        use_banco = usuario_banco
        if usuario_banco:
            return use_banco
    except Exception:
        pass

    usuario_demo = DEMO_USERS.get(cpf_limpo)
    if usuario_demo and usuario_demo["senha"] == senha:
        return {"nome": usuario_demo["nome"], "tipo": usuario_demo["tipo"]}

    return None


def login_required(tipo=None):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if not session.get("logado"):
                return redirect(url_for("login"))
            if tipo and session.get("tipo_usuario") != tipo:
                return redirect(url_for("login"))
            return view(*args, **kwargs)

        return wrapper

    return decorator


def contexto_usuario(perfil):
    return {"nome": session.get("nome"), "perfil": perfil}


@app.route("/")
def login():
    if session.get("logado"):
        if session.get("tipo_usuario") == "professor":
            return redirect(url_for("professor_inicio"))
        if session.get("tipo_usuario") == "aluno":
            return redirect(url_for("aluno_inicio"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def autenticar():
    usuario = autenticar_usuario(request.form.get("cpf"), request.form.get("senha"))

    if not usuario:
        flash("Usuário ou senha inválidos.")
        return redirect(url_for("login"))

    session["nome"] = usuario["nome"]
    session["logado"] = True
    session["tipo_usuario"] = usuario["tipo"]

    if usuario["tipo"] == "professor":
        return redirect(url_for("professor_inicio"))
    return redirect(url_for("aluno_inicio"))


@app.route("/home")
def home():
    return redirect(url_for("login"))


@app.route("/professor/inicio")
@login_required("professor")
def professor_inicio():
    return render_template("Professor-inical.html", **contexto_usuario("professor"))


@app.route("/professor/lancar-notas")
@login_required("professor")
def lancar_notas():
    return render_template("Professor-lancar-notas.html", **contexto_usuario("professor"))


@app.route("/professor/desempenho-das-turmas")
@login_required("professor")
def professor_desempenho():
    return render_template("Professor-desempenho.html", **contexto_usuario("professor"))


@app.route("/professor/chamadas")
@login_required("professor")
def fazer_chamada():
    return render_template("Professor-chamadas.html", **contexto_usuario("professor"))


@app.route("/professor/alunos-em-alerta")
@login_required("professor")
def alunos_alerta():
    return render_template("Professor-alertas.html", **contexto_usuario("professor"))


@app.route("/professor/relatorios")
@login_required("professor")
def professor_relatorios():
    return render_template("Professor-relatorios.html", **contexto_usuario("professor"))


@app.route("/aluno/inicio")
@login_required("aluno")
def aluno_inicio():
    return render_template("Aluno-inicial.html", **contexto_usuario("aluno"))


@app.route("/aluno/ver-notas")
@login_required("aluno")
def aluno_notas():
    return render_template("Aluno-notas.html", notas=NOTAS_ALUNO, **contexto_usuario("aluno"))


@app.route("/aluno/ranking-das-turmas")
@login_required("aluno")
def ranking_turmas():
    return render_template("Ranking-turmas.html", ranking_turmas=RANKING_TURMAS, **contexto_usuario("aluno"))


@app.route("/aluno/ranking-dos-alunos")
@login_required("aluno")
def ranking_alunos():
    return render_template("Ranking-alunos.html", ranking_alunos=RANKING_ALUNOS, **contexto_usuario("aluno"))


@app.route("/aluno/ranking-da-turma")
@login_required("aluno")
def ranking_turma():
    return render_template("Aluno-ranking-turma.html", ranking_turma=RANKING_TURMA, **contexto_usuario("aluno"))


@app.route("/aluno/presenca-nas-aulas")
@login_required("aluno")
def aluno_presenca():
    return render_template("Aluno-presença.html", **contexto_usuario("aluno"))


@app.route("/sair")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
