from flask import Blueprint, render_template, session

import adm as db
from src.blueprints.auth import login_required

professor_bp = Blueprint("professor_bp", __name__)


def contexto_usuario(perfil):
    nome = session.get("nome") or "Usuário"
    return {"nome": nome, "nome_usuario": nome, "perfil": perfil}


@professor_bp.route("/professor/inicio", endpoint="professor_inicio")
@login_required("professor")
def professor_inicio():
    return render_template("Professor-inical.html", **contexto_usuario("professor"))


@professor_bp.route("/professor/lancar-notas", endpoint="lancar_notas")
@login_required("professor")
def lancar_notas():
    return render_template("Professor-lancar-notas.html", **contexto_usuario("professor"))


@professor_bp.route("/professor/desempenho-das-turmas", endpoint="professor_desempenho")
@login_required("professor")
def professor_desempenho():
    ranking_turmas = db.gerar_ranking_geral_das_turmas()
    return render_template("Professor-desempenho.html", ranking_turmas=ranking_turmas, **contexto_usuario("professor"))


@professor_bp.route("/professor/chamadas", endpoint="fazer_chamada")
@login_required("professor")
def fazer_chamada():
    return render_template("Professor-chamadas.html", **contexto_usuario("professor"))


@professor_bp.route("/professor/alunos-em-alerta", endpoint="alunos_alerta")
@login_required("professor")
def alunos_alerta():
    return render_template("Professor-alertas.html", **contexto_usuario("professor"))


@professor_bp.route("/professor/relatorios", endpoint="professor_relatorios")
@login_required("professor")
def professor_relatorios():
    return render_template("Professor-relatorios.html", **contexto_usuario("professor"))
