import os
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for

# Importando suas funções do adm.py
import adm as db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "EUSOUALUNOLICEU")


def limpar_cpf(cpf):
    return "".join(char for char in (cpf or "") if char.isdigit())


def autenticar_usuario(cpf, senha):
    cpf_limpo = limpar_cpf(cpf)

    try:
        # Busca no banco de dados usando o SQLAlchemy (via adm.py)
        usuario_banco = db.buscar_usuario(cpf_limpo, senha)
        if usuario_banco:
            return usuario_banco
    except Exception as e:
        print(f"Erro ao autenticar: {e}")
        pass

    return None


def login_required(perfil=None):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if not session.get("logado"):
                return redirect(url_for("login"))
            if perfil and session.get("perfil_usuario") != perfil:
                flash("Acesso não autorizado.", "danger")
                return redirect(url_for("login"))
            return view(*args, **kwargs)

        return wrapper

    return decorator


def contexto_usuario(perfil):
    return {"nome_usuario": session.get("nome"), "perfil": perfil}


# ==========================
# ROTAS DE AUTENTICAÇÃO
# ==========================
@app.route("/")
def login():
    if session.get("logado"):
        if session.get("perfil_usuario") == "professor":
            return redirect(url_for("professor_inicio"))
        if session.get("perfil_usuario") == "aluno":
            return redirect(url_for("aluno_inicio"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def autenticar():
    usuario = autenticar_usuario(request.form.get("cpf"), request.form.get("senha"))

    if not usuario or not usuario.ativo:
        flash("Usuário ou senha inválidos, ou conta desativada.", "danger")
        return redirect(url_for("login"))

    # Como o SQLAlchemy retorna um objeto, usamos a notação de ponto (.)
    session["usuario_id"] = usuario.id
    session["nome"] = usuario.nome
    session["logado"] = True
    session["perfil_usuario"] = usuario.perfil

    if usuario.perfil == "professor":
        return redirect(url_for("professor_inicio"))
    return redirect(url_for("aluno_inicio"))


@app.route("/home")
def home():
    return redirect(url_for("login"))


@app.route("/sair")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ==========================
# ROTAS DO PROFESSOR
# ==========================
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
    # Exemplo utilizando função do adm.py para ranking geral das turmas
    ranking_turmas = db.gerar_ranking_geral_das_turmas()
    return render_template("Professor-desempenho.html", ranking_turmas=ranking_turmas, **contexto_usuario("professor"))


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


# ==========================
# ROTAS DO ALUNO
# ==========================
@app.route("/aluno/inicio")
@login_required("aluno")
def aluno_inicio():
    return render_template("Aluno-inicial.html", **contexto_usuario("aluno"))


@app.route("/aluno/ver-notas")
@login_required("aluno")
def aluno_notas():
    # Buscando o boletim completo do aluno logado usando o adm.py
    boletim = db.obter_boletim(session.get("usuario_id"))
    return render_template("Aluno-notas.html", boletim=boletim, **contexto_usuario("aluno"))


@app.route("/aluno/ranking-das-turmas")
@login_required("aluno")
def ranking_turmas():
    ranking_turmas_dados = db.gerar_ranking_geral_das_turmas()
    return render_template("Ranking-turmas.html", ranking_turmas=ranking_turmas_dados, **contexto_usuario("aluno"))


@app.route("/aluno/ranking-dos-alunos")
@login_required("aluno")
def ranking_alunos():
    # Pode ser adaptado caso crie uma função de ranking geral de alunos no adm.py
    return render_template("Ranking-alunos.html", **contexto_usuario("aluno"))


@app.route("/aluno/ranking-da-turma")
@login_required("aluno")
def ranking_turma():
    # Nota: Idealmente passaria o turma_id do aluno logado
    return render_template("Aluno-ranking-turma.html", **contexto_usuario("aluno"))


@app.route("/aluno/presenca-nas-aulas")
@login_required("aluno")
def aluno_presenca():
    boletim = db.obter_boletim(session.get("usuario_id"))
    presencas = boletim["presencas"] if boletim else []
    return render_template("Aluno-presença.html", presencas=presencas, **contexto_usuario("aluno"))


if __name__ == "__main__":
    app.run(debug=True)